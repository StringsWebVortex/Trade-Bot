"""Tests for the v5 spot-perp basis trade strategy.

REG-1704 (STR-21): the entry hurdle is the measured four-leg round trip on the
raw gap, and the strategy abstains without a measured cost.
"""

from __future__ import annotations

import pytest

from src.risk.execution_cost import ExecutionCost
from src.strategies.basis_trade import (
    BasisTradeContext,
    BasisTradeStrategy,
    compute_annualized_basis_pct,
    raw_basis_bps,
)
from src.strategies.registry import StrategyRegistry

# 6 bps a leg: 4.5 fee + 1.0 half-spread + 0.5 impact. Hurdle ~27.3 bps.
_COST = ExecutionCost(fee_bps=4.5, half_spread_bps=1.0, impact_bps=0.5, uncertainty_bps=1.0)


def _ctx(perp: float, days: float = 1.0, cost: ExecutionCost | None = _COST) -> BasisTradeContext:
    return BasisTradeContext(
        spot_price=100.0, perp_price=perp, days_to_perp_funding_normalization=days, cost=cost
    )


def test_compute_annualized_basis_pct_positive() -> None:
    pct = compute_annualized_basis_pct(spot_price=100.0, perp_price=100.05)
    assert pct > 0


def test_compute_annualized_basis_pct_rejects_nonpositive_spot() -> None:
    with pytest.raises(ValueError, match="spot_price"):
        compute_annualized_basis_pct(0.0, 100.0)


def test_compute_annualized_basis_pct_rejects_nonpositive_perp() -> None:
    with pytest.raises(ValueError, match="perp_price"):
        compute_annualized_basis_pct(100.0, 0.0)


def test_rejects_non_basistradecontext_bar() -> None:
    strat = BasisTradeStrategy()
    with pytest.raises(TypeError, match="BasisTradeContext"):
        strat.generate_signal(bar=None)


def test_registers_with_registry() -> None:
    registry = StrategyRegistry()
    registry.register(BasisTradeStrategy())
    assert "basis_trade_v1" in registry


def test_rejects_invalid_capital_fraction() -> None:
    with pytest.raises(ValueError, match="max_capital_fraction"):
        BasisTradeStrategy(max_capital_fraction=0.0)


def test_default_horizon_reproduces_the_historical_scale() -> None:
    # The horizon parameter must not change what this function has always
    # returned; it only makes the assumption explicit.
    assert compute_annualized_basis_pct(100.0, 100.05) == pytest.approx(18.25, abs=1e-6)


def test_horizon_divides_the_annualization() -> None:
    raw_gap_pct = 0.05
    assert compute_annualized_basis_pct(100.0, 100.05, 365.0) == pytest.approx(
        raw_gap_pct, abs=1e-9
    )
    assert compute_annualized_basis_pct(100.0, 100.05, 7.0) == pytest.approx(
        raw_gap_pct * 365.0 / 7.0, abs=1e-9
    )


def test_a_wider_horizon_shrinks_the_signal() -> None:
    near = compute_annualized_basis_pct(100.0, 100.05, 1.0)
    far = compute_annualized_basis_pct(100.0, 100.05, 30.0)
    assert 0.0 < far < near


def test_non_positive_horizon_is_rejected() -> None:
    # Not "instant convergence" — a division by zero wearing a plausible name.
    for bad in (0.0, -1.0):
        with pytest.raises(ValueError, match="days_to_convergence"):
            compute_annualized_basis_pct(100.0, 100.05, bad)


def test_raw_basis_bps_is_the_unannualised_gap() -> None:
    assert raw_basis_bps(100.0, 100.05) == pytest.approx(5.0)
    assert raw_basis_bps(100.0, 99.5) == pytest.approx(-50.0)


def test_flat_when_gap_below_the_measured_hurdle() -> None:
    assert BasisTradeStrategy().generate_signal(_ctx(100.001)).direction == 0


def test_shorts_perp_on_contango() -> None:
    sig = BasisTradeStrategy().generate_signal(_ctx(100.5))  # 50 bps
    assert sig.direction == -1
    assert sig.confidence > 0.0


def test_longs_perp_on_backwardation() -> None:
    assert BasisTradeStrategy().generate_signal(_ctx(99.5)).direction == 1


def test_a_routine_perp_premium_no_longer_clears_a_fixed_annualised_gate() -> None:
    """Before STR-21 a 1.37 bp gap cleared the fixed 5%-a-year threshold at the
    1-day horizon and traded, though four taker legs cost far more than that."""
    assert compute_annualized_basis_pct(100.0, 100.0137) > 5.0
    assert BasisTradeStrategy().generate_signal(_ctx(100.0137)).direction == 0


def test_abstains_without_a_measured_cost() -> None:
    sig = BasisTradeStrategy().generate_signal(_ctx(101.0, cost=None))
    assert sig.direction == 0
    assert sig.confidence == 0.0


def test_the_same_gap_trades_or_not_on_the_measured_cost() -> None:
    cheap = ExecutionCost(fee_bps=1.0, half_spread_bps=0.5, impact_bps=0.5, uncertainty_bps=0.5)
    dear = ExecutionCost(fee_bps=10.0, half_spread_bps=1.0, impact_bps=1.0, uncertainty_bps=1.0)
    strat = BasisTradeStrategy()
    assert strat.generate_signal(_ctx(100.3, cost=cheap)).direction == -1
    assert strat.generate_signal(_ctx(100.3, cost=dear)).direction == 0


def test_the_horizon_does_not_move_the_entry_decision() -> None:
    """Convergence captures the raw gap whenever it happens; only cost decides."""
    strat = BasisTradeStrategy()
    near = strat.generate_signal(_ctx(100.5, days=1.0))
    far = strat.generate_signal(_ctx(100.5, days=365.0))
    assert near == far


def test_bad_prices_still_raise_without_a_cost() -> None:
    with pytest.raises(ValueError, match="perp_price"):
        BasisTradeStrategy().generate_signal(_ctx(0.0, cost=None))
