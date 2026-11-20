"""
Measured execution cost, and the entry hurdle a carry or arbitrage trade must clear.

STR-21: the basis, funding-carry and cross-exchange families compared their
signal against fixed numbers (5% a year, 0.01% per funding period, a 12bps
round trip) that no measurement produced. A fixed threshold is too loose on a
venue or tier that charges more and too tight on one that charges less, and
nothing told the strategy which case it was in.

The hurdle here is built from what the account actually pays:

    per_leg_bps  = fee_bps + half_spread_bps + impact_bps
    round_trip   = legs * per_leg_bps
    hurdle       = round_trip + z * sqrt(legs) * uncertainty_bps

  fee_bps          : measured from the account's own recent fills
                     (measure_fee_bps), not a published schedule
  half_spread_bps  : from the live order book, as SlippageModel takes it
  impact_bps       : SlippageModel's calibrated square-root impact
  uncertainty_bps  : per-leg standard deviation of the realised cost; the
                     legs are treated as independent, so their spread adds
                     in quadrature
  z                : one-sided confidence that the realised round trip stays
                     under the hurdle (1.645 -> 95%)

A trade enters only when its gross edge exceeds the hurdle. When the cost is
unknown (too few fills to measure a fee, no order book) the caller has no
hurdle and the strategy abstains: an unmeasured cost is not a zero cost.

Pure: no I/O. The caller gathers fills, spread and impact.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final, Protocol

_BPS: Final[float] = 10_000.0

# Fewer fills than this cannot tell a fee tier from noise; below it the fee is
# reported unknown rather than estimated.
MIN_FEE_SAMPLES: Final[int] = 20

# One-sided 95%: the realised round trip exceeds the hurdle on about one
# trade in twenty when the legs' cost noise is roughly normal.
HURDLE_Z: Final[float] = 1.645


@dataclass(frozen=True, slots=True)
class FeeMeasurement:
    """Fee per leg, in bps of notional, measured from real fills."""

    mean_bps: float
    std_bps: float
    samples: int


def measure_fee_bps(
    fills: Iterable[tuple[float, float]],
    min_samples: int = MIN_FEE_SAMPLES,
) -> FeeMeasurement | None:
    """
    Fee per leg from ``(notional_usd, fee_usd)`` pairs of the account's fills.

    A pair with a non-finite value or a non-positive notional is not a fill
    and is skipped. A negative fee (a maker rebate) is kept: it is what the
    account was paid. Returns None when fewer than ``min_samples`` fills
    remain.
    """
    if min_samples < 2:
        raise ValueError(f"min_samples must be >= 2, got {min_samples}")
    rates = [
        fee / notional * _BPS
        for notional, fee in fills
        if math.isfinite(notional) and math.isfinite(fee) and notional > 0.0
    ]
    if len(rates) < min_samples:
        return None
    mean = math.fsum(rates) / len(rates)
    var = math.fsum((r - mean) ** 2 for r in rates) / (len(rates) - 1)
    return FeeMeasurement(mean_bps=mean, std_bps=math.sqrt(var), samples=len(rates))


class ClosedTradeLegs(Protocol):
    """The fields of a stored trade that closed_trade_fills reads."""

    @property
    def entry_price(self) -> float: ...

    @property
    def exit_price(self) -> float | None: ...

    @property
    def quantity(self) -> float: ...

    @property
    def fee_usd(self) -> float: ...


def closed_trade_fills(trades: Iterable[ClosedTradeLegs]) -> list[tuple[float, float]]:
    """
    ``(notional_usd, fee_usd)`` pairs for measure_fee_bps, one per closed trade.

    The executors record a closed trade's fee_usd as both legs' fees, so the
    notional it is measured against is both legs' traded value,
    ``(entry_price + exit_price) * quantity``: the pair's rate is the per-leg
    fee averaged over the round trip. A trade with no exit yet carries only
    its entry fee and would read as half the rate, so it is skipped; so is
    one whose prices, quantity or fee are not finite, or whose prices or
    quantity are not positive.
    """
    fills: list[tuple[float, float]] = []
    for trade in trades:
        exit_price = trade.exit_price
        if exit_price is None:
            continue
        values = (trade.entry_price, exit_price, trade.quantity, trade.fee_usd)
        if not all(math.isfinite(v) for v in values):
            continue
        if trade.entry_price <= 0.0 or exit_price <= 0.0 or trade.quantity <= 0.0:
            continue
        fills.append(((trade.entry_price + exit_price) * trade.quantity, trade.fee_usd))
    return fills


@dataclass(frozen=True, slots=True)
class ExecutionCost:
    """Measured cost of one leg (one marketable order), in bps of notional."""

    fee_bps: float
    half_spread_bps: float
    impact_bps: float
    uncertainty_bps: float

    def __post_init__(self) -> None:
        for name in ("fee_bps", "half_spread_bps", "impact_bps", "uncertainty_bps"):
            value = getattr(self, name)
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite, got {value}")
        for name in ("half_spread_bps", "impact_bps", "uncertainty_bps"):
            if getattr(self, name) < 0.0:
                raise ValueError(f"{name} must be >= 0, got {getattr(self, name)}")

    @classmethod
    def from_measurements(
        cls,
        fee: FeeMeasurement,
        half_spread_bps: float,
        impact_bps: float,
        slippage_error_std_bps: float = 0.0,
    ) -> ExecutionCost:
        """Combine a measured fee with the spread, impact and slippage error."""
        return cls(
            fee_bps=fee.mean_bps,
            half_spread_bps=half_spread_bps,
            impact_bps=impact_bps,
            uncertainty_bps=math.hypot(fee.std_bps, slippage_error_std_bps),
        )

    @property
    def per_leg_bps(self) -> float:
        return self.fee_bps + self.half_spread_bps + self.impact_bps

    def round_trip_bps(self, legs: int) -> float:
        _check_legs(legs)
        return legs * self.per_leg_bps

    def hurdle_bps(self, legs: int, z: float = HURDLE_Z) -> float:
        """Gross edge a trade of ``legs`` orders must exceed to enter."""
        _check_legs(legs)
        if not math.isfinite(z) or z < 0.0:
            raise ValueError(f"z must be a finite value >= 0, got {z}")
        return max(0.0, self.round_trip_bps(legs) + z * math.sqrt(legs) * self.uncertainty_bps)


def edge_confidence(gross_edge_bps: float, hurdle_bps: float) -> float:
    """
    Confidence in [0, 1] from how far the edge clears the hurdle.

    0 at or below the hurdle; 1 once the net edge equals the hurdle again
    (the edge pays the round trip twice over). Relative, so it scales with
    the venue's own cost rather than with a fixed bps band.
    """
    net = gross_edge_bps - hurdle_bps
    if not math.isfinite(net) or net <= 0.0:
        return 0.0
    if hurdle_bps <= 0.0:
        return 1.0
    return min(1.0, net / hurdle_bps)


def _check_legs(legs: int) -> None:
    if legs < 1:
        raise ValueError(f"legs must be >= 1, got {legs}")
