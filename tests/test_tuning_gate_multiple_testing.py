"""STR-05: the promotion gate corrects for the number of prior attempts.

Decides:
  - REG-1111 -- A primary-metric win must survive deflation for the attempt count
"""

from __future__ import annotations

from src.tuning.evaluator import EvaluationResult, MetricComparison
from src.tuning.gate import PromotionGate
from src.tuning.registry import TunableParameter

_SAMPLES = (0.9, -0.1, 0.7, 0.1, 0.8, 0.0, 0.6, 0.2, 0.5, 0.4, 0.3, 0.6)


def _param() -> TunableParameter:
    return TunableParameter(
        name="hmm.entropy_threshold",
        description="t",
        floor=0.3,
        ceiling=0.7,
        current=0.5,
        eval_strategy="cpcv_oos_sharpe",
    )


def _evaluation(
    p_value: float, samples: tuple[float, ...] = (), *, samples_are_returns: bool | None = None
) -> EvaluationResult:
    return EvaluationResult(
        param_name="hmm.entropy_threshold",
        challenger_value=0.55,
        comparisons=(
            MetricComparison(
                metric_name="oos_sharpe",
                champion_mean=0.0,
                challenger_mean=0.4,
                delta=0.4,
                p_value=p_value,
                significant_improvement=True,
                significant_regression=False,
                challenger_samples=samples,
                challenger_samples_are_returns=(
                    bool(samples) if samples_are_returns is None else samples_are_returns
                ),
            ),
        ),
    )


def test_deflated_sharpe_accepts_first_attempt_but_rejects_after_many() -> None:
    """Would fail before the fix: the gate ignored attempt count entirely."""
    gate = PromotionGate()
    evaluation = _evaluation(0.01, _SAMPLES)
    assert gate.decide(_param(), evaluation, "oos_sharpe", n_trials=1).accepted
    late = gate.decide(_param(), evaluation, "oos_sharpe", n_trials=100_000)
    assert not late.accepted
    assert any("deflated Sharpe" in r for r in late.reasons)


def test_bonferroni_fallback_when_no_samples_available() -> None:
    gate = PromotionGate()
    evaluation = _evaluation(0.03)
    assert gate.decide(_param(), evaluation, "oos_sharpe", n_trials=1).accepted
    many = gate.decide(_param(), evaluation, "oos_sharpe", n_trials=5)
    assert not many.accepted
    assert any("Bonferroni" in r for r in many.reasons)


def test_fold_metric_samples_use_bonferroni_not_return_level_dsr() -> None:
    evaluation = _evaluation(0.01, _SAMPLES, samples_are_returns=False)
    decision = PromotionGate().decide(_param(), evaluation, "oos_sharpe", n_trials=100)
    assert not decision.accepted
    assert any("Bonferroni" in reason for reason in decision.reasons)
    assert not any("deflated Sharpe" in reason for reason in decision.reasons)


def test_nonfinite_primary_p_value_fails_closed() -> None:
    evaluation = _evaluation(float("nan"))
    decision = PromotionGate().decide(_param(), evaluation, "oos_sharpe", n_trials=1)
    assert not decision.accepted
    assert any("invalid" in reason for reason in decision.reasons)


def test_strong_evidence_survives_a_few_attempts() -> None:
    """Negative control: the correction must not reject everything."""
    assert PromotionGate().decide(_param(), _evaluation(0.0001), "oos_sharpe", n_trials=5).accepted
