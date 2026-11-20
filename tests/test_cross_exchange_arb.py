"""Tests for the v3 cross-exchange basis arbitrage strategy.

REG-1704 (STR-21): the entry hurdle is the measured four-leg round trip, and
the strategy abstains without a measured cost.
"""

from __future__ import annotations

import pytest

from src.risk.execution_cost import ExecutionCost
from src.strategies.cross_exchange_arb import (
    ROUND_TRIP_LEGS,
    CrossExchangeArbStrategy,
    CrossExchangeContext,
    compute_basis_bps,
)
from src.strategies.registry import StrategyRegistry

# 6 bps a leg: 4.5 fee + 1.0 half-spread + 0.5 impact. Hurdle ~27.3 bps.
_COST = ExecutionCost(fee_bps=4.5, half_spread_bps=1.0, impact_bps=0.5, uncertainty_bps=1.0)


def _ctx(
    price_a: float, price_b: float, cost: ExecutionCost | None = _COST
) -> CrossExchangeContext:
    return CrossExchangeContext("binance", price_a, "okx", price_b, cost=cost)


def test_compute_basis_bps_positive_spread() -> None:
    bps = compute_basis_bps(price_a=60100.0, price_b=60000.0)
    assert bps == pytest.approx((100.0 / 60000.0) * 10_000.0)


def test_compute_basis_bps_rejects_nonpositive_price_b() -> None:
    with pytest.raises(ValueError, match="price_b"):
        compute_basis_bps(100.0, 0.0)


def test_rejects_non_crossexchangecontext_bar() -> None:
    strat = CrossExchangeArbStrategy()
    with pytest.raises(TypeError, match="CrossExchangeContext"):
        strat.generate_signal(bar=None)


def test_flat_when_spread_below_the_measured_hurdle() -> None:
    sig = CrossExchangeArbStrategy().generate_signal(_ctx(60100.0, 60000.0))  # ~16.7 bps
    assert sig.direction == 0


def test_shorts_a_when_a_richer_than_b() -> None:
    sig = CrossExchangeArbStrategy().generate_signal(_ctx(60300.0, 60000.0))  # 50 bps
    assert sig.direction == -1
    assert sig.confidence > 0.0


def test_longs_a_when_a_cheaper_than_b() -> None:
    sig = CrossExchangeArbStrategy().generate_signal(_ctx(59700.0, 60000.0))
    assert sig.direction == 1


def test_confidence_capped_at_one() -> None:
    sig = CrossExchangeArbStrategy().generate_signal(_ctx(66000.0, 60000.0))
    assert sig.confidence == 1.0


def test_compute_basis_bps_rejects_nonpositive_price_a() -> None:
    with pytest.raises(ValueError, match="price_a"):
        compute_basis_bps(0.0, 100.0)


def test_abstains_without_a_measured_cost() -> None:
    """An unmeasured cost is not a zero cost: a wide spread still does not trade."""
    sig = CrossExchangeArbStrategy().generate_signal(_ctx(66000.0, 60000.0, cost=None))
    assert sig.direction == 0
    assert sig.confidence == 0.0


def test_the_same_spread_trades_or_not_on_the_measured_cost() -> None:
    """30 bps gross: clears a cheap venue pair's hurdle, not a dear one's."""
    cheap = ExecutionCost(fee_bps=1.0, half_spread_bps=0.5, impact_bps=0.5, uncertainty_bps=0.5)
    dear = ExecutionCost(fee_bps=10.0, half_spread_bps=1.0, impact_bps=1.0, uncertainty_bps=1.0)
    assert cheap.hurdle_bps(ROUND_TRIP_LEGS) < 30.0 < dear.hurdle_bps(ROUND_TRIP_LEGS)
    strat = CrossExchangeArbStrategy()
    assert strat.generate_signal(_ctx(60180.0, 60000.0, cost=cheap)).direction == -1
    assert strat.generate_signal(_ctx(60180.0, 60000.0, cost=dear)).direction == 0


def test_higher_cost_lowers_confidence_on_the_same_spread() -> None:
    cheap = ExecutionCost(fee_bps=1.0, half_spread_bps=0.5, impact_bps=0.0, uncertainty_bps=0.0)
    strat = CrossExchangeArbStrategy()
    low = strat.generate_signal(_ctx(60300.0, 60000.0, cost=cheap))
    high = strat.generate_signal(_ctx(60300.0, 60000.0))
    assert low.confidence > high.confidence > 0.0


def test_registers_with_registry() -> None:
    registry = StrategyRegistry()
    registry.register(CrossExchangeArbStrategy())
    assert "cross_exchange_arb_v1" in registry


def test_rejects_invalid_capital_fraction() -> None:
    with pytest.raises(ValueError, match="max_capital_fraction"):
        CrossExchangeArbStrategy(max_capital_fraction=0.0)
