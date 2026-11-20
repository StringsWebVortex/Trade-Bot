"""REG-1711: champion/challenger metrics are compared with a one-sided paired t-test.

Every backtest harness builds both arms in the same fold loop, so the samples
are fold-aligned. Welch's two-sample test treats them as independent and lets
the fold-to-fold spread both arms share hide a consistent per-fold effect. The
evaluator now tests the per-fold differences (``ttest_rel``) one-sided in the
direction of the delta, and rejects unequal fold counts rather than treating the arms as independent.
"""

import pytest
from scipy.stats import ttest_ind, ttest_rel

from src.tuning.evaluator import ChallengerEvaluator, InsufficientSampleError

_ALPHA = 0.05

# Folds with a wide spread (0.0 .. 1.1) that both arms share, and a small but
# consistent per-fold shift of 0.010 .. 0.012.
_CHAMPION = [0.1 * i for i in range(12)]
_SHIFT = [0.01 + 0.001 * (i % 3) for i in range(12)]


@pytest.mark.parametrize("sign", [1.0, -1.0], ids=["improvement", "regression"])
def test_fold_aligned_shift_is_significant_where_welch_is_not(sign: float) -> None:
    challenger = [c + sign * s for c, s in zip(_CHAMPION, _SHIFT, strict=True)]
    alternative = "greater" if sign > 0 else "less"
    # Premise: the unpaired Welch test cannot see the shift through the spread.
    welch_p = float(
        ttest_ind(challenger, _CHAMPION, equal_var=False, alternative=alternative).pvalue
    )
    assert welch_p > _ALPHA

    comparison = ChallengerEvaluator().compare_metric("oos_sharpe", _CHAMPION, challenger)

    assert comparison.significant_improvement is (sign > 0)
    assert comparison.significant_regression is (sign < 0)
    assert comparison.p_value == pytest.approx(
        float(ttest_rel(challenger, _CHAMPION, alternative=alternative).pvalue)
    )
    assert comparison.p_value < _ALPHA


def test_unequal_fold_counts_are_rejected() -> None:
    champion = [0.1 * i for i in range(10)]
    challenger = [0.1 * i + 0.5 for i in range(12)]

    with pytest.raises(
        InsufficientSampleError, match="paired comparison requires equal sample counts"
    ):
        ChallengerEvaluator().compare_metric("oos_sharpe", champion, challenger)


def test_identical_arms_report_no_evidence() -> None:
    samples = [0.1 * i for i in range(10)]

    comparison = ChallengerEvaluator().compare_metric("oos_sharpe", samples, list(samples))

    assert comparison.p_value == 1.0
    assert not comparison.significant_improvement
    assert not comparison.significant_regression
