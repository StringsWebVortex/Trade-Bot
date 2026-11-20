"""Tests for the funding-rate carry strategy (v2 Sub-task 2, family 2).

REG-1704 (STR-21): the funding expected over the measured holding horizon must
beat the measured two-leg round trip; no measured cost or horizon, no trade.
"""

from __future__ import annotations

import math

import pytest

from src.risk.execution_cost import ExecutionCost
from src.strategies.funding_carry import FundingCarryStrategy, FundingContext
from src.strategies.registry import StrategyRegistry

# 6 bps a leg: 4.5 fee + 1.0 half-spread + 0.5 impact. Two-leg hurdle ~14.3 bps.
_COST = ExecutionCost(fee_bps=4.5, half_spread_bps=1.0, impact_bps=0.5, uncertainty_bps=1.0)


def test_rejects_non_fundingcontext_bar() -> None:
    strat = FundingCarryStrategy()
    with pytest.raises(TypeError, match="FundingContext"):
        strat.generate_signal(bar=None)


def _ctx(
    rate: float,
    z: float,
    periods: float | None = 10.0,
    cost: ExecutionCost | None = _COST,
) -> FundingContext:
    return FundingContext(
        funding_rate_pct=rate, funding_zscore=z, expected_periods=periods, cost=cost
    )


def test_flat_when_rate_and_zscore_small() -> None:
    sig = FundingCarryStrategy().generate_signal(_ctx(0.001, 0.2))
    assert sig.direction == 0
    assert sig.confidence == 0.0


def test_flat_when_zscore_stretched_but_carry_below_the_hurdle() -> None:
    # 0.1 bp a period for 10 periods is 1 bp, under a ~14.3 bp two-leg hurdle.
    assert FundingCarryStrategy().generate_signal(_ctx(0.001, 3.0)).direction == 0


def test_shorts_perp_on_stretched_positive_funding() -> None:
    sig = FundingCarryStrategy().generate_signal(_ctx(0.05, 2.5))
    assert sig.direction == -1
    assert sig.confidence > 0.0
    assert sig.regime_fit == pytest.approx(0.6)


def test_longs_perp_on_stretched_negative_funding() -> None:
    assert FundingCarryStrategy().generate_signal(_ctx(-0.05, -2.5)).direction == 1


def test_confidence_capped_at_one() -> None:
    assert FundingCarryStrategy().generate_signal(_ctx(0.5, 10.0)).confidence == 1.0


def test_abstains_without_a_measured_cost_or_horizon() -> None:
    strat = FundingCarryStrategy()
    assert strat.generate_signal(_ctx(0.5, 10.0, cost=None)).direction == 0
    assert strat.generate_signal(_ctx(0.5, 10.0, periods=None)).direction == 0
    assert strat.generate_signal(_ctx(0.5, 10.0, periods=0.0)).direction == 0
    assert strat.generate_signal(_ctx(0.5, 10.0, periods=math.nan)).direction == 0


def test_a_nan_zscore_abstains() -> None:
    assert FundingCarryStrategy().generate_signal(_ctx(0.5, math.nan)).direction == 0


def test_a_small_but_persistent_rate_can_pay_where_the_fixed_floor_refused() -> None:
    """STR-21: 0.008% sat under the old fixed 0.01% floor whatever it earned.
    Collected over 50 measured periods it is 40 bps, above the hurdle."""
    strat = FundingCarryStrategy()
    assert strat.generate_signal(_ctx(0.008, 2.0, periods=50.0)).direction == -1
    assert strat.generate_signal(_ctx(0.008, 2.0, periods=1.0)).direction == 0


def test_a_dearer_venue_needs_more_carry() -> None:
    dear = ExecutionCost(fee_bps=10.0, half_spread_bps=2.0, impact_bps=1.0, uncertainty_bps=1.0)
    strat = FundingCarryStrategy()
    assert strat.generate_signal(_ctx(0.02, 2.0)).direction == -1
    assert strat.generate_signal(_ctx(0.02, 2.0, cost=dear)).direction == 0


def test_registers_with_registry() -> None:
    registry = StrategyRegistry()
    registry.register(FundingCarryStrategy())
    assert "funding_carry_v1" in registry


def test_rejects_invalid_capital_fraction() -> None:
    with pytest.raises(ValueError, match="max_capital_fraction"):
        FundingCarryStrategy(max_capital_fraction=1.5)
    with pytest.raises(ValueError, match="max_capital_fraction"):
        FundingCarryStrategy(max_capital_fraction=0.0)
