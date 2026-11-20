"""
Cross-exchange basis arbitrage strategy — v3 Multi-Exchange Execution.

Detects when the same symbol's price diverges meaningfully across two
venues (basis spread) and signals a fade: long the cheaper venue / short
the richer venue. This is a distinct, close-to-market-neutral return
stream on top of v2's single-venue strategy families.

Authority:
  - Almgren & Chriss (2001) — basis spread as an execution/arbitrage signal
  - Chan (2013) Algorithmic Trading Ch.5 — cross-venue arbitrage mechanics
"""

from __future__ import annotations

from dataclasses import dataclass

from src.risk.execution_cost import ExecutionCost, edge_confidence
from src.strategies.registry import Signal

# Opening buys one venue and sells the other; closing reverses both. Four
# marketable orders, each paying its venue's fee, half-spread and impact.
ROUND_TRIP_LEGS: int = 4


@dataclass(frozen=True, slots=True)
class CrossExchangeContext:
    """Bar-equivalent context: same-symbol prices on two venues.

    cost is the measured per-leg execution cost (src/risk/execution_cost.py).
    None means it could not be measured, and the strategy abstains.
    """

    venue_a: str
    price_a: float
    venue_b: str
    price_b: float
    cost: ExecutionCost | None = None


def compute_basis_bps(price_a: float, price_b: float) -> float:
    """Basis spread in basis points: (price_a - price_b) / price_b * 10_000."""
    if price_a <= 0:
        raise ValueError(f"price_a must be positive, got {price_a}")
    if price_b <= 0:
        raise ValueError(f"price_b must be positive, got {price_b}")
    return (price_a - price_b) / price_b * 10_000.0


class CrossExchangeArbStrategy:
    """
    Registry-conformant strategy: fades basis spread between two venues.

    STR-21: the entry threshold is the measured round-trip hurdle
    (ExecutionCost.hurdle_bps over four legs), not a fixed bps figure, and
    confidence is the net edge relative to that hurdle. No measured cost, no
    trade.

    direction is w.r.t. venue_a: positive spread (a richer than b) ->
    short a / long b (direction = -1). Negative spread -> long a (direction = 1).
    """

    strategy_id: str = "cross_exchange_arb_v1"

    def __init__(self, max_capital_fraction: float = 0.10) -> None:
        if not 0.0 < max_capital_fraction <= 1.0:
            raise ValueError(f"max_capital_fraction must be in (0, 1], got {max_capital_fraction}")
        self._max_capital_fraction = max_capital_fraction

    def generate_signal(self, bar: object) -> Signal:
        if not isinstance(bar, CrossExchangeContext):
            raise TypeError(
                f"CrossExchangeArbStrategy requires a CrossExchangeContext, got {type(bar)}"
            )
        if bar.cost is None:
            return Signal(direction=0, confidence=0.0, regime_fit=0.9)

        spread_bps = compute_basis_bps(bar.price_a, bar.price_b)
        confidence = edge_confidence(abs(spread_bps), bar.cost.hurdle_bps(ROUND_TRIP_LEGS))
        if confidence <= 0.0:
            return Signal(direction=0, confidence=0.0, regime_fit=0.9)

        direction = -1 if spread_bps > 0 else 1
        # Regime-agnostic by construction — arbitrage works in any market state.
        return Signal(direction=direction, confidence=confidence, regime_fit=0.9)

    def required_capital_fraction(self) -> float:
        return self._max_capital_fraction
