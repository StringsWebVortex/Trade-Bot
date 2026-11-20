"""
Walk-Forward Sharpe Optimization via Optuna.

Implements a rolling walk-forward study that:
  1. Splits historical data into N_FOLDS anchored train/test windows
  2. For each trial, trains a new model with sampled hyperparams on train
  3. Evaluates out-of-sample Sharpe on test window
  4. Reports the mean OOS Sharpe as the objective

Sampler: TPESampler
Pruner:  HyperbandPruner (prune trials that look unpromising early)

The best hyperparameters are stored in the Optuna study (SQLite-backed)
and can be retrieved with best_params().
"""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import structlog

log: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

_STORAGE_PATH = Path(os.environ.get("OPTUNA_STORAGE", "./models/optuna_studies.db"))
_STUDY_PREFIX = "crypto_intel_wf"
_N_FOLDS = 5
_TRAIN_RATIO = 0.7
# Hourly crypto bars: 365 days x 24. Callers on other bar sizes pass their own.
_DEFAULT_PERIODS_PER_YEAR = 365.0 * 24.0
_DEFAULT_EMBARGO = 1


_DEFAULT_PARAMS: dict[str, Any] = {
    "lr": 1e-3,
    "batch_size": 64,
    "dropout": 0.1,
    "weight_decay": 1e-4,
    "n_layers": 2,
    "n_heads": 8,
}


@dataclass
class WFParams:
    """Hyperparameter search space boundaries."""

    lr_min: float = 1e-5
    lr_max: float = 1e-2
    batch_size_choices: tuple[int, ...] = (32, 64, 128, 256)
    dropout_min: float = 0.0
    dropout_max: float = 0.5
    weight_decay_min: float = 1e-6
    weight_decay_max: float = 1e-2
    n_layers_min: int = 1
    n_layers_max: int = 4
    n_heads_min: int = 2
    n_heads_max: int = 16


def _sharpe(returns: np.ndarray, periods_per_year: float = 252.0) -> float:
    """Annualized Sharpe ratio from a returns array.

    `periods_per_year` is the number of return observations per year; the
    default 252 is the equity-daily convention and is wrong for crypto
    (365 days, intraday bars), so WalkForwardStudy always passes its own.
    """
    if np.asarray(returns).size == 0:
        return 0.0  # np.std([]) is nan, and `nan < 1e-9` is False — guard explicitly
    std = float(np.std(returns))
    if std < 1e-9:
        return 0.0
    return float(np.mean(returns) / std * np.sqrt(periods_per_year))


class WalkForwardStudy:
    """
    Optuna walk-forward hyper-parameter optimization.

    The objective function is provided by the caller as a callable
    (train_fn) that receives hyperparams + train/test data and returns
    an array of OOS returns. This keeps the study agnostic to model type.

    train_fn signature:
        (params: dict, X_train, y_train, X_test, y_test, trial) -> np.ndarray
    """

    def __init__(
        self,
        study_name: str,
        train_fn: Callable,
        data: Any,
        n_trials: int = 100,
        n_folds: int = _N_FOLDS,
        storage_path: Path = _STORAGE_PATH,
        wf_params: WFParams | None = None,
        embargo: int = _DEFAULT_EMBARGO,
        periods_per_year: float = _DEFAULT_PERIODS_PER_YEAR,
    ) -> None:
        # embargo: rows dropped between the end of train and the start of
        # test. Set it to at least the label horizon in bars, or labels
        # computed from future bars leak across the boundary (MTH-009).
        if embargo < 0:
            raise ValueError(f"embargo must be >= 0, got {embargo}")
        if periods_per_year <= 0:
            raise ValueError(f"periods_per_year must be > 0, got {periods_per_year}")
        self._embargo = embargo
        self._periods_per_year = periods_per_year
        self._study_name = f"{_STUDY_PREFIX}_{study_name}"
        self._train_fn = train_fn
        self._data = data
        self._n_trials = n_trials
        self._n_folds = n_folds
        self._storage_path = storage_path
        self._wf_params = wf_params or WFParams()
        self._study: Any = None

    def _build_folds(self) -> list[tuple[Any, Any, Any, Any]]:
        """Split data into walk-forward train/test folds."""
        n = len(self._data)
        min_rows = self._n_folds * (self._embargo + 2)
        if n < min_rows:
            raise ValueError(
                f"{n} rows cannot form {self._n_folds} folds with embargo={self._embargo} "
                f"(need >= {min_rows})"
            )
        fold_size = n // self._n_folds
        folds = []
        for i in range(self._n_folds):
            # The last fold absorbs the n % n_folds remainder instead of dropping it.
            end = n if i == self._n_folds - 1 else (i + 1) * fold_size
            train_end = int(end * _TRAIN_RATIO)
            test_start = train_end + self._embargo
            if test_start >= end:
                raise ValueError(f"fold {i} has an empty test window after embargo")
            X_train = self._data[:train_end]
            y_train = self._data[:train_end]  # caller is responsible for splitting X/y
            X_test = self._data[test_start:end]
            y_test = self._data[test_start:end]
            folds.append((X_train, y_train, X_test, y_test))
        return folds

    def _objective(self, trial: Any) -> float:
        """Optuna objective: mean OOS Sharpe across walk-forward folds."""
        wp = self._wf_params
        params: dict[str, Any] = {
            "lr": trial.suggest_float("lr", wp.lr_min, wp.lr_max, log=True),
            "batch_size": trial.suggest_categorical("batch_size", list(wp.batch_size_choices)),
            "dropout": trial.suggest_float("dropout", wp.dropout_min, wp.dropout_max),
            "weight_decay": trial.suggest_float(
                "weight_decay", wp.weight_decay_min, wp.weight_decay_max, log=True
            ),
            "n_layers": trial.suggest_int("n_layers", wp.n_layers_min, wp.n_layers_max),
            "n_heads": trial.suggest_int("n_heads", wp.n_heads_min, wp.n_heads_max),
        }

        folds = self._build_folds()
        fold_sharpes = []
        for fold_idx, (X_train, y_train, X_test, y_test) in enumerate(folds):
            try:
                oos_returns = self._train_fn(params, X_train, y_train, X_test, y_test, trial)
                s = _sharpe(np.array(oos_returns), self._periods_per_year)
                fold_sharpes.append(s)
                trial.report(float(np.mean(fold_sharpes)), step=fold_idx)
                if trial.should_prune():
                    raise __import__("optuna").exceptions.TrialPruned()
            except __import__("optuna").exceptions.TrialPruned:
                raise
            except Exception as exc:
                # A failed fold is not a -999 Sharpe: averaged in, one
                # transient error would swamp the TPE signal. Prune instead.
                log.warning("wf_fold_failed", fold=fold_idx, exc=str(exc))
                raise __import__("optuna").exceptions.TrialPruned() from exc

        return float(np.mean(fold_sharpes))

    def run(self) -> dict[str, Any]:
        """
        Run the Optuna study and return best parameters.

        Creates or loads an existing SQLite-backed study so trials
        are resumable across restarts.
        """
        try:
            import optuna  # type: ignore[import]

            optuna.logging.set_verbosity(optuna.logging.WARNING)
            storage = f"sqlite:///{self._storage_path}"
            sampler = optuna.samplers.TPESampler(seed=42)
            pruner = optuna.pruners.HyperbandPruner(
                min_resource=1,
                max_resource=self._n_folds,
                reduction_factor=3,
            )
            self._study = optuna.create_study(
                study_name=self._study_name,
                storage=storage,
                load_if_exists=True,
                direction="maximize",
                sampler=sampler,
                pruner=pruner,
            )
            self._study.optimize(self._objective, n_trials=self._n_trials, show_progress_bar=False)
            try:
                best = self._study.best_params
            except ValueError:
                # Every trial was pruned (e.g. every fold failed): no result.
                log.warning("optuna_no_completed_trials_returning_defaults")
                return dict(_DEFAULT_PARAMS)
            log.info("optuna_study_complete", best_sharpe=self._study.best_value, best_params=best)
            return best

        except ImportError:
            log.warning("optuna_not_installed_returning_defaults")
            return dict(_DEFAULT_PARAMS)

    def best_params(self) -> dict[str, Any]:
        """Return best params from the most recent study (or empty dict if not run)."""
        if self._study is None:
            return {}
        try:
            return self._study.best_params
        except Exception:
            return {}
