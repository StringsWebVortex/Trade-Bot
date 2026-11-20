"""MTH-009: walk-forward folds are embargoed, annualised by the right factor,
and a failed fold prunes the trial instead of scoring -999.

Decides:
  - REG-1113 -- Optuna walk-forward has an embargo, configurable annualisation and prunes failed folds
"""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import optuna
import pytest

from src.upgrade.optuna_wf import WalkForwardStudy, _sharpe


def _study(data: list[int], **kw: object) -> WalkForwardStudy:
    return WalkForwardStudy(study_name="t", train_fn=lambda *a: np.array([0.0]), data=data, **kw)


def test_embargo_leaves_a_gap_between_train_and_test() -> None:
    """Would fail before the fix: test started at the first row after train."""
    folds = _study(list(range(100)), n_folds=4, embargo=3)._build_folds()
    for x_train, _, x_test, _ in folds:
        assert x_test[0] - x_train[-1] - 1 == 3


def test_last_fold_keeps_the_remainder_rows() -> None:
    folds = _study(list(range(103)), n_folds=4, embargo=1)._build_folds()
    assert folds[-1][2][-1] == 102


def test_too_few_rows_for_the_folds_is_rejected() -> None:
    with pytest.raises(ValueError, match="cannot form"):
        _study(list(range(3)), n_folds=5)._build_folds()


def test_negative_embargo_rejected() -> None:
    with pytest.raises(ValueError):
        _study(list(range(50)), embargo=-1)


def test_sharpe_uses_the_requested_periods_per_year() -> None:
    returns = np.array([0.01, -0.005, 0.02, 0.0])
    base = float(np.mean(returns) / np.std(returns))
    assert _sharpe(returns, 365.0) == pytest.approx(base * np.sqrt(365.0))


def test_objective_annualises_with_study_periods_per_year() -> None:
    returns = np.array([0.01, -0.005, 0.02, 0.0])
    study = WalkForwardStudy(
        study_name="t",
        train_fn=lambda *a: returns,
        data=list(range(50)),
        n_folds=2,
        periods_per_year=1.0,
    )
    trial = MagicMock()
    trial.should_prune.return_value = False
    assert study._objective(trial) == pytest.approx(float(np.mean(returns) / np.std(returns)))


def test_failed_fold_prunes_instead_of_scoring_minus_999() -> None:
    """Would fail before the fix: the failure was averaged in as -999.0."""

    def boom(*_a: object) -> np.ndarray:
        raise RuntimeError("transient")

    study = WalkForwardStudy(study_name="t", train_fn=boom, data=list(range(50)), n_folds=2)
    trial = MagicMock()
    trial.should_prune.return_value = False
    with pytest.raises(optuna.exceptions.TrialPruned):
        study._objective(trial)
