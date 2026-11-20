"""
API authorization and secret-handling regressions (API-001..005, API-007).

Each test fails against the code before the fix:
  - SEC-1010  POST /controls/{name} enforces the role, not only a valid key
  - SEC-1011  /controls/execution_mode persists, audits and is rate-limited
  - SEC-1012  POST /controls writes only allow-listed leaves, and audits them
  - SEC-1013  GET /controls never renders a DSN or other secret value
  - SEC-1014  the WebSocket key stays out of the URL and uvicorn's logs
  - SEC-1015  operator-secret guessing is bounded globally and secrets are strong
"""

from __future__ import annotations

import logging
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

_TRADE_KEY = "t" * 32
_READ_KEY = "r" * 32
_OP_SECRET = "s" * 32
_BODY = {"value": "manual", "operator": "alice", "operator_secret": _OP_SECRET}


@pytest.fixture
def wired():
    from src.api.fail_closed import CONTROL_HEALTH, SecurityControl, mark_all_healthy
    from src.api.main import AppState

    # API-008: model startup completing, then restore the process-wide registry
    # exactly as it was so this module cannot leak health state to other tests.
    previous_health = {control: CONTROL_HEALTH.status(control) for control in SecurityControl}
    CONTROL_HEALTH.reset()
    mark_all_healthy(CONTROL_HEALTH)
    state = AppState()
    state.ready = True
    state.storage = AsyncMock()
    state.orchestrator = MagicMock()
    env = {
        "API_SECRET_KEY": _TRADE_KEY,
        "API_READONLY_KEY": _READ_KEY,
        "OPERATOR_SECRET": _OP_SECRET,
    }
    with (
        patch.dict(os.environ, env),
        patch("src.api.main._state", state),
        patch("src.api.main.save_execution_mode") as save,
    ):
        state.save_mock = save
        try:
            yield state
        finally:
            CONTROL_HEALTH.reset()
            for control, status in previous_health.items():
                if status.healthy:
                    CONTROL_HEALTH.mark_healthy(control)
                else:
                    CONTROL_HEALTH.mark_degraded(control, status.reason)


def _client() -> TestClient:
    from src.api.main import app

    return TestClient(app, raise_server_exceptions=False)


def _post(name: str, body: dict, key: str = _TRADE_KEY):
    return _client().post(f"/controls/{name}", headers={"x-api-key": key}, json=body)


@pytest.fixture(autouse=True)
def _restore_mode():
    import asyncio

    from src.config import runtime_config

    original = asyncio.run(runtime_config.get_execution_mode())
    yield
    asyncio.run(runtime_config.set_execution_mode(original))


# --- SEC-1010 -------------------------------------------------------------


def test_read_only_key_cannot_write_a_control(wired) -> None:
    """A read-only key holding the operator secret used to change anything."""
    resp = _post("execution_mode", _BODY, key=_READ_KEY)
    assert resp.status_code == 403
    wired.storage.insert_audit_event.assert_not_called()


# --- SEC-1011 -------------------------------------------------------------


def test_controls_execution_mode_persists_and_audits(wired) -> None:
    resp = _post("execution_mode", _BODY)
    assert resp.status_code == 200, resp.text
    wired.save_mock.assert_called_once()
    events = [c.kwargs["event_type"] for c in wired.storage.insert_audit_event.call_args_list]
    assert "execution_mode_change" in events


def test_controls_execution_mode_is_rate_limited(wired) -> None:
    codes = [_post("execution_mode", _BODY).status_code for _ in range(4)]
    assert codes[:3] == [200, 200, 200]
    assert codes[3] == 429


def test_apply_control_refuses_execution_mode_without_the_safe_setter() -> None:
    import asyncio

    from src.api.control_surface import ControlWriteError, apply_control
    from src.api.main import SetRiskControlsRequest

    with pytest.raises(ControlWriteError) as exc_info:
        asyncio.run(
            apply_control(
                "execution_mode",
                "manual",
                SetRiskControlsRequest,
                operator="a",
                operator_secret="b",
            )
        )
    assert exc_info.value.status == 409


# --- SEC-1012 -------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "expected_status"),
    [
        ("storage.decision_log_path", 403),
        ("intelligence.glassnode_base_url", 409),
        ("binance.testnet", 409),
        ("binance.base_url", 403),
    ],
)
def test_non_allow_listed_leaves_are_refused(wired, name, expected_status) -> None:
    """Unallowlisted keys are refused; startup-bound keys use conflict semantics."""
    resp = _post(name, {**_BODY, "value": "/tmp/x"})
    assert resp.status_code == expected_status, resp.text


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("risk.kelly_multiplier", True),
        ("xgboost.n_estimators", True),
        ("storage.decision_log_path", False),
        ("intelligence.coinglass_base_url", False),
        ("api.host", False),
        ("brand_new_group.anything", False),
        ("nodot", False),
    ],
)
def test_allow_list_is_default_deny(name, expected) -> None:
    from src.api.control_surface import is_operator_writable

    assert is_operator_writable(name) is expected


def test_registered_tunables_still_require_the_operator_allow_list(monkeypatch) -> None:
    """A newly registered parameter must not bypass the API's default-deny list."""
    import asyncio

    from src.api import control_surface
    from src.api.control_surface import ControlWriteError, apply_control

    monkeypatch.setattr(control_surface.parameter_registry, "is_registered", lambda _name: True)
    apply = patch.object(control_surface, "_apply_tunable")
    with apply as apply_tunable:
        with pytest.raises(ControlWriteError) as exc_info:
            asyncio.run(
                apply_control(
                    "future_group.new_parameter",
                    1,
                    object,
                    operator="alice",
                    operator_secret=_OP_SECRET,
                )
            )
    assert exc_info.value.status == 403
    apply_tunable.assert_not_called()


def test_a_control_write_is_audited(wired) -> None:
    from src.config import invalidate_settings_cache

    try:
        resp = _post("risk.kelly_multiplier", {**_BODY, "value": 0.2})
        assert resp.status_code == 200, resp.text
    finally:
        invalidate_settings_cache()
    call = wired.storage.insert_audit_event.call_args
    assert call.kwargs["event_type"] == "control_change"
    assert call.kwargs["details"]["control"] == "risk.kelly_multiplier"


# --- SEC-1013 -------------------------------------------------------------


def test_get_controls_renders_no_secret_value(wired) -> None:
    resp = _client().get("/controls", headers={"x-api-key": _READ_KEY})
    assert resp.status_code == 200
    assert "tradebot-local" not in resp.text
    dsn = next(c for c in resp.json()["controls"] if c["name"] == "storage.timescale_dsn")
    assert dsn["value"] is None and dsn["protected"] is True


def test_no_secret_looking_settings_leaf_is_ever_valued() -> None:
    from src.api.control_surface import settings_controls

    for control in settings_controls():
        if any(m in control.name for m in ("dsn", "password", "token", "secret", "api_key")):
            assert control.value is None, control.name


# --- SEC-1014 -------------------------------------------------------------


def test_uvicorn_log_records_have_the_key_redacted() -> None:
    from src.logging_setup import RedactUrlSecretsFilter

    record = logging.LogRecord(
        "uvicorn.error",
        logging.INFO,
        "",
        0,
        '%s - "WebSocket %s" [accepted]',
        ("1.2.3.4:5", "/ws?api_key=SUPERSECRET&x=1"),
        None,
    )
    assert RedactUrlSecretsFilter().filter(record)
    assert "SUPERSECRET" not in record.getMessage()
    assert "x=1" in record.getMessage()


def test_configure_logging_installs_the_uvicorn_filter() -> None:
    from src.logging_setup import RedactUrlSecretsFilter, configure_logging

    configure_logging()
    configure_logging()
    filters = logging.getLogger("uvicorn.error").filters
    assert sum(isinstance(f, RedactUrlSecretsFilter) for f in filters) == 1


def test_websocket_accepts_the_subprotocol_key_and_echoes_only_the_safe_one(wired) -> None:
    key = _TRADE_KEY.encode().hex()
    with _client().websocket_connect("/ws", subprotocols=["tradebot.v1", f"apikey.{key}"]) as ws:
        assert ws.accepted_subprotocol == "tradebot.v1"


# --- SEC-1015 -------------------------------------------------------------


def test_wrong_secret_attempts_lock_out_even_the_correct_secret(wired) -> None:
    from src.api.operator_secret import MAX_FAILURES

    bad = {**_BODY, "operator_secret": "x" * 32}
    codes = [_post("execution_mode", bad).status_code for _ in range(MAX_FAILURES)]
    assert set(codes) == {401}
    assert _post("execution_mode", bad).status_code == 429
    assert _post("execution_mode", _BODY).status_code == 429


def test_lockout_is_global_across_endpoints(wired) -> None:
    """Guesses spread over endpoints share one budget (was 60/min each)."""
    from src.api.operator_secret import MAX_FAILURES

    bad = {**_BODY, "operator_secret": "x" * 32}
    for _ in range(MAX_FAILURES):
        _client().post(
            "/risk-controls",
            headers={"x-api-key": _TRADE_KEY},
            json={"operator": "a", "operator_secret": "x" * 32},
        )
    assert _post("execution_mode", bad).status_code == 429


def test_execution_mode_endpoint_limit_runs_before_secret_check(wired) -> None:
    """Exhausted per-IP budget answers 429 without ever comparing the secret."""
    from src.api import operator_secret

    wired._ENDPOINT_LIMIT = 0
    with (
        patch.object(operator_secret, "verify_operator_secret") as verify,
        patch("src.api.main.verify_operator_secret", verify),
    ):
        resp = _client().post(
            "/execution-mode",
            headers={"x-api-key": _TRADE_KEY},
            json={"mode": "manual", "operator": "a", "operator_secret": "x" * 32},
        )
    assert resp.status_code == 429
    verify.assert_not_called()


@pytest.mark.asyncio
async def test_startup_refuses_a_short_operator_secret() -> None:
    from src.api.main import app, lifespan

    env = {"API_SECRET_KEY": _TRADE_KEY, "OPERATOR_SECRET": "short-secret"}
    with patch.dict(os.environ, env), pytest.raises(RuntimeError, match="at least 32"):
        async with lifespan(app):
            pass
