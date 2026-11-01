"""
REG-1715: the orchestrator fills PortfolioInputs.execution_cost from
measurements only.

The basis, funding-carry and cross-exchange families size their entry hurdle
from the measured per-leg cost and abstain while it is None (REG-1704). The
orchestrator never filled it, so those families could never trade. These
tests pin the wiring: fee from the account's own closed trades, half-spread
from the live order book, impact from SlippageModel for the representative
order, and None whenever any of those cannot be measured.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import pytest
import structlog
from conftest import settings_double

from src.config import StrategyPortfolioSettings, Timeframe, TradingMode
from src.engine.orchestrator import _COST_FEE_TTL_S, Orchestrator
from src.engine.strategy_portfolio import required_inputs
from src.risk.execution_cost import closed_trade_fills
from src.risk.slippage import SlippageModel

_COST_NEEDS = required_inputs(["basis_trade_v1"])


@dataclass
class _Trade:
    entry_price: float
    exit_price: float | None
    quantity: float
    fee_usd: float


# 10 bps on each leg of a 100 USD round trip: 0.10 in, 0.10 out.
_CLOSED = _Trade(entry_price=100.0, exit_price=100.0, quantity=1.0, fee_usd=0.2)


class _Bar:
    def __init__(self) -> None:
        self.close = self.high = self.low = 100.0
        self.volume = 10.0


class _Storage:
    def __init__(self, trades: list[_Trade], bars: int = 30) -> None:
        self.trades = trades
        self.bars = [_Bar() for _ in range(bars)]
        self.trade_calls: list[str] = []
        self.fail = False

    async def fetch_bars(self, symbol, timeframe, since_ts=0, limit=0):
        return self.bars

    async def fetch_trades(self, symbol=None, trading_mode=None, limit=500, **_):
        self.trade_calls.append(trading_mode)
        if self.fail:
            raise RuntimeError("db down")
        return self.trades[:limit]


@dataclass
class _Book:
    bid_price: float
    ask_price: float


class _Fetcher:
    def __init__(self, book: object) -> None:
        self.book = book

    async def fetch_orderbook(self, symbol: str):
        if isinstance(self.book, Exception):
            raise self.book
        return self.book


@dataclass
class _Executor:
    equity_usd: float


def _orch(storage: _Storage, book: object = None, equity: float = 10_000.0) -> Orchestrator:
    orch = object.__new__(Orchestrator)
    orch._log = structlog.get_logger().bind(component="orchestrator_test")
    cfg = settings_double()
    cfg.trading_mode = TradingMode.PAPER
    cfg.strategy_portfolio = StrategyPortfolioSettings(cross_exchange_arb_fraction=0.3)
    orch._cfg = cfg
    orch._storage = storage
    orch._symbol = "BTC/USDT"
    orch._fetcher = _Fetcher(_Book(99.99, 100.01) if book is None else book)
    orch._quote_cache = {}
    orch._fee_cache = {}
    orch._primary_tf = Timeframe.INTRADAY
    orch._executor = _Executor(equity)
    orch._non_primary_executor = None
    return orch


async def test_execution_cost_is_built_from_the_measured_components():
    storage = _Storage([_CLOSED] * 20)
    inputs = await _orch(storage)._build_portfolio_inputs(Timeframe.INTRADAY, _COST_NEEDS)

    cost = inputs.execution_cost
    assert cost is not None
    assert cost.fee_bps == pytest.approx(10.0)
    # 99.99/100.01: 2 bps quoted width, 1 bp from mid to the touch.
    assert cost.half_spread_bps == pytest.approx(1.0)
    # Largest cost-family fraction (0.3) of equity at the mid, against the
    # daily volume of 20 completed 15m bars of 10 units (96 bars a day).
    expected = SlippageModel().estimate(
        symbol="BTC/USDT", qty=10_000.0 * 0.3 / 100.0, price=100.0, adv_20d=960.0, spread_bps=1.0
    )
    assert cost.impact_bps == pytest.approx(expected.impact_bps)
    # Constant fees and no slippage-error calibration: no measured spread.
    assert cost.uncertainty_bps == 0.0
    assert storage.trade_calls == [TradingMode.PAPER.value]


@pytest.mark.parametrize(
    ("trades", "bars", "book", "equity"),
    [
        pytest.param([_CLOSED] * 19, 30, None, 10_000.0, id="too_few_closed_trades"),
        pytest.param(
            [_CLOSED] * 19 + [_Trade(100.0, None, 1.0, 0.1)], 30, None, 10_000.0, id="open_trade"
        ),
        pytest.param([_CLOSED] * 20, 20, None, 10_000.0, id="too_few_bars"),
        pytest.param([_CLOSED] * 20, 30, _Book(0.0, 100.0), 10_000.0, id="one_sided_book"),
        pytest.param([_CLOSED] * 20, 30, _Book(100.1, 100.0), 10_000.0, id="crossed_book"),
        pytest.param([_CLOSED] * 20, 30, RuntimeError("book down"), 10_000.0, id="book_down"),
        pytest.param([_CLOSED] * 20, 30, None, 0.0, id="no_equity"),
    ],
)
async def test_an_unmeasured_component_leaves_the_cost_unknown(trades, bars, book, equity):
    orch = _orch(_Storage(trades, bars=bars), book=book, equity=equity)
    inputs = await orch._build_portfolio_inputs(Timeframe.INTRADAY, _COST_NEEDS)
    assert inputs.execution_cost is None


async def test_a_timeframe_with_no_executor_has_no_cost():
    orch = _orch(_Storage([_CLOSED] * 20))
    orch._executor = None
    inputs = await orch._build_portfolio_inputs(Timeframe.INTRADAY, _COST_NEEDS)
    assert inputs.execution_cost is None


async def test_the_cost_is_not_measured_unless_a_cost_family_needs_it():
    storage = _Storage([_CLOSED] * 20)
    inputs = await _orch(storage)._build_portfolio_inputs(
        Timeframe.INTRADAY, required_inputs(["breakout_volume_v1"])
    )
    assert inputs.execution_cost is None
    assert storage.trade_calls == []


async def test_the_fee_is_read_once_per_ttl_window():
    storage = _Storage([_CLOSED] * 20)
    orch = _orch(storage)
    await orch._build_portfolio_inputs(Timeframe.INTRADAY, _COST_NEEDS)
    await orch._build_portfolio_inputs(Timeframe.INTRADAY, _COST_NEEDS)
    assert len(storage.trade_calls) == 1

    # Age the entry past its TTL rather than sleeping.
    mode = TradingMode.PAPER.value
    _, fee = orch._fee_cache[mode]
    orch._fee_cache[mode] = (time.monotonic() - _COST_FEE_TTL_S - 1.0, fee)
    await orch._build_portfolio_inputs(Timeframe.INTRADAY, _COST_NEEDS)
    assert len(storage.trade_calls) == 2


async def test_a_failed_trade_read_is_not_cached():
    storage = _Storage([_CLOSED] * 20)
    storage.fail = True
    orch = _orch(storage)
    first = await orch._build_portfolio_inputs(Timeframe.INTRADAY, _COST_NEEDS)
    assert first.execution_cost is None

    storage.fail = False
    second = await orch._build_portfolio_inputs(Timeframe.INTRADAY, _COST_NEEDS)
    assert second.execution_cost is not None


@pytest.mark.parametrize(
    ("trade", "expected"),
    [
        pytest.param(_Trade(100.0, 110.0, 2.0, 0.42), [(420.0, 0.42)], id="both_legs_notional"),
        pytest.param(_Trade(100.0, None, 1.0, 0.1), [], id="open"),
        pytest.param(_Trade(100.0, 100.0, 0.0, 0.2), [], id="zero_quantity"),
        pytest.param(_Trade(0.0, 100.0, 1.0, 0.2), [], id="zero_entry"),
        pytest.param(_Trade(100.0, 100.0, 1.0, float("nan")), [], id="nan_fee"),
        pytest.param(_Trade(100.0, float("inf"), 1.0, 0.2), [], id="inf_exit"),
        pytest.param(_Trade(100.0, 100.0, 1.0, -0.02), [(200.0, -0.02)], id="rebate_kept"),
    ],
)
def test_closed_trade_fills(trade, expected):
    assert closed_trade_fills([trade]) == expected
