"""
Abstract base class for trade executors (VUL-038).

Both LiveExecutor and PaperExecutor must implement this interface.
Replaces the unsafe cast(LiveExecutor, ...) pattern in api/main.py —
all API code should type against AbstractExecutor.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.execution.idempotency import IdempotencyRegistry
from src.risk.kelly import KellyResult, apply_size_scalar

# ---------------------------------------------------------------------------
# Approval queue -- RESTRICTED (above notional_limit_usd) and MANUAL modes
# ---------------------------------------------------------------------------
#
# EXR-018 / REG-1718: submit_signal() never waits for an operator. It queues
# the trade and returns "queued", so the timeframe loop keeps ticking. An
# approval is an approved *intent*: it is executed only by the next tick of
# the same symbol and timeframe whose own signal is still tradeable. That tick
# has re-run the whole gate stack, the meta-label gate and Kelly against fresh
# data, and it brings the fresh price. The intent is then checked once more
# against what the operator approved: same direction, price within
# approval_max_price_drift_bps of the price the request showed, and never more
# notional than was approved. Anything else rejects it. An approved intent
# that its next tick does not execute lapses (close_approval_window), so an
# approval can never be redeemed by a later, unrelated signal.


@dataclass
class ApprovalRequest:
    """
    A trade awaiting, or approved by, an operator.

    entry_price : mark price when the request was queued -- the price the
                  operator sees and approves against (0.0 = unknown)
    resolved    : set when approved, rejected or expired
    approved    : True = the operator approved the intent
    operator    : approving operator, or 'auto_timeout'
    timeout_s   : seconds an unresolved request stays approvable
                  (None = until the operator decides)
    resolved_at : time.monotonic() of the resolution
    window_seen : an approved intent has already been offered to one tick
    """

    request_id: str
    symbol: str
    timeframe: str
    direction: int
    notional_usd: float
    entry_price: float
    quantity: float
    kelly_fraction: float
    regime_state: int
    meta_label_prob: float
    raw_signal: float
    created_at: float  # time.monotonic()

    resolved: bool = field(default=False)
    approved: bool = field(default=False)
    operator: str = field(default="")
    timeout_s: float | None = field(default=None)
    resolved_at: float = field(default=0.0)
    window_seen: bool = field(default=False)

    def to_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "direction": "long" if self.direction == 1 else "short",
            "notional_usd": round(self.notional_usd, 2),
            "entry_price": round(self.entry_price, 4),
            "quantity": self.quantity,
            "kelly_fraction": round(self.kelly_fraction, 4),
            "regime_state": self.regime_state,
            "meta_label_prob": round(self.meta_label_prob, 4),
            "raw_signal": round(self.raw_signal, 4),
        }


def expire_unresolved_approvals(queue: dict[str, ApprovalRequest], now: float) -> None:
    """Auto-reject unresolved requests older than their own timeout_s."""
    for req in queue.values():
        if req.resolved or req.timeout_s is None or now - req.created_at <= req.timeout_s:
            continue
        req.resolved = True
        req.approved = False
        req.operator = "auto_timeout"
        req.resolved_at = now


def open_approval_for(
    queue: dict[str, ApprovalRequest], symbol: str, timeframe: str
) -> ApprovalRequest | None:
    """The request still open for this symbol/timeframe: unresolved, or approved
    and not yet executed. At most one exists, because a key with an open
    request never queues a second one."""
    for req in queue.values():
        if req.symbol == symbol and req.timeframe == timeframe:
            if not req.resolved or req.approved:
                return req
    return None


def lapse_approved_intents(
    queue: dict[str, ApprovalRequest], symbol: str, timeframe: str
) -> list[ApprovalRequest]:
    """
    Start-of-tick bookkeeping for one symbol/timeframe.

    An approved intent is offered to exactly one tick: the first one that
    starts after the approval. That tick marks it; the tick after drops it.
    Returns the intents dropped here.
    """
    lapsed: list[ApprovalRequest] = []
    for rid, req in list(queue.items()):
        if req.symbol != symbol or req.timeframe != timeframe:
            continue
        if not (req.resolved and req.approved):
            continue
        if req.window_seen:
            queue.pop(rid, None)
            lapsed.append(req)
        else:
            req.window_seen = True
    return lapsed


def revalidate_approved_intent(
    req: ApprovalRequest,
    *,
    direction: int,
    kelly_result: KellyResult,
    current_price: float,
    max_price_drift_bps: float,
) -> tuple[KellyResult | None, str]:
    """
    Decide whether a fresh, gate-passed signal may execute an approved intent.

    Returns (order size to fill, "") or (None, reason). Fails closed: an
    unknown price, a changed direction, a price that moved further than the
    operator's approval covers, or a size that cannot be brought within the
    approved notional all reject.
    """
    if direction != req.direction:
        return None, "approval_direction_changed"
    ref = req.entry_price
    if not (math.isfinite(ref) and ref > 0.0 and math.isfinite(current_price)):
        return None, "approval_price_unknown"
    if current_price <= 0.0:
        return None, "approval_price_unknown"
    drift_bps = abs(current_price / ref - 1.0) * 10_000.0
    if not drift_bps <= max_price_drift_bps:
        return None, "approval_price_drift"
    fresh = kelly_result.notional_usd
    if not (math.isfinite(fresh) and fresh > 0.0 and req.notional_usd > 0.0):
        return None, "approval_size_invalid"
    if fresh <= req.notional_usd:
        return kelly_result, ""
    capped = apply_size_scalar(kelly_result, req.notional_usd / fresh, current_price)
    if capped is None:
        return None, "approval_size_below_minimum"
    return capped, ""


class AbstractExecutor(ABC):
    """Common interface shared by LiveExecutor and PaperExecutor."""

    @property
    @abstractmethod
    def idempotency(self) -> IdempotencyRegistry:
        """
        Registry of order idempotency keys this executor has submitted (LAW3).

        Part of the abstract interface rather than a live-only detail: paper
        and live must dedupe identically, or a duplicate-submission bug hides
        in paper trading and only appears with real money. It is exposed so
        reconciliation and recovery paths can ask "did this intent already go
        out?" without reaching into a concrete executor.
        """
        ...

    @property
    @abstractmethod
    def equity_usd(self) -> float: ...

    @property
    @abstractmethod
    def cash_usd(self) -> float: ...

    @property
    @abstractmethod
    def starting_capital(self) -> float: ...

    @property
    @abstractmethod
    def starting_equity_usd(self) -> float:
        """
        Daily-start equity for drawdown gate calculation.

        NEW-009: Exposes drawdown_tracker.daily_start_equity through the
        AbstractExecutor interface, preventing orchestrator from reaching
        through the abstraction boundary to a concrete attribute.
        """
        ...

    @abstractmethod
    def open_positions(self) -> list[dict[str, object]]: ...

    @abstractmethod
    async def open_positions_safe(self) -> list[dict[str, object]]: ...

    @abstractmethod
    def pending_approvals(self) -> list[dict[str, object]]: ...

    @abstractmethod
    async def pending_approvals_safe(self) -> list[dict[str, object]]: ...

    @abstractmethod
    async def resolve_approval(
        self,
        request_id: str,
        approved: bool,
        operator: str,
    ) -> bool: ...

    @abstractmethod
    def close_approval_window(self, symbol: str, timeframe: str) -> None:
        """
        Called at the start of every tick for symbol/timeframe (EXR-018).

        Drops an approved intent that already had its tick, so an approval is
        never redeemed by a later signal. Synchronous on purpose: it holds no
        await, so it is atomic with respect to the executor's other coroutines.
        """
        ...

    @abstractmethod
    async def submit_signal(self, *args, **kwargs) -> tuple[str | None, str]: ...

    @abstractmethod
    def position_count(self) -> int: ...

    @abstractmethod
    async def get_consecutive_losses(self, symbol: str) -> int: ...

    @abstractmethod
    async def get_daily_pnl(self, symbol: str) -> float: ...

    @abstractmethod
    async def reset_daily_equity(self) -> float:
        """
        Atomically read current equity, reset the drawdown tracker's daily_start,
        and return the equity value used for the reset.

        NEW-005: Callers (orchestrator midnight reset) must use this instead of
        accessing drawdown_tracker directly to avoid torn reads during concurrent
        mark_to_market calls.
        """
        ...

    @abstractmethod
    async def get_risk_snapshot(self) -> tuple[float, float, float]:
        """
        C-08: Atomically return (equity_usd, starting_equity_usd, daily_pnl_usd)
        under the executor lock, preventing torn reads in orchestrator._tick().
        """
        ...

    @abstractmethod
    async def mark_to_market(self, prices: dict[str, float]) -> float:
        """
        Update unrealized PnL for all open positions given latest prices.

        GAP-013: added to the abstract interface so the orchestrator's
        position-monitor loop can call this through AbstractExecutor without
        an unsafe cast to a concrete executor type.
        """
        ...

    @abstractmethod
    async def close_position(
        self,
        trade_id: str,
        exit_price: float,
        exit_reason: str,
    ) -> float:
        """
        Close an open position at the given price, returning realized net PnL.

        GAP-013: added to the abstract interface for the same reason as
        mark_to_market above -- the position-monitor loop needs to close
        positions that trip a stop-loss / take-profit / time-exit condition.
        """
        ...
