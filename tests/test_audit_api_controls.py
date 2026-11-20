"""
POST /controls/{name} carries the same authority check as /risk-controls.

The endpoint routes to the very setters /risk-controls and /execution-mode
own, so authenticating the key is not enough: a read-only key holder who also
knows OPERATOR_SECRET must be refused with 403, before the write is attempted.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

PRIMARY = "a" * 40
READONLY = "b" * 40
_OPERATOR_SECRET = "operator-secret-" + "d" * 32  # pragma: allowlist secret
_WRONG_SECRET = "wrong-secret-" + "e" * 32  # pragma: allowlist secret


@pytest.fixture
def client(
    monkeypatch: pytest.MonkeyPatch, healthy_security_controls: object
) -> Iterator[TestClient]:
    monkeypatch.setenv("API_SECRET_KEY", PRIMARY)
    monkeypatch.setenv("API_READONLY_KEY", READONLY)
    monkeypatch.setenv("OPERATOR_SECRET", _OPERATOR_SECRET)

    from src.api import main as api_main

    monkeypatch.setattr(api_main._state, "ready", True, raising=False)
    calls: list[tuple[str, object]] = []

    async def _recording_apply_control(name: str, value: object, *args: object, **kw: object):
        calls.append((name, value))
        return {"name": name, "value": value}

    monkeypatch.setattr(api_main, "apply_control", _recording_apply_control)
    test_client = TestClient(api_main.app)
    test_client.calls = calls  # type: ignore[attr-defined]
    yield test_client


def _post(client: TestClient, key: str, secret: str):
    return client.post(
        "/controls/risk_controls.stop_loss_pct",
        headers={"x-api-key": key},
        json={"value": 0.05, "operator": "alice", "operator_secret": secret},
    )


def test_read_only_key_with_correct_operator_secret_is_403(client: TestClient) -> None:
    response = _post(client, READONLY, _OPERATOR_SECRET)

    assert response.status_code == 403
    assert client.calls == []  # type: ignore[attr-defined]


def test_trade_authorizing_key_passes_the_role_gate(client: TestClient) -> None:
    response = _post(client, PRIMARY, _OPERATOR_SECRET)

    assert response.status_code == 200
    assert client.calls == [("risk_controls.stop_loss_pct", 0.05)]  # type: ignore[attr-defined]


def test_operator_secret_is_still_enforced_for_an_authorized_key(client: TestClient) -> None:
    response = _post(client, PRIMARY, _WRONG_SECRET)

    assert response.status_code == 401
    assert client.calls == []  # type: ignore[attr-defined]


def test_route_declares_the_same_gates_as_risk_controls() -> None:
    from fastapi.routing import APIRoute

    from src.api.main import app, require_healthy_security_controls

    route = next(
        r
        for r in app.routes
        if isinstance(r, APIRoute) and r.path == "/controls/{name}" and "POST" in r.methods
    )
    calls = [dep.call for dep in route.dependant.dependencies]
    assert any(getattr(c, "__name__", "") == "_dependency" for c in calls)
    assert require_healthy_security_controls in calls
