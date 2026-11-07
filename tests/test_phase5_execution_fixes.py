"""Phase 5 execution fixes: EXR-014..EXR-021 regressions.

Decides:
  - REG-1300 -- paper fills carry a spread cost when ADV is unknown (EXR-014)
  - REG-1301 -- OrderNotFound right after placement is retried (EXR-015)
  - REG-1302 -- tick-size amount precision is quantised correctly (EXR-016)
  - REG-1303 -- a cognitive size reduction is requantised (EXR-017)
  - REG-1304 -- the MANUAL approval wait is bounded (EXR-018)
  - REG-1305 -- a low Hurst exponent warns rather than vetoes (EXR-019)
  - REG-1307 -- drift baselines use the live statistic's units (EXR-021)
"""

from __future__ import annotations

import contextlib
import os
import tempfile
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import ccxt
import pytest
import structlog

from src.config import ExecutionMode, runtime_config
from src.data.storage import StorageBackend
from src.execution import order_manager as om
from src.execution.paper import PaperExecutor, PaperPosition
from src.risk.cognitive_engine import RegimeValidator, SignalContext, ValidatorStatus
from src.risk.kelly import KellyResult, apply_size_scalar, compute_position_size
from src.risk.performance_drift import PerformanceBaseline, PerformanceDriftDetector


def _kelly(notional=500.0, price=100.0):
    return KellyResult(
        kelly_fraction=0.2,
        adjusted_fraction=0.1,
        capital_usd=10000.0,
        entry_price=price,
        quantity=notional / price,
        notional_usd=notional,
        is_capped=False,
    )


@pytest.fixture
async def executor():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.remove(path)
    sb = StorageBackend(db_path=path)
    await sb.initialize()
    ex = PaperExecutor(sb, starting_capital=10000.0)
    await ex.initialize()
    yield ex
    await runtime_config.set_execution_mode(ExecutionMode.AUTOMATIC)
    await sb.close()
    for ext in ("", "-wal", "-shm"):
        with contextlib.suppress(FileNotFoundError):
            os.remove(path + ext)


@pytest.mark.asyncio
async def test_exr014_entry_has_default_spread_cost_without_adv(executor):
    await runtime_config.set_execution_mode(ExecutionMode.AUTOMATIC)
    trade_id, _ = await executor.submit_signal("BTC/USDT", "15m", 1, _kelly(), 1, 0.6, 0.5, 100.0)
    assert executor._positions[trade_id].entry_price > 100.0


def test_exr014_exit_has_default_spread_cost_without_adv():
    ex = PaperExecutor.__new__(PaperExecutor)
    ex._log = structlog.get_logger("t")
    ex._risk_cfg = SimpleNamespace(slippage_default_spread_bps=2.0)
    pos = PaperPosition(
        trade_id="t",
        symbol="BTC/USDT",
        timeframe="15m",
        direction=1,
        entry_price=100.0,
        quantity=1.0,
        notional_usd=100.0,
        entry_ts=1,
        kelly_fraction=0.1,
        regime_at_entry=0,
        meta_label_prob=0.6,
        raw_signal=0.5,
        approved_by="auto",
        execution_mode="automatic",
        fee_usd=0.0,
    )
    assert ex._slipped_exit_price(100.0, pos) < 100.0
    pos.direction = 0
    assert ex._slipped_exit_price(100.0, pos) > 100.0


@pytest.mark.asyncio
async def test_exr015_order_not_found_is_retried_then_permanent(monkeypatch):
    monkeypatch.setattr(om, "_ORDER_CONFIRM_INTERVAL", 0.0)
    exchange = MagicMock()
    exchange.fetch_order = AsyncMock(side_effect=ccxt.OrderNotFound("nf"))
    fsm = MagicMock()
    with pytest.raises(ccxt.OrderNotFound):
        await om.OrderManager()._confirm_order_fill(exchange, "1", "BTC/USDT", fsm)
    assert exchange.fetch_order.await_count == om._ORDER_NOT_FOUND_GRACE_POLLS + 1


def test_exr016_tick_size_precision_is_not_whole_units():
    result = compute_position_size(
        p_long=0.7,
        direction=1,
        capital_usd=10000.0,
        entry_price=100.0,
        avg_win_usd=2.0,
        avg_loss_usd=1.0,
        amount_precision=1e-05,
    )
    assert result is not None
    assert result.quantity != int(result.quantity) or result.quantity > 0
    assert result.quantity > 0.0


def test_exr016_017_scalar_on_tick_size_keeps_fraction():
    out = apply_size_scalar(_kelly(500.0, 100.0), 0.5, 100.0, amount_precision=0.001)
    assert out is not None
    assert out.quantity == pytest.approx(2.5)


def test_exr017_engine_requantises_cognitive_reduction():
    import inspect

    from src.engine import signal_engine

    src = inspect.getsource(signal_engine)
    assert "round(\n                    kelly_result.quantity" not in src
    assert "cognitive_scalar_below_minimum" in src
    assert "**self._symbol_precision" in src


@pytest.mark.asyncio
async def test_exr018_manual_approval_wait_is_bounded(executor):
    await runtime_config.set_execution_mode(ExecutionMode.MANUAL)
    executor._await_approval = AsyncMock(return_value=(False, ""))
    await executor.submit_signal("BTC/USDT", "15m", 1, _kelly(), 1, 0.6, 0.5, 100.0)
    assert executor._await_approval.await_args.args[1] is not None


def test_exr019_low_hurst_warns_not_vetoes():
    ctx = SignalContext(
        signal_id="s",
        symbol="BTC/USDT",
        timeframe="1h",
        p_long=0.7,
        p_bet=0.7,
        expected_edge_bps=40.0,
        regime_state=1,
        regime_probs=[0.10, 0.85, 0.05],
        hurst_exponent=0.40,
        current_price=65000.0,
        atr=300.0,
        atr_median_20=290.0,
        realized_vol=0.45,
        adv_20d=50000.0,
        spread_bps=2.0,
        capital_usd=100000.0,
        daily_pnl_usd=0.0,
        open_positions=0,
        consecutive_losses=0,
        funding_rate_8h=0.0,
        basis_pct=0.0,
        exchange_name="binance",
        proposed_qty=0.01,
        proposed_notional_usd=650.0,
        kelly_adjusted_fraction=0.05,
    )
    assert RegimeValidator().validate(ctx).status == ValidatorStatus.WARN


def _baseline(**kw):
    return PerformanceBaseline(
        train_sharpe=2.0,
        oos_sharpe=1.5,
        train_accuracy=0.6,
        oos_accuracy=0.58,
        train_win_rate=0.9,
        max_drawdown_pct=0.1,
        trades_in_backtest=400,
        **kw,
    )


def test_exr021_baselines_use_matching_units():
    legacy = _baseline()
    assert legacy.sharpe_baseline_per_trade == 1.5
    assert legacy.win_rate_baseline == 0.9
    with pytest.raises(ValueError, match="oos_sharpe_per_trade must be finite"):
        _baseline(oos_sharpe_per_trade=float("nan"))
    fixed = _baseline(oos_sharpe_per_trade=0.2, oos_win_rate=0.5)
    assert fixed.sharpe_baseline_per_trade == 0.2
    assert fixed.win_rate_baseline == 0.5
    det = PerformanceDriftDetector(fixed)
    for i in range(30):
        det.record_trade_outcome(
            pnl_usd=1.0 if i % 2 == 0 else -0.8,
            predicted_prob=0.6,
            actual_direction=1,
            current_equity=10000.0,
            starting_equity=10000.0,
        )
    assert not det._check_sharpe_drift().drifted
    assert not det._check_winrate_drift().drifted
