"""
The runtime platform's face on the existing control API.

Not a second control API: the routes live in ``src/api/main.py`` beside
``/controls``, behind the same API key, permission and rate-limit
dependencies, and every mutation needs the same operator second factor
(SEC-007). This module only turns request bodies into change-manager calls
and change-manager refusals into HTTP statuses.

The path is always

    API -> operator second factor -> ChangeManager (classify, dependencies,
    policy, approval) -> SupervisorSet -> controller -> component

and nothing here touches a supervisor, a controller or a subsystem
directly. An AI client (an agent behind an MCP tool, say) may request
changes and execute approved ones, but the change manager refuses it
approval, stage results and promotion.

Who is asking (SEC-0016). With OPERATOR_CREDENTIALS set, the operator's own
secret decides the name and kind (``human`` or ``ai``) the change manager
sees; the request body's ``operator`` and ``actor_kind`` must agree with the
credential or the call is refused, so an AI credential can never pass for a
human. Without it, the single OPERATOR_SECRET holder is the human operator
(``actor_kind="ai"`` can only lower that), so that secret must never be given
to an automated client.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import structlog
from pydantic import BaseModel, Field

from src.agent_control.model import ManifestError, to_dict
from src.agent_control.store import STATE_DIR_ENV, STATE_DIR_NAME, TaskStore
from src.runtime.adaptive import SYSTEM_EVALUATOR
from src.runtime.changes import (
    ROLE_APPROVER,
    ROLE_REQUESTER,
    Actor,
    ActorKind,
    ChangeError,
    ChangeRecord,
    ChangeRequest,
    ChangeStatus,
    RuntimeLifecycleUnavailableError,
    UnauthorizedError,
)
from src.runtime.contracts import (
    ComponentVersion,
    LifecycleAction,
    LifecycleState,
    RuntimeContractError,
)
from src.runtime.platform import RuntimePlatform
from src.runtime.registry import UnknownComponentError
from src.runtime.supervisor import ActionRefusedError

log: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

# What /runtime/components/{id}/{action} accepts: the operator's direct
# levers. Version changes and activations go through /runtime/changes, where
# the target version and the classification are explicit.
COMPONENT_ACTIONS: frozenset[str] = frozenset(
    {"pause", "resume", "drain", "stop", "deactivate", "quarantine", "rollback", "start"}
)


class RuntimeControlError(Exception):
    def __init__(self, status: int, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail


class OperatorFactor(BaseModel):
    operator: str = Field(min_length=1, max_length=64)
    operator_secret: str
    # None: take the kind from the credential (OPERATOR_CREDENTIALS) or, with
    # the single OPERATOR_SECRET, the human operator. A claim is never trusted
    # on its own: with credentials it must match, without them it can only
    # lower human to ai.
    actor_kind: Literal["human", "ai"] | None = None


class RuntimeChangeBody(OperatorFactor):
    component_id: str = Field(min_length=1, max_length=200)
    action: str
    reason: str = Field(min_length=1, max_length=500)
    target_version: str | None = Field(default=None, max_length=100)
    target_implementation: str | None = Field(default=None, max_length=200)
    target_configuration: dict[str, Any] | None = None
    expected_version: str | None = Field(default=None, max_length=100)


class RuntimeDecisionBody(OperatorFactor):
    reason: str = Field(default="", max_length=500)


class RuntimeActionBody(OperatorFactor):
    reason: str = Field(min_length=1, max_length=500)
    expected_version: str | None = Field(default=None, max_length=100)


class RuntimeDesiredBody(OperatorFactor):
    component_id: str = Field(min_length=1, max_length=200)
    target_state: str
    reason: str = Field(min_length=1, max_length=500)
    target_version: str | None = Field(default=None, max_length=100)


def check_operator_secret(secret: str) -> None:
    """SEC-007: the same second factor as /controls and /execution-mode."""
    expected = os.environ.get("OPERATOR_SECRET", "").strip()
    if not expected:
        raise RuntimeControlError(503, "OPERATOR_SECRET is not configured.")
    if not hmac.compare_digest(secret.encode("utf-8"), expected.encode("utf-8")):
        raise RuntimeControlError(401, "Invalid operator secret.")


OPERATOR_CREDENTIALS_ENV = "OPERATOR_CREDENTIALS"
_OPERATOR_NAME = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_CREDENTIAL_FIELDS = frozenset({"kind", "secret_sha256"})
_ROLES: dict[ActorKind, frozenset[str]] = {
    ActorKind.HUMAN: frozenset({ROLE_REQUESTER, ROLE_APPROVER}),
    ActorKind.AI: frozenset({ROLE_REQUESTER}),
}


@dataclass(frozen=True, slots=True)
class OperatorCredential:
    """One operator: the name and kind a matching secret authenticates as."""

    name: str
    kind: ActorKind
    secret_sha256: bytes


def _sha256(secret: str) -> bytes:
    return hashlib.sha256(secret.encode("utf-8")).digest()


def parse_operator_credentials(raw: str, operator_secret: str) -> tuple[OperatorCredential, ...]:
    """
    OPERATOR_CREDENTIALS: a JSON object mapping each operator name to
    ``{"kind": "human" | "ai", "secret_sha256": "<64 lowercase hex>"}``.

    Raises ValueError on anything that would make an identity ambiguous: a
    malformed entry, two operators sharing one secret, or an AI credential
    whose secret is OPERATOR_SECRET (which also unlocks the human-only
    /controls family).
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"not valid JSON ({exc.msg})") from None
    if not isinstance(data, dict) or not data:
        raise ValueError("must be a non-empty JSON object of operator name -> credential")
    legacy = _sha256(operator_secret) if operator_secret else None
    credentials: list[OperatorCredential] = []
    for name, entry in data.items():
        if not _OPERATOR_NAME.fullmatch(name):
            raise ValueError(f"operator name {name!r} must match {_OPERATOR_NAME.pattern}")
        if not isinstance(entry, dict) or set(entry) != _CREDENTIAL_FIELDS:
            raise ValueError(f"{name}: needs exactly the fields kind and secret_sha256")
        kind, hashed = entry["kind"], entry["secret_sha256"]
        if kind not in ("human", "ai"):
            raise ValueError(f"{name}: kind must be 'human' or 'ai'")
        if not isinstance(hashed, str) or not _SHA256_HEX.fullmatch(hashed):
            raise ValueError(f"{name}: secret_sha256 must be 64 lowercase hex characters")
        hashed_bytes = bytes.fromhex(hashed)
        if any(hmac.compare_digest(hashed_bytes, c.secret_sha256) for c in credentials):
            raise ValueError(f"{name}: shares its secret with another operator")
        if kind == "ai" and legacy is not None and hmac.compare_digest(hashed_bytes, legacy):
            raise ValueError(f"{name}: an ai credential must not use OPERATOR_SECRET")
        credentials.append(OperatorCredential(name, ActorKind(kind), hashed_bytes))
    return tuple(credentials)


def _credential_actor(body: OperatorFactor, raw: str) -> Actor:
    operator_secret = os.environ.get("OPERATOR_SECRET", "").strip()
    try:
        credentials = parse_operator_credentials(raw, operator_secret)
    except ValueError as exc:
        log.error("runtime_control.operator_credentials_invalid", error=str(exc))
        raise RuntimeControlError(503, f"{OPERATOR_CREDENTIALS_ENV} is not usable.") from None
    supplied = _sha256(body.operator_secret)
    # Every entry is compared, so the time taken does not say which matched.
    matched: OperatorCredential | None = None
    for credential in credentials:
        if hmac.compare_digest(supplied, credential.secret_sha256) and matched is None:
            matched = credential
    if matched is None:
        raise RuntimeControlError(401, "Invalid operator secret.")
    if body.operator != matched.name:
        log.warning(
            "runtime_control.operator_name_mismatch", claimed=body.operator, actual=matched.name
        )
        raise RuntimeControlError(403, "operator does not match the operator credential.")
    if body.actor_kind is not None and body.actor_kind != matched.kind.value:
        log.warning(
            "runtime_control.actor_kind_mismatch",
            operator=matched.name,
            claimed=body.actor_kind,
            actual=matched.kind.value,
        )
        raise RuntimeControlError(
            403, f"{matched.name} is a {matched.kind.value} operator, not {body.actor_kind}."
        )
    return Actor(matched.name, matched.kind, _ROLES[matched.kind])


def actor_for(body: OperatorFactor) -> Actor:
    """
    SEC-0016: the change manager's actor comes from the operator credential,
    never from what the request body claims about itself.
    """
    raw = os.environ.get(OPERATOR_CREDENTIALS_ENV, "").strip()
    if raw:
        return _credential_actor(body, raw)
    check_operator_secret(body.operator_secret)
    kind = ActorKind.AI if body.actor_kind == "ai" else ActorKind.HUMAN
    return Actor(body.operator, kind, _ROLES[kind])


def _action(name: str) -> LifecycleAction:
    try:
        return LifecycleAction(name.upper())
    except ValueError:
        raise RuntimeControlError(422, f"unknown lifecycle action {name!r}") from None


def _state(name: str) -> LifecycleState:
    try:
        return LifecycleState(name.upper())
    except ValueError:
        raise RuntimeControlError(422, f"unknown lifecycle state {name!r}") from None


def component(platform: RuntimePlatform, component_id: str) -> dict[str, Any]:
    record = platform.registry.find(component_id)
    if record is None:
        raise RuntimeControlError(404, f"unknown component {component_id}")
    return {
        **record.to_dict(platform.registry.dependents(component_id)),
        "history": [t.to_dict() for t in platform.registry.history(component_id)],
        "changes": [c.to_dict() for c in platform.changes.changes(component_id)],
    }


def change(platform: RuntimePlatform, change_id: str) -> dict[str, Any]:
    try:
        record = platform.changes.get(change_id)
    except ChangeError:
        raise RuntimeControlError(404, f"unknown change {change_id}") from None
    audit = platform.changes.audit_log(change_id)
    return {**record.to_dict(), "audit": [e.to_dict() for e in audit]}


def _submit(platform: RuntimePlatform, request: ChangeRequest) -> ChangeRecord:
    submitted = platform.changes.submit(request)
    # Taking risk off never waits: a LIVE_SAFE change is APPROVED on
    # submission and executes now, by the actor who asked.
    if submitted.status is ChangeStatus.APPROVED:
        return platform.changes.execute(submitted.change_id, request.actor)
    return submitted


def submit_change(platform: RuntimePlatform, body: RuntimeChangeBody) -> dict[str, Any]:
    actor = actor_for(body)
    action = _action(body.action)
    target = None
    if body.target_version is not None:
        current = platform.registry.find(body.component_id)
        if current is None:
            raise RuntimeControlError(404, f"unknown component {body.component_id}")
        implementation = body.target_implementation or current.version.implementation
        try:
            target = ComponentVersion.create(
                body.target_version, implementation, body.target_configuration
            )
        except RuntimeContractError as exc:
            raise RuntimeControlError(422, str(exc)) from exc
    request = ChangeRequest(
        component_id=body.component_id,
        action=action,
        actor=actor,
        reason=body.reason,
        target_version=target,
        expected_version=body.expected_version,
    )
    return _submit(platform, request).to_dict()


def component_action(
    platform: RuntimePlatform, component_id: str, action: str, body: RuntimeActionBody
) -> dict[str, Any]:
    if action not in COMPONENT_ACTIONS:
        raise RuntimeControlError(422, f"{action!r} is not a component action")
    request = ChangeRequest(
        component_id=component_id,
        action=_action(action),
        actor=actor_for(body),
        reason=body.reason,
        expected_version=body.expected_version,
    )
    return _submit(platform, request).to_dict()


def decide(
    platform: RuntimePlatform, change_id: str, verb: str, body: RuntimeDecisionBody
) -> dict[str, Any]:
    actor = actor_for(body)
    if verb not in {"approve", "execute", "promote", "rollback", "cancel"}:
        raise RuntimeControlError(404, f"unknown decision {verb!r}")
    changes = platform.changes
    try:
        result = changes.decide_lifecycle(
            change_id,
            verb,
            actor,
            reason=body.reason or "operator rollback",
            system_actor=SYSTEM_EVALUATOR,
        )
    except RuntimeLifecycleUnavailableError as exc:
        raise RuntimeControlError(503, str(exc)) from exc
    except UnauthorizedError as exc:
        raise RuntimeControlError(403, str(exc)) from exc
    except ActionRefusedError as exc:
        raise RuntimeControlError(409, str(exc)) from exc
    except ChangeError as exc:
        status = 404 if str(exc).startswith(("unknown change", "unknown component")) else 409
        raise RuntimeControlError(status, str(exc)) from exc
    return result.to_dict()


def set_desired(platform: RuntimePlatform, body: RuntimeDesiredBody) -> dict[str, Any]:
    actor = actor_for(body)
    try:
        desired = platform.changes.request_desired(
            body.component_id, _state(body.target_state), actor, body.reason, body.target_version
        )
    except UnknownComponentError:
        raise RuntimeControlError(404, f"unknown component {body.component_id}") from None
    except RuntimeContractError as exc:
        raise RuntimeControlError(422, str(exc)) from exc
    return desired.to_dict()


def note_operator_intent(
    platform: RuntimePlatform | None,
    component_id: str,
    target_state: LifecycleState,
    operator: str,
    reason: str,
) -> str | None:
    """
    Record as desired state a change an operator made through the subsystem's
    own endpoint (a gauntlet re-enable, /self-tuning/pause or /resume), so the
    runtime loop keeps it rather than reverting it to an older intent. The
    endpoint has already checked the operator second factor. Returns why it
    could not be recorded, or None.
    """
    if platform is None:
        return "runtime platform not started"
    if platform.registry.find(component_id) is None:
        return f"{component_id} is not registered"
    actor = Actor(operator, ActorKind.HUMAN, frozenset({ROLE_REQUESTER}))
    try:
        platform.changes.request_desired(component_id, target_state, actor, reason)
    except (UnknownComponentError, RuntimeContractError, UnauthorizedError) as exc:
        return str(exc)
    return None


def reconcile(platform: RuntimePlatform, body: OperatorFactor) -> list[dict[str, Any]]:
    actor_for(body)
    return [o.to_dict() for o in platform.reconciler.reconcile_once()]


def _agent_state_dir() -> Path:
    """TB_AGENT_STATE_DIR, else the clone's .git/agent-control (agent_control.store)."""
    override = os.environ.get(STATE_DIR_ENV, "").strip()
    return Path(override) if override else _REPO_ROOT / ".git" / STATE_DIR_NAME


_REPO_ROOT = Path(__file__).resolve().parents[2]


def agent_ledgers(state_dir: Path | None = None) -> dict[str, Any]:
    """
    The Claude session task manifests and the branch-audit ledger, read-only.
    A manifest that does not parse is reported by id, not skipped silently.
    """
    store = TaskStore(state_dir or _agent_state_dir())
    tasks: list[dict[str, Any]] = []
    unreadable: list[str] = []
    for task_id in store.task_ids():
        try:
            data = to_dict(store.load(task_id))
        except ManifestError as exc:
            unreadable.append(f"{task_id}: {exc}")
            continue
        steps = data["steps"]
        tasks.append(
            {
                "task_id": data["task_id"],
                "objective": data["objective"],
                "phase": data["phase"],
                "status": data["status"],
                "branch": data["branch"],
                "baseline_sha": data["baseline_sha"],
                "current_sha": data["current_sha"],
                "steps_done": sum(1 for step in steps if step["state"] != "OPEN"),
                "steps_total": len(steps),
                "next_action": data["next_action"],
                "updated_at": data["updated_at"],
            }
        )
    try:
        ledger = to_dict(store.load_ledger())["entries"]
    except ManifestError as exc:
        unreadable.append(f"branch-audit: {exc}")
        ledger = []
    return {"tasks": tasks, "branch_audit": ledger, "unreadable": unreadable}


def trace(platform: RuntimePlatform, trace_id: str) -> dict[str, Any]:
    found = platform.traces.trace(trace_id)
    if found is None:
        raise RuntimeControlError(404, f"no trace {trace_id}")
    return found.to_dict()
