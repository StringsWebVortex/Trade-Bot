"""
REG-1716 (EXR-029): an open loss counts against the 2% daily-drawdown halt.

The halt was fed today's realised PnL only, so an unrealised loss of any size
never tripped it until the position closed. The tick now passes the worse of
realised PnL and the marked equity change since the daily reset.
"""

from __future__ import annotations

import math
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from test_orchestrator_extra_coverage import _make_executor, _make_orch, _make_skip_result

from src.config import RiskSettings, Timeframe
from src.risk.gates import GateStatus, check_daily_drawdown, stricter_daily_pnl


@pytest.mark.parametrize(
    ("realised", "marked", "expected"),
    [(0.0, -3_000.0, -3_000.0), (-2_500.0, 1_000.0, -2_500.0), (100.0, 50.0, 50.0)],
)
def test_the_worse_of_realised_and_marked_is_used(
    realised: float, marked: float, expected: float
) -> None:
    assert stricter_daily_pnl(realised, marked) == expected


@pytest.mark.parametrize(("realised", "marked"), [(math.nan, 0.0), (0.0, math.inf)])
def test_a_non_finite_input_halts(realised: float, marked: float) -> None:
    pnl = stricter_daily_pnl(realised, marked)
    assert math.isnan(pnl)
    assert check_daily_drawdown(pnl, 100_000.0, RiskSettings(_env_file=None)).status == (
        GateStatus.HALT_DRAWDOWN
    )


def test_an_open_three_percent_loss_halts_with_nothing_realised() -> None:
    cfg = settings_double().risk
    pnl = stricter_daily_pnl(0.0, -3_000.0)
    assert check_daily_drawdown(pnl, 100_000.0, cfg).status == GateStatus.HALT_DRAWDOWN
    # Realised-only, the old input, let it through.
    assert check_daily_drawdown(0.0, 100_000.0, cfg).passed


async def test_the_tick_passes_the_open_loss_to_the_engine() -> None:
    orch = _make_orch()
    executor = _make_executor()
    executor.equity_usd = 97_000.0  # 3% below the daily start, nothing closed
    orch._executor = executor
    orch._tick_counts = {Timeframe.INTRADAY.value: 0}
    orch._last_tick_ts = {Timeframe.INTRADAY.value: 0.0}
    orch._last_close_for_corr = {}
    engine = MagicMock()
    engine.tick = AsyncMock(return_value=_make_skip_result())
    orch._engines = {Timeframe.INTRADAY.value: engine}
    tracker = MagicMock()
    tracker.correlation_scalar = MagicMock(return_value=1.0)

    with (
        patch("src.engine.orchestrator.get_portfolio_correlation", return_value=tracker),
        patch("src.engine.orchestrator.compute_win_loss_stats", return_value=(0, 0.0, 0.0, 0.0)),
    ):
        await orch._tick(Timeframe.INTRADAY)

    kwargs = engine.tick.await_args.kwargs
    assert kwargs["daily_pnl_usd"] == pytest.approx(-3_000.0)
    assert kwargs["starting_equity_usd"] == 100_000.0
