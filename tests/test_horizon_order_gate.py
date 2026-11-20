"""Regression tests for the single risk-gated horizon order path.

Decides:
  - REG-0030 — horizon decisions cannot bypass the single risk-gated order path
"""

from __future__ import annotations

import asyncio
import time
from types import SimpleNamespace

import pytest
import structlog

from src.config import Timeframe
from src.engine.orchestrator import Orchestrator
from src.engine.signal_engine import SignalResult

_NOW = 1_800_000_000.0


@pytest.fixture(autouse=True)
def _frozen_wall_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    """The staleness gate reads time.time(); a fixed clock makes "fresh" and
    "5 s old" exact instead of depending on how long the test took."""
    monkeypatch.setattr(time, "time", lambda: _NOW)


def _orchestrator(action: str | None, *, observed_at: float | None = None) -> Orchestrator:
    orchestrator = Orchestrator.__new__(Orchestrator)
    orchestrator._primary_tf = Timeframe.INTRADAY
    orchestrator._symbol = "BTC/USDT"
    orchestrator._intelligence_task = None
    orchestrator._intelligence_adapter = SimpleNamespace(
        _intel=SimpleNamespace(
            _cfg={"inference_timeout_seconds": 1.0},
            last_decision=(
                {
                    "action": action,
                    "direction": 1 if action == "BUY" else -1,
                    "expected_return": 0.03 if action == "BUY" else -0.03,
                    "uncertainty": 0.005,
                    "conflict": False,
                    "contributions": {0: 1.0},
                    "model_versions": {0: "promoted-v1"},
                    "freshness_seconds": {0: 0.1},
                    "calibrated": True,
                    "abstain_reason": "no validated horizon expert",
                }
                if action is not None
                else None
            ),
            last_horizon_ts=time.time() if observed_at is None else observed_at,
            last_horizon_symbol="BTC/USDT",
        )
    )
    orchestrator._log = structlog.get_logger("test.horizon_order_gate")
    return orchestrator


def _result(direction: int = 1) -> SignalResult:
    return SignalResult(
        tradeable=True,
        direction=direction,
        p_long=0.8,
        p_bet=0.8,
        kelly_result=SimpleNamespace(adjusted_fraction=0.01),
        regime=None,
        gate_result=None,
        skip_reason="",
    )


def test_horizon_abstention_vetoes_an_existing_tradeable_signal(monkeypatch) -> None:
    monkeypatch.setenv("INTEL_ENABLED", "true")
    result = asyncio.run(
        _orchestrator("ABSTAIN")._apply_intelligence_order_gate(_result(), Timeframe.INTRADAY)
    )
    assert not result.tradeable
    assert result.kelly_result is None
    assert "no validated horizon expert" in result.skip_reason


def test_only_a_fresh_direction_aligned_decision_can_clear_the_extra_veto(monkeypatch) -> None:
    monkeypatch.setenv("INTEL_ENABLED", "true")
    orchestrator = _orchestrator("BUY")
    assert asyncio.run(
        orchestrator._apply_intelligence_order_gate(_result(1), Timeframe.INTRADAY)
    ).tradeable
    mismatch = asyncio.run(
        orchestrator._apply_intelligence_order_gate(_result(0), Timeframe.INTRADAY)
    )
    assert not mismatch.tradeable
    assert mismatch.skip_reason == "horizon_horizon_direction_disagrees_with_signal_engine"


def test_stale_and_non_primary_horizon_decisions_cannot_authorize_orders(monkeypatch) -> None:
    monkeypatch.setenv("INTEL_ENABLED", "true")
    stale = asyncio.run(
        _orchestrator("BUY", observed_at=time.time() - 5)._apply_intelligence_order_gate(
            _result(), Timeframe.INTRADAY
        )
    )
    secondary = asyncio.run(
        _orchestrator("BUY")._apply_intelligence_order_gate(_result(), Timeframe.SWING)
    )
    assert not stale.tradeable
    assert stale.skip_reason == "horizon_horizon_decision_stale"
    assert not secondary.tradeable
    assert secondary.skip_reason == "horizon_primary_timeframe_only"


def test_uncalibrated_or_symbol_mismatched_decision_fails_closed(monkeypatch) -> None:
    monkeypatch.setenv("INTEL_ENABLED", "true")
    uncalibrated = _orchestrator("BUY")
    uncalibrated._intelligence_adapter._intel.last_decision["calibrated"] = False
    result = asyncio.run(uncalibrated._apply_intelligence_order_gate(_result(), Timeframe.INTRADAY))
    assert not result.tradeable
    assert result.skip_reason == "horizon_horizon_decision_uncalibrated"

    wrong_symbol = _orchestrator("BUY")
    wrong_symbol._intelligence_adapter._intel.last_horizon_symbol = "ETH/USDT"
    result = asyncio.run(wrong_symbol._apply_intelligence_order_gate(_result(), Timeframe.INTRADAY))
    assert not result.tradeable
    assert result.skip_reason == "horizon_horizon_symbol_mismatch"


def test_malformed_or_future_horizon_decision_fails_closed(monkeypatch) -> None:
    monkeypatch.setenv("INTEL_ENABLED", "true")
    malformed = _orchestrator("BUY")
    malformed._intelligence_adapter._intel.last_decision["contributions"] = {}
    result = asyncio.run(malformed._apply_intelligence_order_gate(_result(), Timeframe.INTRADAY))
    assert not result.tradeable
    assert result.skip_reason == "horizon_horizon_decision_invalid"

    future = _orchestrator("BUY", observed_at=_NOW + 1.0)
    result = asyncio.run(future._apply_intelligence_order_gate(_result(), Timeframe.INTRADAY))
    assert not result.tradeable
    assert result.skip_reason == "horizon_horizon_decision_stale"


@pytest.mark.parametrize("horizon_action", ["BUY", "ABSTAIN"])
def test_full_tick_keeps_horizon_veto_inside_existing_executor_path(
    monkeypatch, horizon_action: str
) -> None:
    """A fused decision can veto an engine-approved signal, never originate one."""
    from unittest.mock import AsyncMock, MagicMock, patch

    from test_orchestrator_coverage import _make_executor, _make_orch, _make_storage

    from src.risk.kelly import KellyResult

    monkeypatch.setenv("INTEL_ENABLED", "true")
    orch = _make_orch()
    executor = _make_executor()
    executor.submit_signal = AsyncMock(return_value=("trade-1", "opened"))
    executor.get_current_equity = AsyncMock(return_value=10_000.0)
    executor.open_positions_safe = AsyncMock(return_value=[])
    orch._executor = executor
    orch._storage = _make_storage()
    orch._storage.latest_close = AsyncMock(return_value=None)
    orch._crypto_box = SimpleNamespace(enabled=False)
    orch._tick_counts = {Timeframe.INTRADAY.value: 0}
    orch._last_tick_ts = {Timeframe.INTRADAY.value: 0.0}
    orch._intelligence_adapter = _orchestrator("BUY")._intelligence_adapter
    if horizon_action == "ABSTAIN":
        orch._intelligence_adapter._intel.last_decision["action"] = "ABSTAIN"
        orch._intelligence_adapter._intel.last_decision["abstain_reason"] = "no validated expert"

    from src.engine.signal_engine import SignalResult

    kelly = KellyResult(
        kelly_fraction=0.04,
        adjusted_fraction=0.04,
        capital_usd=10_000.0,
        entry_price=42_000.0,
        quantity=0.01,
        notional_usd=420.0,
        is_capped=False,
    )
    engine = MagicMock()
    engine.tick = AsyncMock(
        return_value=SignalResult(
            tradeable=True,
            direction=1,
            p_long=0.8,
            p_bet=0.8,
            kelly_result=kelly,
            regime=None,
            gate_result=None,
            skip_reason="",
        )
    )
    orch._engines = {Timeframe.INTRADAY.value: engine}

    with (
        patch("src.engine.orchestrator.compute_win_loss_stats", return_value=(0, 0.0, 0.0, 0.0)),
        patch("src.engine.orchestrator.update_metrics"),
    ):
        asyncio.run(orch._tick(Timeframe.INTRADAY))

    engine.tick.assert_awaited_once()
    if horizon_action == "BUY":
        executor.submit_signal.assert_awaited_once()
    else:
        executor.submit_signal.assert_not_awaited()


def test_full_tick_cannot_override_a_preexisting_signal_engine_risk_veto(monkeypatch) -> None:
    from unittest.mock import AsyncMock, MagicMock, patch

    from test_orchestrator_coverage import _make_executor, _make_orch, _make_storage

    from src.engine.signal_engine import SignalResult

    monkeypatch.setenv("INTEL_ENABLED", "true")
    orch = _make_orch()
    executor = _make_executor()
    executor.submit_signal = AsyncMock(return_value=("trade-1", "opened"))
    orch._executor = executor
    orch._storage = _make_storage()
    orch._storage.latest_close = AsyncMock(return_value=None)
    orch._crypto_box = SimpleNamespace(enabled=False)
    orch._tick_counts = {Timeframe.INTRADAY.value: 0}
    orch._last_tick_ts = {Timeframe.INTRADAY.value: 0.0}
    orch._intelligence_adapter = _orchestrator("BUY")._intelligence_adapter

    engine = MagicMock()
    engine.tick = AsyncMock(
        return_value=SignalResult(
            tradeable=False,
            direction=1,
            p_long=0.8,
            p_bet=0.0,
            kelly_result=None,
            regime=None,
            gate_result=SimpleNamespace(passed=False, reason="daily_loss_limit"),
            skip_reason="daily_loss_limit",
        )
    )
    orch._engines = {Timeframe.INTRADAY.value: engine}

    with (
        patch("src.engine.orchestrator.compute_win_loss_stats", return_value=(0, 0.0, 0.0, 0.0)),
        patch("src.engine.orchestrator.update_metrics"),
    ):
        asyncio.run(orch._tick(Timeframe.INTRADAY))

    engine.tick.assert_awaited_once()
    executor.submit_signal.assert_not_awaited()
