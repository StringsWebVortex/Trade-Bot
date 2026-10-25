"""
Promotion gate for the self-tuning subsystem.

Design: docs/SELF_TUNING_DESIGN.md §1.3-1.4 ("multi-metric improvement,
never a single-metric win") and §3 (bounds enforcement).

The gate is the single choke point through which a challenger value must
pass before VersionedConfigStore.promote() is ever called. It enforces,
in order:

  1. The challenger value is within the parameter's registered bounds.
  2. A designated primary metric shows a statistically significant
     improvement.
  3. NO tracked metric shows a statistically significant regression --
     a challenger that improves Sharpe but significantly worsens
     drawdown is rejected, not accepted as a "trade-off."

Anything that fails any check is rejected with a human-readable reason,
which the caller is expected to write to TuningAuditLog.

Registry: RISK-005 (config/quality_registry.json).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from src.tuning.evaluator import (
    _SIGNIFICANCE_ALPHA,
    EvaluationResult,
    deflated_sharpe_ratio,
)
from src.tuning.registry import TunableParameter

# Minimum deflated-Sharpe probability once the attempt count is accounted for.
_DSR_MIN_PROBABILITY: Final[float] = 0.95


@dataclass(frozen=True)
class GateDecision:
    accepted: bool
    reasons: tuple[str, ...]


class PromotionGate:
    def decide(
        self,
        param: TunableParameter,
        evaluation: EvaluationResult,
        primary_metric: str,
        n_trials: int = 1,
    ) -> GateDecision:
        """
        `n_trials` is the number of PROPOSED attempts on this parameter to
        date, including this one. Each attempt is a fresh draw at nominal
        alpha against the same data, so the primary improvement must also
        survive a multiple-testing correction (STR-05): the deflated Sharpe
        ratio when the challenger samples are available, otherwise a
        Bonferroni-adjusted p-value.
        """
        reasons: list[str] = []

        if not param.in_bounds(evaluation.challenger_value):
            reasons.append(
                f"challenger value {evaluation.challenger_value} outside bounds "
                f"[{param.floor}, {param.ceiling}]"
            )
            return GateDecision(accepted=False, reasons=tuple(reasons))

        if evaluation.any_significant_regression:
            regressed = [c.metric_name for c in evaluation.comparisons if c.significant_regression]
            reasons.append(f"significant regression on: {', '.join(regressed)}")

        try:
            primary_improved = evaluation.improved(primary_metric)
        except KeyError:
            reasons.append(f"primary metric {primary_metric!r} not present in evaluation")
            return GateDecision(accepted=False, reasons=tuple(reasons))

        if not primary_improved:
            reasons.append(f"primary metric {primary_metric!r} did not significantly improve")

        if primary_improved:
            comp = evaluation.comparison(primary_metric)
            trials = max(1, n_trials)
            if comp.challenger_samples:
                dsr = deflated_sharpe_ratio(list(comp.challenger_samples), trials)
                if dsr < _DSR_MIN_PROBABILITY:
                    reasons.append(
                        f"deflated Sharpe {dsr:.3f} < {_DSR_MIN_PROBABILITY} "
                        f"after {trials} attempts (multiple testing)"
                    )
            elif comp.p_value >= _SIGNIFICANCE_ALPHA / trials:
                reasons.append(
                    f"p-value {comp.p_value:.4g} not below Bonferroni threshold "
                    f"{_SIGNIFICANCE_ALPHA / trials:.4g} after {trials} attempts"
                )

        accepted = not reasons
        if accepted:
            reasons.append(
                f"primary metric {primary_metric!r} significantly improved; no regressions"
            )

        return GateDecision(accepted=accepted, reasons=tuple(reasons))
