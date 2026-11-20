"""
Capital preservation floor — v10 Fully Autonomous Multi-Decade Operation.

The final backstop beneath every other automated decision layer (v2's
kill-switch, v4's drift detection, v7's macro budget, v9's meta-allocator):
a hard, code-enforced maximum drawdown that halts ALL trading and requires
explicit human re-authorization to resume. Unlike the per-strategy
kill-switch (v2), this operates at the whole-book level and is designed
to never be bypassed by any automated process — only an explicit,
out-of-band re-authorization call clears it.

Authority:
  - Domain Prior: enforce drawdown and position limits; Kelly is a
    ceiling, not a target — this is the outermost such ceiling, beneath
    which no automated system may trade regardless of any other signal

Registry: INV-002 (config/quality_registry.json).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import structlog

from src.eventbus import get_event_bus
from src.risk.state_persistence import StateUnreadableError, load_state, save_state

log = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class ReAuthorization:
    """Records who/when cleared the floor — never auto-generated."""

    authorized_by: str
    reason: str
    at_ms: int


class CapitalPreservationFloor:
    """
    Tracks peak equity and halts trading (halted=True) the instant
    drawdown from peak exceeds max_drawdown_pct. Once halted, only
    re_authorize() can clear it — no automated code path may call
    re_authorize() from within this module or any other risk module.
    """

    def __init__(self, max_drawdown_pct: float = 0.30, state_path: Path | None = None) -> None:
        if not 0.0 < max_drawdown_pct < 1.0:
            raise ValueError(f"max_drawdown_pct must be in (0, 1), got {max_drawdown_pct}")
        self._max_drawdown_pct = max_drawdown_pct
        self._peak_equity: float = 0.0
        self._halted: bool = False
        self._halt_reason: str = ""
        self._last_reauth: ReAuthorization | None = None
        # EXR-013: with a state_path, halted/peak/reauth survive a restart.
        self._state_path = state_path
        self._restore()

    def _restore(self) -> None:
        if self._state_path is None:
            return
        try:
            state = load_state(self._state_path)
            if state is None:
                return
            peak = float(state["peak_equity"])
            if not math.isfinite(peak) or peak < 0.0:
                raise StateUnreadableError("non-finite peak")
            self._peak_equity = peak
            self._halted = bool(state["halted"])
            self._halt_reason = str(state.get("halt_reason", ""))
            reauth = state.get("last_reauth")
            if isinstance(reauth, dict):
                self._last_reauth = ReAuthorization(
                    authorized_by=str(reauth["authorized_by"]),
                    reason=str(reauth["reason"]),
                    at_ms=int(reauth["at_ms"]),
                )
        except (StateUnreadableError, KeyError, TypeError, ValueError) as exc:
            # An unreadable file cannot rule out a halt: fail closed.
            self._halted = True
            self._halt_reason = f"capital floor state unreadable, failing closed: {exc}"
            log.critical("capital_floor.state_unreadable", error=str(exc))

    def _persist(self) -> None:
        if self._state_path is None:
            return
        reauth = self._last_reauth
        save_state(
            self._state_path,
            {
                "halted": self._halted,
                "halt_reason": self._halt_reason,
                "peak_equity": self._peak_equity,
                "last_reauth": None
                if reauth is None
                else {
                    "authorized_by": reauth.authorized_by,
                    "reason": reauth.reason,
                    "at_ms": reauth.at_ms,
                },
            },
        )

    def update_equity(self, equity_usd: float) -> bool:
        """
        Records the latest equity mark and evaluates the floor. Returns
        True if trading should proceed (not halted), False if halted.
        Once halted, repeated calls keep returning False regardless of
        equity recovery — recovery alone never auto-clears the halt.

        Raises ValueError on a non-finite mark, which is *not* merely
        defensive here — it is the difference between a one-tick fault and a
        permanently disabled backstop:

          - `equity_usd < 0.0` is False for NaN, so the existing guard does
            not catch it, and `drawdown_pct` then computes to NaN.
            `nan >= max_drawdown_pct` is False, so the floor does not fire.
          - `inf` is worse and it persists. `max(peak, inf)` sets
            `_peak_equity = inf`, and from then on every drawdown is
            `(inf - equity) / inf = nan`, which never trips the floor again.
            One bad mark silently disables the outermost backstop for the
            life of the process.

        Raising keeps a corrupt mark out of `_peak_equity` entirely. The
        caller sees the fault instead of a floor that has quietly stopped
        working — this instance holds the only copy of that state, so there
        is nothing downstream that would notice.
        """
        if not math.isfinite(equity_usd):
            raise ValueError(f"equity_usd must be a finite number, got {equity_usd}")
        if equity_usd < 0.0:
            raise ValueError(f"equity_usd must be non-negative, got {equity_usd}")

        new_peak = equity_usd > self._peak_equity
        self._peak_equity = max(self._peak_equity, equity_usd)
        if new_peak and not self._halted:
            self._persist()
        if self._halted:
            return False

        if self._peak_equity > 0.0:
            drawdown_pct = (self._peak_equity - equity_usd) / self._peak_equity
            if drawdown_pct >= self._max_drawdown_pct:
                self._halted = True
                self._halt_reason = (
                    f"drawdown {drawdown_pct:.3f} >= floor {self._max_drawdown_pct:.3f} "
                    f"(peak={self._peak_equity:.2f}, current={equity_usd:.2f})"
                )
                self._persist()
                # The outermost backstop tripping is the single most
                # important thing this process can tell an operator, and it
                # never auto-clears -- someone has to come and re-authorize
                # it. Waiting for a 30s poll to surface that is 30s of a
                # halted system looking like a quiet one.
                get_event_bus().publish(
                    "capital_floor",
                    {
                        "halted": True,
                        "reason": self._halt_reason,
                        "drawdown_pct": round(drawdown_pct, 4),
                        "peak_equity_usd": round(self._peak_equity, 2),
                        "equity_usd": round(equity_usd, 2),
                    },
                )
                return False
        return True

    @property
    def is_halted(self) -> bool:
        return self._halted

    @property
    def halt_reason(self) -> str:
        return self._halt_reason

    def re_authorize(self, authorized_by: str, reason: str, at_ms: int) -> None:
        """
        Explicit human re-authorization to resume trading. Does not reset
        peak_equity — a fresh peak is only established as new marks come
        in, so the floor remains sensitive to further drawdown from the
        pre-halt peak until equity genuinely recovers past it.
        """
        if not authorized_by:
            raise ValueError("authorized_by must be a non-empty string")
        self._halted = False
        self._halt_reason = ""
        self._last_reauth = ReAuthorization(authorized_by=authorized_by, reason=reason, at_ms=at_ms)
        self._persist()
        get_event_bus().publish(
            "capital_floor",
            {
                "halted": False,
                "authorized_by": authorized_by,
                "reason": reason,
                "at_ms": at_ms,
            },
        )

    @property
    def last_reauthorization(self) -> ReAuthorization | None:
        return self._last_reauth
