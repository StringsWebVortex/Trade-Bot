"""
SEC-0016 -- the runtime operator's name and kind come from their credential.

Audit API-012: every /runtime write built its change-manager Actor from the
``operator`` name and ``actor_kind`` the request body chose, checked only
against one shared OPERATOR_SECRET. An AI client holding that secret sent
``actor_kind="human"`` and became an approver, and the audit recorded
whatever name it typed. With OPERATOR_CREDENTIALS set, the secret alone picks
the operator, and a body that claims another name or kind is refused.
Without it, the single-secret model stays as documented: the holder is the
human operator, and a claim can only lower that to ``ai``.
"""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Iterator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.api.runtime_control import (
    RuntimeControlError,
    RuntimeDecisionBody,
    actor_for,
    parse_operator_credentials,
)
from src.eventbus import EventBus
from src.runtime.adapters import Discovery
from src.runtime.changes import ROLE_APPROVER, ActorKind
from src.runtime.contracts import ComponentType, LifecycleState
from src.runtime.platform import RuntimePlatform, build_runtime_platform
from tests.runtime._support import FakeController, spec

TRADE = {"x-api-key": "t" * 32}
LEGACY = "s" * 32
HUMAN_SECRET = "h" * 32
AI_SECRET = "a" * 32


def _sha(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


CREDENTIALS = json.dumps(
    {
        "alice": {"kind": "human", "secret_sha256": _sha(HUMAN_SECRET)},
        "agent": {"kind": "ai", "secret_sha256": _sha(AI_SECRET)},
    }
)


def _body(operator: str, secret: str, kind: str | None = None) -> RuntimeDecisionBody:
    return RuntimeDecisionBody(operator=operator, operator_secret=secret, actor_kind=kind)


@pytest.fixture
def credentials() -> Iterator[None]:
    env = {"OPERATOR_SECRET": LEGACY, "OPERATOR_CREDENTIALS": CREDENTIALS}
    with patch.dict(os.environ, env):
        yield


@pytest.mark.parametrize("kind", [None, "ai"])
def test_an_ai_credential_is_an_ai_actor(credentials: None, kind: str | None) -> None:
    actor = actor_for(_body("agent", AI_SECRET, kind))
    assert (actor.name, actor.kind) == ("agent", ActorKind.AI)
    assert ROLE_APPROVER not in actor.roles


def test_a_human_credential_is_a_human_approver(credentials: None) -> None:
    actor = actor_for(_body("alice", HUMAN_SECRET))
    assert (actor.name, actor.kind) == ("alice", ActorKind.HUMAN)
    assert ROLE_APPROVER in actor.roles


@pytest.mark.parametrize(
    ("operator", "secret", "kind", "status"),
    [
        ("agent", AI_SECRET, "human", 403),  # the API-012 hole
        ("alice", AI_SECRET, None, 403),  # an AI credential borrowing a human name
        ("alice", HUMAN_SECRET, "ai", 403),
        ("alice", "wrong" * 8, None, 401),
        ("alice", LEGACY, None, 401),  # OPERATOR_SECRET no longer opens runtime writes
    ],
)
def test_a_claim_that_disagrees_with_the_credential_is_refused(
    credentials: None, operator: str, secret: str, kind: str | None, status: int
) -> None:
    with pytest.raises(RuntimeControlError) as refused:
        actor_for(_body(operator, secret, kind))
    assert refused.value.status == status


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ("not json", "not valid JSON"),
        ("{}", "non-empty"),
        ('{"bad name": {"kind": "human", "secret_sha256": "' + "0" * 64 + '"}}', "must match"),
        ('{"x": {"kind": "system", "secret_sha256": "' + "0" * 64 + '"}}', "kind must be"),
        ('{"x": {"kind": "ai", "secret_sha256": "ABC"}}', "64 lowercase hex"),
        ('{"x": {"kind": "ai"}}', "exactly the fields"),
        (
            json.dumps(
                {
                    "x": {"kind": "human", "secret_sha256": _sha(HUMAN_SECRET)},
                    "y": {"kind": "ai", "secret_sha256": _sha(HUMAN_SECRET)},
                }
            ),
            "shares its secret",
        ),
        (json.dumps({"x": {"kind": "ai", "secret_sha256": _sha(LEGACY)}}), "OPERATOR_SECRET"),
    ],
)
def test_an_ambiguous_credential_map_is_rejected(raw: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        parse_operator_credentials(raw, LEGACY)


def test_an_unusable_credential_map_fails_closed() -> None:
    env = {"OPERATOR_SECRET": LEGACY, "OPERATOR_CREDENTIALS": "{}"}
    with patch.dict(os.environ, env), pytest.raises(RuntimeControlError) as refused:
        actor_for(_body("alice", HUMAN_SECRET))
    assert refused.value.status == 503


def test_a_human_may_hold_the_legacy_secret_as_their_credential() -> None:
    raw = json.dumps({"alice": {"kind": "human", "secret_sha256": _sha(LEGACY)}})
    env = {"OPERATOR_SECRET": LEGACY, "OPERATOR_CREDENTIALS": raw}
    with patch.dict(os.environ, env):
        assert actor_for(_body("alice", LEGACY)).kind is ActorKind.HUMAN


@pytest.mark.parametrize(("kind", "expected"), [(None, ActorKind.HUMAN), ("ai", ActorKind.AI)])
def test_without_credentials_the_secret_holder_is_human_unless_lowered(
    kind: str | None, expected: ActorKind
) -> None:
    env = {"OPERATOR_SECRET": LEGACY, "OPERATOR_CREDENTIALS": ""}
    with patch.dict(os.environ, env):
        actor = actor_for(_body("alice", LEGACY, kind))
    assert (actor.name, actor.kind) == ("alice", expected)


def _platform() -> RuntimePlatform:
    return build_runtime_platform(
        bus=EventBus(),
        discoveries=[Discovery(spec("v"), LifecycleState.STANDBY)],
        controllers={t: FakeController() for t in ComponentType},
    )


@pytest.fixture
def api() -> Iterator[tuple[TestClient, RuntimePlatform]]:
    from src.api.main import AppState, app

    state = AppState()
    state.ready = True
    state.storage = AsyncMock()
    state.orchestrator = MagicMock()
    state.runtime = _platform()
    env = {
        "API_SECRET_KEY": "t" * 32,
        "OPERATOR_SECRET": LEGACY,
        "OPERATOR_CREDENTIALS": CREDENTIALS,
    }
    with patch.dict(os.environ, env), patch("src.api.main._state", state):
        yield TestClient(app, raise_server_exceptions=False), state.runtime


def test_an_ai_client_cannot_approve_by_claiming_to_be_human(
    api: tuple[TestClient, RuntimePlatform],
) -> None:
    client, platform = api
    ai = {"operator": "agent", "operator_secret": AI_SECRET}
    body = {**ai, "component_id": "worker:v", "action": "activate", "reason": "go live"}
    change = client.post("/runtime/changes", headers=TRADE, json=body).json()
    assert (change["status"], change["actor"]["kind"]) == ("AWAITING_APPROVAL", "ai")
    cid = change["change_id"]

    claimed = client.post(
        f"/runtime/changes/{cid}/approve", headers=TRADE, json={**ai, "actor_kind": "human"}
    )
    assert claimed.status_code == 403
    assert platform.changes.get(cid).approved_by is None

    human = {"operator": "alice", "operator_secret": HUMAN_SECRET}
    approved = client.post(f"/runtime/changes/{cid}/approve", headers=TRADE, json=human).json()
    assert approved["approved_by"] == "alice"
    audit = [(e.event, e.actor) for e in platform.changes.audit_log(cid)]
    assert audit[0][1] == "agent" and ("approved", "alice") in audit
