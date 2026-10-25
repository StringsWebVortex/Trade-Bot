"""
REG-1704 (STR-21): the entry hurdle is built from measured cost, never a fixed figure.

src/risk/execution_cost.py turns the account's own fills (fee), the live book
(half-spread) and the calibrated impact model into a per-leg cost, and a
round-trip hurdle with a margin for how much that cost varies. An unmeasured
fee is reported unknown, not zero.
"""

from __future__ import annotations

import math

import pytest

from src.risk.execution_cost import (
    HURDLE_Z,
    MIN_FEE_SAMPLES,
    ExecutionCost,
    FeeMeasurement,
    edge_confidence,
    measure_fee_bps,
)


def _fills(rate_bps: float, n: int, notional: float = 1_000.0) -> list[tuple[float, float]]:
    return [(notional, notional * rate_bps / 10_000.0)] * n


def test_fee_is_measured_from_the_accounts_fills() -> None:
    fills = _fills(10.0, 10) + _fills(4.0, 10, notional=5_000.0)
    fee = measure_fee_bps(fills)
    assert fee is not None
    assert fee.samples == 20
    assert fee.mean_bps == pytest.approx(7.0)
    assert fee.std_bps == pytest.approx(math.sqrt(9.0 * 20 / 19))


def test_too_few_fills_is_unknown_not_zero() -> None:
    assert measure_fee_bps(_fills(10.0, MIN_FEE_SAMPLES - 1)) is None
    assert measure_fee_bps([]) is None


def test_fills_that_are_not_fills_are_skipped() -> None:
    junk = [(0.0, 1.0), (-5.0, 1.0), (math.nan, 1.0), (100.0, math.inf)]
    assert measure_fee_bps(junk + _fills(5.0, MIN_FEE_SAMPLES - 1)) is None
    fee = measure_fee_bps(junk + _fills(5.0, MIN_FEE_SAMPLES))
    assert fee is not None and fee.samples == MIN_FEE_SAMPLES


def test_a_maker_rebate_is_kept_as_a_negative_fee() -> None:
    fee = measure_fee_bps(_fills(-1.0, MIN_FEE_SAMPLES))
    assert fee is not None
    assert fee.mean_bps == pytest.approx(-1.0)


def test_round_trip_and_hurdle_scale_with_the_measured_cost() -> None:
    cost = ExecutionCost(fee_bps=4.5, half_spread_bps=1.0, impact_bps=0.5, uncertainty_bps=1.0)
    assert cost.per_leg_bps == pytest.approx(6.0)
    assert cost.round_trip_bps(4) == pytest.approx(24.0)
    assert cost.hurdle_bps(4) == pytest.approx(24.0 + HURDLE_Z * 2.0)
    dearer = ExecutionCost(fee_bps=10.0, half_spread_bps=1.0, impact_bps=0.5, uncertainty_bps=1.0)
    assert dearer.hurdle_bps(4) > cost.hurdle_bps(4)


def test_from_measurements_adds_the_noise_in_quadrature() -> None:
    fee = FeeMeasurement(mean_bps=4.0, std_bps=3.0, samples=30)
    cost = ExecutionCost.from_measurements(
        fee, half_spread_bps=1.0, impact_bps=2.0, slippage_error_std_bps=4.0
    )
    assert cost.fee_bps == pytest.approx(4.0)
    assert cost.uncertainty_bps == pytest.approx(5.0)


@pytest.mark.parametrize("field", ["fee_bps", "half_spread_bps", "impact_bps", "uncertainty_bps"])
def test_a_non_finite_cost_is_rejected(field: str) -> None:
    values = {"fee_bps": 1.0, "half_spread_bps": 1.0, "impact_bps": 1.0, "uncertainty_bps": 1.0}
    values[field] = math.nan
    with pytest.raises(ValueError, match=field):
        ExecutionCost(**values)


@pytest.mark.parametrize("field", ["half_spread_bps", "impact_bps", "uncertainty_bps"])
def test_a_negative_spread_impact_or_uncertainty_is_rejected(field: str) -> None:
    values = {"fee_bps": 1.0, "half_spread_bps": 1.0, "impact_bps": 1.0, "uncertainty_bps": 1.0}
    values[field] = -0.1
    with pytest.raises(ValueError, match=field):
        ExecutionCost(**values)


def test_invalid_legs_and_z_are_rejected() -> None:
    cost = ExecutionCost(fee_bps=1.0, half_spread_bps=1.0, impact_bps=1.0, uncertainty_bps=1.0)
    with pytest.raises(ValueError, match="legs"):
        cost.hurdle_bps(0)
    with pytest.raises(ValueError, match="z"):
        cost.hurdle_bps(2, z=-1.0)
    with pytest.raises(ValueError, match="min_samples"):
        measure_fee_bps([], min_samples=1)


def test_edge_confidence_is_relative_to_the_hurdle() -> None:
    assert edge_confidence(10.0, 10.0) == 0.0
    assert edge_confidence(15.0, 10.0) == pytest.approx(0.5)
    assert edge_confidence(40.0, 10.0) == 1.0
    assert edge_confidence(math.nan, 10.0) == 0.0
    assert edge_confidence(1.0, 0.0) == 1.0
