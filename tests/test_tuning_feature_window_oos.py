"""STR-06: the feature-window backtest scores only bars after the model's
training end, so the "oos_sharpe" is not computed on training data.

Decides:
  - REG-1112 -- Feature-window backtest excludes bars the frozen model was trained on
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from xgboost import XGBClassifier

from src.config import FeatureSettings
from src.features.pipeline import FEATURE_COLUMNS
from src.tuning import backtest_harness
from src.tuning.backtest_harness import run_feature_window_backtest

_CFG = FeatureSettings(cpcv_n_splits=10, purge_gap_bars=1, triple_barrier_max_holding_bars=1)


def _bars(n: int = 1000) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    close = 100.0 * np.cumprod(1.0 + rng.normal(0.0002, 0.01, n))
    high = close * (1.0 + np.abs(rng.normal(0.0, 0.002, n)))
    low = close * (1.0 - np.abs(rng.normal(0.0, 0.002, n)))
    open_ = np.concatenate(([close[0]], close[:-1]))
    idx = (np.arange(n) * 900_000).astype(np.int64)
    return pd.DataFrame(
        {
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": rng.uniform(50.0, 150.0, n),
        },
        index=idx,
    )


def _model() -> XGBClassifier:
    rng = np.random.default_rng(0)
    X = rng.standard_normal((300, len(FEATURE_COLUMNS)))
    model = XGBClassifier(n_estimators=3, max_depth=2, verbosity=0)
    model.fit(X, (X[:, 0] > 0).astype(int))
    return model


def _run(monkeypatch: pytest.MonkeyPatch, oos_start_ms: int | None) -> list[pd.Index]:
    seen: list[pd.Index] = []

    def spy(_model: object, features: pd.DataFrame) -> np.ndarray:
        seen.append(features.index)
        return np.ones(len(features), dtype=int)

    monkeypatch.setattr(backtest_harness, "_predict_direction_batch", spy)
    run_feature_window_backtest(
        _bars(),
        field_name="atr_window",
        champion_window=14,
        challenger_window=17,
        direction_model=_model(),
        features_cfg=_CFG,
        oos_start_ms=oos_start_ms,
    )
    return seen


def test_only_bars_after_training_end_are_scored(monkeypatch: pytest.MonkeyPatch) -> None:
    """Would fail before the fix: every bar, including training bars, was scored."""
    cutoff = 400 * 900_000
    scored = _run(monkeypatch, cutoff)
    assert scored
    for index in scored:
        assert len(index) > 0
        assert int(index.min()) > cutoff


def test_bars_all_before_training_end_leave_nothing_to_score(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative case: a model trained through the last bar has no OOS data, so
    the backtest refuses to produce a verdict instead of scoring in-sample."""
    with pytest.raises(ValueError):
        _run(monkeypatch, 10**12)
