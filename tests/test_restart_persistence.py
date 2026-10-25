"""
Restart persistence (EXR-009, EXR-010, EXR-013).

Decides:
  - REG-1050 -- open positions are rebuilt from storage on restart
  - REG-1051 -- the daily drawdown baseline and peak survive a restart
  - REG-1052 -- capital-floor halt and strategy kill switches survive a restart
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import tempfile
import time
from collections import OrderedDict
from unittest.mock import AsyncMock

import pytest
import structlog

from src.data.storage import EquityRecord, StorageBackend, TradeRecord
from src.execution.live import LiveExecutor
from src.execution.paper import PaperExecutor
from src.risk.capital_preservation_floor import CapitalPreservationFloor
from src.risk.performance_drift import PerformanceBaseline
from src.risk.state_persistence import state_file
from src.risk.strategy_kill_switch import StrategyKillSwitchManager

_NOW_MS = int(time.time() * 1000)


@pytest.fixture
async def storage():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.remove(path)
    sb = StorageBackend(db_path=path)
    await sb.initialize()
    yield sb
    await sb.close()
    for ext in ("", "-wal", "-shm"):
        with contextlib.suppress(FileNotFoundError):
            os.remove(path + ext)


def _equity(mode: str, ts: int, equity: float, cash: float, peak: float) -> EquityRecord:
    return EquityRecord(
        ts=ts,
        trading_mode=mode,
        equity_usd=equity,
        cash_usd=cash,
        unrealized_pnl=0.0,
        daily_pnl_usd=0.0,
        daily_pnl_pct=0.0,
        peak_equity_usd=peak,
        drawdown_pct=0.0,
    )


def _open_trade(mode: str, trade_id: str = "t-open") -> TradeRecord:
    return TradeRecord(
        id=trade_id,
        symbol="BTC/USDT",
        timeframe="15m",
        trading_mode=mode,
        execution_mode="automatic",
        direction=1,
        entry_price=100.0,
        exit_price=None,
        quantity=5.0,
        notional_usd=500.0,
        entry_ts=_NOW_MS - 1000,
        exit_ts=None,
        pnl_usd=None,
        pnl_pct=None,
        fee_usd=0.5,
        kelly_fraction=0.1,
        regime_at_entry=1,
        meta_label_prob=0.6,
        exit_reason=None,
        approved_by="auto",
        raw_signal=0.5,
    )


class TestPaperRestart:
    async def test_open_positions_rebuilt(self, storage) -> None:
        """Catches EXR-009: a restart left _positions empty, so open trades
        were never marked or closed and equity stayed understated."""
        await storage.insert_equity(_equity("paper", _NOW_MS, 10_000.0, 9_500.0, 10_000.0))
        await storage.insert_trade(_open_trade("paper"))
        ex = PaperExecutor(storage, starting_capital=10_000.0)
        await ex.initialize()
        assert set(ex._positions) == {"t-open"}
        assert ex._positions["t-open"].quantity == 5.0

    async def test_closed_trades_not_rebuilt(self, storage) -> None:
        """Negative case: only trades with exit_ts NULL come back."""
        await storage.insert_equity(_equity("paper", _NOW_MS, 10_000.0, 10_000.0, 10_000.0))
        ex = PaperExecutor(storage, starting_capital=10_000.0)
        await ex.initialize()
        assert ex._positions == {}

    async def test_daily_baseline_and_peak_restored(self, storage) -> None:
        """Catches EXR-010: after restart daily_start was the configured
        starting capital, so a loss on an account up 50% showed positive PnL."""
        await storage.insert_equity(_equity("paper", _NOW_MS - 10, 15_000.0, 15_000.0, 16_000.0))
        await storage.insert_equity(_equity("paper", _NOW_MS, 12_000.0, 12_000.0, 16_000.0))
        ex = PaperExecutor(storage, starting_capital=10_000.0)
        await ex.initialize()
        tracker = ex.drawdown_tracker
        assert tracker.daily_pnl_usd < 0.0
        assert tracker.daily_pnl_usd == pytest.approx(-3_000.0)
        assert tracker.drawdown_from_peak_pct == pytest.approx(-25.0)


class TestLiveRestart:
    @staticmethod
    def _executor(storage) -> LiveExecutor:
        ex = object.__new__(LiveExecutor)
        ex._storage = storage
        ex._starting_capital = 10_000.0
        ex._cash = 10_000.0
        ex._peak_equity = 10_000.0
        ex._positions = {}
        ex._order_fsm_registry = OrderedDict()
        ex._reconcile_with_exchange = AsyncMock()
        ex._log = structlog.get_logger("t")
        ex._initialized = False
        ex._lock = asyncio.Lock()
        return ex

    async def test_positions_and_baseline_restored(self, storage) -> None:
        """Catches EXR-009 and EXR-010 in the live executor."""
        await storage.insert_equity(_equity("live", _NOW_MS, 12_000.0, 11_500.0, 16_000.0))
        await storage.insert_trade(_open_trade("live"))
        ex = self._executor(storage)
        await ex.initialize()
        assert set(ex._positions) == {"t-open"}
        ex._reconcile_with_exchange.assert_awaited_once()
        assert ex._drawdown_tracker.drawdown_from_peak_pct == pytest.approx(-25.0)
        assert ex._drawdown_tracker.daily_pnl_usd == pytest.approx(0.0)


class TestFloorRestart:
    def test_halt_survives_restart(self) -> None:
        """Catches EXR-013: a restart silently cleared the whole-book halt."""
        path = state_file("floor_test")
        first = CapitalPreservationFloor(0.30, state_path=path)
        first.update_equity(1000.0)
        assert first.update_equity(600.0) is False
        second = CapitalPreservationFloor(0.30, state_path=path)
        assert second.is_halted
        assert second.update_equity(1000.0) is False

    def test_peak_survives_restart(self) -> None:
        """Peak restarted from 0, so drawdown from the old peak was invisible."""
        path = state_file("floor_peak")
        CapitalPreservationFloor(0.30, state_path=path).update_equity(1000.0)
        second = CapitalPreservationFloor(0.30, state_path=path)
        assert second.update_equity(600.0) is False

    def test_reauthorize_survives_restart(self) -> None:
        """Negative case: an explicit re-authorization is also durable."""
        path = state_file("floor_reauth")
        first = CapitalPreservationFloor(0.30, state_path=path)
        first.update_equity(1000.0)
        first.update_equity(600.0)
        first.re_authorize("op", "reviewed", 1)
        second = CapitalPreservationFloor(0.30, state_path=path)
        assert not second.is_halted
        assert second.last_reauthorization is not None

    def test_corrupt_file_fails_closed(self) -> None:
        """An unreadable state file cannot rule out a halt."""
        path = state_file("floor_corrupt")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{not json", encoding="utf-8")
        assert CapitalPreservationFloor(0.30, state_path=path).is_halted

    def test_no_file_starts_clean(self) -> None:
        assert not CapitalPreservationFloor(0.30, state_path=state_file("floor_new")).is_halted


def _baseline() -> PerformanceBaseline:
    return PerformanceBaseline(
        train_sharpe=2.5,
        oos_sharpe=2.0,
        train_accuracy=0.58,
        oos_accuracy=0.55,
        train_win_rate=0.54,
        max_drawdown_pct=0.10,
        trades_in_backtest=500,
    )


class TestKillSwitchRestart:
    def test_disabled_strategy_stays_disabled(self) -> None:
        """Catches EXR-013: disabled strategies came back enabled."""
        path = state_file("ks")
        a = StrategyKillSwitchManager()
        a.enable_persistence(path)
        a.register_strategy("s1", _baseline())
        a.register_strategy("s2", _baseline())
        a.disable("s1", "drift")
        b = StrategyKillSwitchManager()
        b.enable_persistence(path)
        b.register_strategy("s1", _baseline())
        b.register_strategy("s2", _baseline())
        assert not b.is_enabled("s1")
        assert b.is_enabled("s2")
        assert b.disabled_reason("s1") == "drift"

    def test_re_enable_is_durable(self) -> None:
        path = state_file("ks2")
        a = StrategyKillSwitchManager()
        a.enable_persistence(path)
        a.register_strategy("s1", _baseline())
        a.disable("s1", "drift")
        a.re_enable("s1", force=True)
        b = StrategyKillSwitchManager()
        b.enable_persistence(path)
        b.register_strategy("s1", _baseline())
        assert b.is_enabled("s1")

    def test_corrupt_file_disables_all(self) -> None:
        path = state_file("ks3")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("garbage", encoding="utf-8")
        m = StrategyKillSwitchManager()
        m.enable_persistence(path)
        m.register_strategy("s1", _baseline())
        assert not m.is_enabled("s1")


