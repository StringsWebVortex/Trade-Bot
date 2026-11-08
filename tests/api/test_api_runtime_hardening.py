"""API-006/008/009/010/011/012/014/015/030 regressions.

Decides: SEC-1200, SEC-1201, SEC-1202, REG-1203, REG-1204, SEC-1205,
SEC-1207, SEC-1208, REG-1209"""

from __future__ import annotations

import asyncio
import inspect
import json
import time
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from src.api import main as api_main
from src.api.access_control import Role
from src.api.fail_closed import CONTROL_HEALTH, SecurityControl


class _Socket:
    def __init__(self, delay: float = 0.0, fail: bool = False) -> None:
        self.delay = delay
        self.fail = fail
        self.sent: list[dict] = []

    async def send_text(self, message: str) -> None:
        if self.delay:
            await asyncio.sleep(self.delay)
        if self.fail:
            raise RuntimeError("peer gone")
        self.sent.append(json.loads(message))


async def _state_with(clients: dict[_Socket, Role]) -> api_main.AppState:
    state = api_main.AppState()
    for ws, role in clients.items():
        assert await state.add_ws_client(ws)  # type: ignore[arg-type]
        state._ws_roles[ws] = role  # type: ignore[index]
    return state


# -- API-006 -----------------------------------------------------------------


async def test_read_only_socket_never_receives_pending_approvals() -> None:
    ro, op = _Socket(), _Socket()
    state = await _state_with({ro: Role.READ_ONLY, op: Role.TRADE_AUTHORIZING})
    await state.broadcast(
        {"type": "tick", "pending_approvals": [{"id": "x"}]},
        operator_only_fields=("pending_approvals",),
    )
    assert "pending_approvals" not in ro.sent[0]
    assert ro.sent[0]["type"] == "tick"
    assert op.sent[0]["pending_approvals"] == [{"id": "x"}]


def test_approvals_route_requires_the_approve_permission() -> None:
    route = next(r for r in api_main.app.routes if getattr(r, "path", "") == "/approvals")
    names = [getattr(d.call, "__qualname__", "") for d in route.dependant.dependencies]
    assert any("requires" in n for n in names)


# -- API-010 -----------------------------------------------------------------


async def test_stalled_client_does_not_hold_up_the_others() -> None:
    state = await _state_with(
        {_Socket(delay=60): Role.TRADE_AUTHORIZING, _Socket(): Role.TRADE_AUTHORIZING}
    )
    state._WS_SEND_TIMEOUT_S = 0.05
    started = time.monotonic()
    delivered = await state.broadcast({"type": "tick"})
    assert time.monotonic() - started < 2.0
    assert delivered == 1
    assert len(state.ws_clients) == 1  # the stalled peer was dropped


# -- API-008 -----------------------------------------------------------------


def test_every_trade_affecting_post_is_behind_the_security_control_gate() -> None:
    exempt = {"/risk/size-check", "/debug/selftest"}
    ungated = []
    for route in api_main.app.routes:
        if "POST" not in getattr(route, "methods", ()) or route.path in exempt:
            continue
        calls = [d.call for d in route.dependant.dependencies]
        if api_main.require_healthy_security_controls not in calls:
            ungated.append(route.path)
    assert not ungated, ungated


async def test_audit_write_failure_degrades_the_audit_control() -> None:
    CONTROL_HEALTH.reset()
    storage = MagicMock()

    async def boom(**_: object) -> None:
        raise OSError("disk full")

    storage.insert_audit_event = boom
    try:
        with pytest.raises(OSError):
            await api_main._audit_event(storage, event_type="x")
        assert SecurityControl.AUDIT_LOGGING in CONTROL_HEALTH.degraded()
    finally:
        CONTROL_HEALTH.reset()


def test_control_surface_audit_uses_the_fail_closed_wrapper() -> None:
    source = inspect.getsource(api_main)
    # The wrapper itself is the sole raw storage call; every route, including
    # the shared /controls/{name} route, must pass through it.
    assert source.count("insert_audit_event(") == 1
    assert "await _audit_event(\n        _state.storage,\n        event_type=\"control_change\"" in source


def test_unusable_key_configuration_degrades_authentication(monkeypatch) -> None:
    from src.api import auth

    CONTROL_HEALTH.reset()
    monkeypatch.delenv("API_SECRET_KEY", raising=False)
    try:
        with pytest.raises(HTTPException) as exc:
            auth.verify_api_key("anything")
        assert exc.value.status_code == 503
        assert SecurityControl.AUTHENTICATION in CONTROL_HEALTH.degraded()
    finally:
        CONTROL_HEALTH.reset()


# -- API-009 -----------------------------------------------------------------


def test_readiness_report_does_not_echo_raw_orchestrator_errors() -> None:
    from src.api.readiness import readiness_report

    dsn = "postgresql://trader:hunter2@db.internal:5432/bot"
    report = readiness_report(
        api_ready=True,
        stopping=False,
        runtime_ready=True,
        reconcile_passes=1,
        orchestrator={
            "warm_up": "failed",
            "error": f"connect failed {dsn}",
            "loops_started": False,
        },
        trading_mode="paper",
    )
    blob = json.dumps(report)
    assert "hunter2" not in blob and "db.internal" not in blob


def test_endpoints_do_not_return_str_exc_in_a_200_body() -> None:
    source = inspect.getsource(api_main)
    assert 'return {"error": str(exc)}' not in source


# -- API-011 -----------------------------------------------------------------


async def test_runtime_call_runs_off_the_event_loop() -> None:
    import threading

    main_thread = threading.get_ident()
    seen = await api_main._runtime_call(threading.get_ident)
    assert seen != main_thread


# -- API-012 -----------------------------------------------------------------


@pytest.mark.parametrize("bad", ["a b", "x\ny", "a;rm", "é"])
def test_operator_names_are_validated_on_runtime_and_control_bodies(bad: str) -> None:
    from src.api.runtime_control import OperatorFactor

    with pytest.raises(ValidationError):
        OperatorFactor(operator=bad, operator_secret="s")
    with pytest.raises(ValidationError):
        api_main.SetControlRequest(value=1, operator=bad, operator_secret="s")


# -- API-014 -----------------------------------------------------------------


def test_log_redaction_matches_key_substrings_and_walks_nested_values() -> None:
    from src.logging_setup import redact_event

    out = redact_event(
        None,
        "info",
        {
            "binance_api_secret": "abc",
            "timescale_dsn": "x",
            "details": {"old": {"db_passphrase": "p", "ok": 1}, "list": [{"token": "t"}]},
            "plain": "fine",
        },
    )
    assert out["binance_api_secret"] == "[REDACTED]"
    assert out["timescale_dsn"] == "[REDACTED]"
    assert out["details"]["old"]["db_passphrase"] == "[REDACTED]"
    assert out["details"]["old"]["ok"] == 1
    assert out["details"]["list"][0]["token"] == "[REDACTED]"
    assert out["plain"] == "fine"


# -- API-015 -----------------------------------------------------------------


def test_selftest_has_a_low_limit_and_a_dedicated_single_worker() -> None:
    assert api_main._SELFTEST_LIMIT_PER_MIN <= 5
    assert api_main._SELFTEST_EXECUTOR._max_workers == 1
    state = api_main.AppState()
    for _ in range(api_main._SELFTEST_LIMIT_PER_MIN):
        state.check_endpoint_rate_limit("t", "ip", limit=api_main._SELFTEST_LIMIT_PER_MIN)
    with pytest.raises(HTTPException) as exc:
        state.check_endpoint_rate_limit("t", "ip", limit=api_main._SELFTEST_LIMIT_PER_MIN)
    assert exc.value.status_code == 429


# -- API-030 -----------------------------------------------------------------


@pytest.mark.parametrize(
    "name",
    [
        "self_tuning.shadow_mode",
        "order_throttle.enabled",
        "order_throttle.rate",
        "order_throttle.burst",
        "order_throttle.max_wait_s",
        "intelligence.glassnode_base_url",
        "binance.testnet",
        "okx.testnet",
    ],
)
def test_construction_time_settings_are_not_reported_live(name: str) -> None:
    from src.api.control_surface import _STARTUP_ONLY, settings_controls

    assert name in _STARTUP_ONLY
    by_name = {c.name: c for c in settings_controls()}
    if name in by_name:
        assert by_name[name].live is False
