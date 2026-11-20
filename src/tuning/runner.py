"""
Shadow-mode tuning runner -- ties proposer + evaluator + gate + store +
audit log together into one attempt cycle.

Design: docs/SELF_TUNING_DESIGN.md §2 (architecture) and §7 (rollout plan,
step 2: "running in shadow mode only -- proposals logged, never promoted").

`shadow_mode=True` (the default) makes this runner behaviorally inert
with respect to real trading: a challenger can clear every gate check and
it will still only be recorded as WOULD_PROMOTE in the audit log, never
written to VersionedConfigStore. Flipping to live promotion
(`SELF_TUNING_SHADOW_MODE=false`) is a separate, explicit operator
configuration step (see rollout plan step 3), not a flag flip here.

When shadow_mode is False and a challenger is promoted, this runner also
advances the parameter's live champion value in ParameterRegistry
(registry.update_current) -- see src/tuning/live_overrides.py, which is
the seam that surfaces that updated value to the live regime/risk/
features/model code paths.

A live promotion is also journalled to a Markdown decision log
(`decision_log_path`, default DECISION_LOG.md via SelfTuningSettings) so an
unattended structural change is reconstructable by a human auditor without
parsing the JSONL audit log. Shadow WOULD_PROMOTE events are not journalled
-- they change nothing, and logging them would bury the real changes.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import structlog

from src.config import SelfTuningSettings
from src.diagnostics.decision_log_writer import (
    StructuralChangeRecord,
    append_to_decision_log,
)
from src.tuning.audit import TuningAuditLog, TuningEventType
from src.tuning.evaluator import EvaluationResult, MetricComparison
from src.tuning.gate import GateDecision, PromotionGate
from src.tuning.proposer import Proposal, Proposer
from src.tuning.registry import ParameterRegistry, TunableParameter
from src.tuning.store import VersionedConfigStore
from src.tuning.watchdog import DriftDetector, PostPromotionWatchdog

log: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

EvaluateFn = Callable[[TunableParameter, Proposal], list[MetricComparison]]


@dataclass(frozen=True)
class AttemptResult:
    param_name: str
    attempted: bool
    accepted: bool
    promoted: bool
    reasons: tuple[str, ...]
    challenger_value: float | None = None


class SelfTuningDisabledError(RuntimeError):
    """Raised only if a caller forces a live (non-shadow) promotion while the kill switch is off."""


class TuningRunner:
    def __init__(
        self,
        registry: ParameterRegistry,
        store: VersionedConfigStore,
        audit_log: TuningAuditLog,
        settings: SelfTuningSettings,
        proposer: Proposer,
        gate: PromotionGate,
        shadow_mode: bool = True,
        decision_log_path: Path | None = None,
        watchdog: PostPromotionWatchdog | None = None,
        probation_detector_factory: Callable[[], DriftDetector] | None = None,
    ) -> None:
        self._watchdog = watchdog
        self._probation_detector_factory = probation_detector_factory
        self._registry = registry
        self._store = store
        self._audit_log = audit_log
        self._settings = settings
        self._proposer = proposer
        self._gate = gate
        self._shadow_mode = shadow_mode
        # Markdown journal for human auditors. Only written on live promotions
        # -- a shadow WOULD_PROMOTE changes nothing structurally, so logging it
        # here would bury the real changes in noise.
        self._decision_log_path = decision_log_path

    def set_probation_detector_factory(self, factory: Callable[[], DriftDetector] | None) -> None:
        """Supplied by the layer that owns the drift baseline (orchestration);
        tuning sits below risk and cannot construct a detector itself."""
        self._probation_detector_factory = factory

    def _cooldown_active(
        self,
        param_name: str,
        closed_trade_count: int | None = None,
        bar_count: int | None = None,
    ) -> tuple[bool, str]:
        """
        Whether this parameter is still inside its post-attempt cooldown.

        Two independent guards, both of which must clear. Wall-clock alone is
        not enough: a quiet market can let 24 hours pass on a handful of
        trades, and re-tuning on that little new evidence is how a tuner
        starts fitting noise. min_trades_between_attempts existed in
        SelfTuningSettings for exactly this and was never read by anything --
        the hours half of the cadence guard was enforced and the trades half
        silently was not.

        Evidence counters are optional because the runner has no storage
        access of its own. Trade-driven and bar-driven callers supply their
        respective counters; an unavailable counter is not guessed at.
        """
        entries = [
            e
            for e in self._audit_log.read_for_param(param_name)
            if e.event_type == TuningEventType.PROPOSED
        ]
        if not entries:
            return False, ""
        last = entries[-1]
        elapsed_hours = (
            datetime.now(UTC) - datetime.fromisoformat(last.timestamp)
        ).total_seconds() / 3600.0
        if elapsed_hours < self._settings.min_hours_between_attempts:
            return True, "cooldown_active"

        if closed_trade_count is not None:
            previous_trades = last.details.get("closed_trade_count")
            if isinstance(previous_trades, int) and (
                closed_trade_count - previous_trades < self._settings.min_trades_between_attempts
            ):
                return True, "cooldown_active_insufficient_trades"

        if bar_count is not None:
            previous_bars = last.details.get("bar_count")
            if isinstance(previous_bars, int) and (
                bar_count - previous_bars < self._settings.min_bars_between_attempts
            ):
                return True, "cooldown_active_insufficient_bars"
        return False, ""

    def _write_decision_log(
        self,
        param_name: str,
        proposal: Proposal,
        decision: GateDecision,
        primary_metric: str,
    ) -> None:
        """
        Append a Markdown record of a live promotion for human auditors.

        Best-effort by design: the promotion is already durable in the version
        store and the JSONL audit log, so a filesystem problem here must not
        undo or block a decision those two have already recorded. The failure
        is logged at error level rather than swallowed.
        """
        if self._decision_log_path is None:
            return
        record = StructuralChangeRecord(
            title=f"Self-tuning promoted {param_name}",
            change_type="parameter_promoted",
            justification=(
                f"Challenger value {proposal.challenger_value} cleared the promotion "
                f"gate on {primary_metric} and replaced champion "
                f"{proposal.champion_value}. Promoted unattended by the self-tuning "
                f"runner (shadow_mode=False)."
            ),
            evidence={
                "param_name": param_name,
                "champion_value": proposal.champion_value,
                "challenger_value": proposal.challenger_value,
                "primary_metric": primary_metric,
                "gate_reasons": "; ".join(decision.reasons),
            },
        )
        try:
            append_to_decision_log(record, self._decision_log_path)
        except OSError as exc:
            log.error(
                "tuning.decision_log_write_failed",
                param_name=param_name,
                path=str(self._decision_log_path),
                error=str(exc),
            )

    def attempt(
        self,
        param_name: str,
        evaluate_fn: EvaluateFn,
        primary_metric: str,
        closed_trade_count: int | None = None,
        bar_count: int | None = None,
    ) -> AttemptResult:
        """
        Run one propose -> evaluate -> gate -> (shadow-log | promote) cycle.

        `evaluate_fn(param, proposal) -> list[MetricComparison]` is called
        AFTER the challenger value is proposed, so the caller's backtest
        harness (e.g. run_entropy_threshold_backtest) always evaluates the
        actual proposed value -- not a value chosen independently of what
        the proposer picked. This runner only orchestrates the decision;
        it does not itself run backtests.

        `closed_trade_count` and `bar_count` are the current evidence counts
        for trade-driven and bar-driven parameters respectively. Each is
        compared only with the matching count recorded by that parameter's
        previous proposal.
        """
        if not self._settings.enabled:
            self._audit_log.record(
                param_name, TuningEventType.SKIPPED, {"reason": "self_tuning_disabled"}
            )
            return AttemptResult(
                param_name=param_name,
                attempted=False,
                accepted=False,
                promoted=False,
                reasons=("self_tuning_disabled",),
            )

        if self._watchdog is not None and self._watchdog.is_locked(param_name):
            self._audit_log.record(
                param_name, TuningEventType.SKIPPED, {"reason": "watchdog_locked"}
            )
            return AttemptResult(
                param_name=param_name,
                attempted=False,
                accepted=False,
                promoted=False,
                reasons=("watchdog_locked",),
            )

        blocked, cooldown_reason = self._cooldown_active(param_name, closed_trade_count, bar_count)
        if blocked:
            self._audit_log.record(param_name, TuningEventType.SKIPPED, {"reason": cooldown_reason})
            return AttemptResult(
                param_name=param_name,
                attempted=False,
                accepted=False,
                promoted=False,
                reasons=(cooldown_reason,),
            )

        param = self._registry.get(param_name)
        n_trials = (
            sum(
                1
                for e in self._audit_log.read_for_param(param_name)
                if e.event_type == TuningEventType.PROPOSED
            )
            + 1
        )
        proposal = self._proposer.propose(param, primary_metric)
        self._audit_log.record(
            param_name,
            TuningEventType.PROPOSED,
            {
                "champion_value": proposal.champion_value,
                "challenger_value": proposal.challenger_value,
                # Recorded so the NEXT attempt can measure how much new
                # trade or bar evidence has accumulated since this one.
                "closed_trade_count": closed_trade_count,
                "bar_count": bar_count,
            },
        )

        comparisons = evaluate_fn(param, proposal)
        evaluation = EvaluationResult(
            param_name=param_name,
            challenger_value=proposal.challenger_value,
            comparisons=tuple(comparisons),
        )
        self._audit_log.record(
            param_name,
            TuningEventType.EVALUATED,
            {
                "comparisons": [
                    {
                        "metric": c.metric_name,
                        "delta": c.delta,
                        "p_value": c.p_value,
                        "significant_improvement": c.significant_improvement,
                        "significant_regression": c.significant_regression,
                    }
                    for c in comparisons
                ]
            },
        )

        decision: GateDecision = self._gate.decide(param, evaluation, primary_metric, n_trials)

        if not decision.accepted:
            self._audit_log.record(
                param_name, TuningEventType.REJECTED, {"reasons": list(decision.reasons)}
            )
            return AttemptResult(
                param_name=param_name,
                attempted=True,
                accepted=False,
                promoted=False,
                reasons=decision.reasons,
                challenger_value=proposal.challenger_value,
            )

        if self._shadow_mode:
            self._audit_log.record(
                param_name,
                TuningEventType.WOULD_PROMOTE,
                {"challenger_value": proposal.challenger_value, "reasons": list(decision.reasons)},
            )
            return AttemptResult(
                param_name=param_name,
                attempted=True,
                accepted=True,
                promoted=False,
                reasons=decision.reasons,
                challenger_value=proposal.challenger_value,
            )

        self._store.promote(
            param_name,
            proposal.challenger_value,
            evidence={"reasons": list(decision.reasons)},
            promoted_by="bot",
        )
        self._registry.update_current(param_name, proposal.challenger_value)
        self._audit_log.record(
            param_name,
            TuningEventType.PROMOTED,
            {"challenger_value": proposal.challenger_value, "reasons": list(decision.reasons)},
        )
        self._write_decision_log(param_name, proposal, decision, primary_metric)
        if self._watchdog is not None and self._probation_detector_factory is not None:
            self._watchdog.start_probation(param_name, self._probation_detector_factory())
        return AttemptResult(
            param_name=param_name,
            attempted=True,
            accepted=True,
            promoted=True,
            reasons=decision.reasons,
            challenger_value=proposal.challenger_value,
        )
