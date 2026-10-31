"""
EXR-004, EXR-005, EXR-011, AGT-011 (+AGT-010 doc honesty) regressions.

Each test fails on the pre-fix code:
 * drift accuracy scored a placeholder 0.5 so every long was a wrong call;
 * the baseline was invented from getattr defaults;
 * NaN inputs passed the cognitive validators and the halt triggers.

Decides:
  - REG-1060 — Drift accuracy uses the real entry P(long); unknown is skipped
  - REG-1061 — Drift and kill-switch baseline is built only from measured CPCV metrics
  - REG-1062 — Cognitive engine vetoes non-finite inputs
  - REG-1063 — Halt triggers fire on non-finite readings
"""

from __future__ import annotations

import math
from types import SimpleNamespace

import pytest

from src.config import invalidate_settings_cache
from src.diagnostics import halt_triggers
from src.diagnostics.halt_triggers import evaluate
from src.engine.orchestrator import baseline_from_training
from src.risk.cognitive_engine import CognitiveEngine, SignalContext
from src.risk.performance_drift import PerformanceBaseline, PerformanceDriftDetector

HEALTHY = {
    "market_data_age_s": 5.0,
    "position_deviation": 0.0,
    "reconciliation_ok": True,
    "risk_engine_ok": True,
    "consecutive_order_failures": 0,
    "auth_failures": 0,
    "drawdown_fraction": 0.03,
    "audit_log_ok": True,
    "clock_skew_s": 0.4,
}


def _detector() -> PerformanceDriftDetector:
    return PerformanceDriftDetector(PerformanceBaseline(1.0, 1.0, 0.6, 0.6, 0.55, 0.1, 100))


def _record(det, n, prob, direction=1):
    for _ in range(n):
        det.record_trade_outcome(
            pnl_usd=10.0,
            predicted_prob=prob,
            actual_direction=direction,
            current_equity=10_000.0,
            starting_equity=10_000.0,
        )


def test_real_entry_prob_scores_longs_correct():
    det = _detector()
    _record(det, 5, 0.7, 1)
    assert [ok for _, ok in det._live_predictions] == [1] * 5


def test_unknown_prob_skips_accuracy_sample():
    """None must not be booked as a wrong long prediction (EXR-004)."""
    det = _detector()
    _record(det, 5, None, 1)
    assert len(det._live_predictions) == 0


def test_nan_prob_skips_accuracy_sample():
    det = _detector()
    _record(det, 3, float("nan"), 1)
    assert len(det._live_predictions) == 0


def _result(**kw):
    base = {"oos_sharpe": 1.2, "accuracy": 0.57, "max_drawdown": 8.0, "n_trades": 300}
    base.update(kw)
    return SimpleNamespace(**base)


def test_baseline_comes_from_measured_metrics():
    b = baseline_from_training(_result())
    assert b is not None
    assert (b.oos_sharpe, b.oos_accuracy, b.trades_in_backtest) == (1.2, 0.57, 300)
    assert b.max_drawdown_pct == pytest.approx(0.08)


@pytest.mark.parametrize(
    "res",
    [
        None,
        object(),
        _result(oos_sharpe=float("nan")),
        _result(accuracy=float("inf")),
        _result(n_trades=0),
        _result(max_drawdown=100.0 * 5),
    ],
)
def test_missing_or_invalid_metrics_give_no_baseline(res):
    assert baseline_from_training(res) is None


def _ctx(**over) -> SignalContext:
    base = {
        "signal_id": "BTCUSDT_1h_1750000000000",
        "symbol": "BTC/USDT",
        "timeframe": "1h",
        "p_long": 0.7,
        "p_bet": 0.71,
        "expected_edge_bps": 40.0,
        "regime_state": 1,
        "regime_probs": [0.15, 0.75, 0.10],
        "hurst_exponent": 0.62,
        "current_price": 65000.0,
        "atr": 300.0,
        "atr_median_20": 290.0,
        "realized_vol": 0.45,
        "adv_20d": 50_000.0,
        "spread_bps": 2.0,
        "capital_usd": 100_000.0,
        "daily_pnl_usd": 200.0,
        "open_positions": 0,
        "consecutive_losses": 0,
        "funding_rate_8h": 0.0,
        "basis_pct": 0.0,
        "exchange_name": "binance",
        "proposed_qty": 0.01,
        "proposed_notional_usd": 650.0,
        "kelly_adjusted_fraction": 0.0784,
    }
    base.update(over)
    return SignalContext(**base)


@pytest.fixture(autouse=True)
def _settings():
    invalidate_settings_cache()
    yield
    invalidate_settings_cache()


@pytest.mark.parametrize(
    "over",
    [
        {"realized_vol": float("nan")},
        {"p_bet": float("nan")},
        {"hurst_exponent": float("nan")},
        {"atr": float("nan")},
        {"regime_probs": [0.2, float("nan"), 0.3]},
        {"capital_usd": float("inf")},
    ],
)
def test_cognitive_engine_vetoes_non_finite_input(over):
    d = CognitiveEngine().evaluate(_ctx(**over))
    assert d.passed is False
    assert d.adjusted_size_fraction == 0.0
    assert "non-finite" in (d.veto_reason or "")


def test_cognitive_engine_still_passes_clean_context():
    assert CognitiveEngine().evaluate(_ctx()).passed is True


@pytest.mark.parametrize(
    "key", ["market_data_age_s", "position_deviation", "drawdown_fraction", "clock_skew_s"]
)
@pytest.mark.parametrize("bad", [math.nan, math.inf])
def test_halt_triggers_fire_on_non_finite(key, bad):
    assert not evaluate(HEALTHY).should_halt
    assert evaluate({**HEALTHY, key: bad}).should_halt


def test_halt_trigger_docs_do_not_claim_live_enforcement():
    """AGT-010: module says plainly it is not wired into src/."""
    assert "NOT enforced in the live path" in (halt_triggers.__doc__ or "")
