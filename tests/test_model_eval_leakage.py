"""
Regression tests for the model-evaluation leakage findings INT-001..INT-005, INT-007.

REG-1100 INT-001  OOS metrics are scored on the forward label return
REG-1101 INT-002  the ensemble regresses on the forward label return
REG-1102 INT-003  meta-labels come from out-of-fold primary predictions
REG-1103 INT-004  CPCV purges/embargoes every contiguous test block
REG-1104 INT-005  CPCV counts each test sample once
REG-1105 INT-007  ensemble member scores are out-of-sample
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from src.config import FeatureSettings, XGBoostSettings
from src.features.pipeline import BASE_FEATURE_COLUMNS, FeatureMatrix, build_feature_matrix
from src.intelligence.ensemble_predictor import (
    EnsemblePredictor,
    TreeEnsemblePredictor,
    XGBoostPredictor,
)
from src.models.trainer import (
    ModelTrainer,
    build_cpcv_folds,
    collapse_oos_predictions,
    evaluation_returns,
    oos_sharpe_and_drawdown,
)

FEATURES = list(BASE_FEATURE_COLUMNS)

_XGB = XGBoostSettings(n_estimators=10, max_depth=2, early_stopping_rounds=5)
_FEAT = FeatureSettings(
    cpcv_n_splits=4,
    cpcv_n_test_splits=2,
    purge_gap_bars=2,
    embargo_pct=0.01,
    triple_barrier_max_holding_bars=2,
)


def _trainer() -> ModelTrainer:
    return ModelTrainer("BTC/USDT", "15m", xgb_cfg=_XGB, feature_cfg=_FEAT)


def _fm(n: int = 400, seed: int = 1, noise_labels: bool = False) -> FeatureMatrix:
    rng = np.random.default_rng(seed)
    idx = pd.RangeIndex(n)
    feats = pd.DataFrame(rng.standard_normal((n, len(FEATURES))), columns=FEATURES, index=idx)
    if noise_labels:
        labels = pd.Series(rng.integers(0, 2, n).astype(np.int8), index=idx)
    else:
        labels = pd.Series((feats[FEATURES[0]] > 0).astype(np.int8), index=idx)
    return FeatureMatrix(
        features=feats,
        labels=labels,
        meta=None,
        daily_vol=pd.Series(0.02, index=idx),
        log_returns=pd.Series(rng.standard_normal(n) * 0.01, index=idx),
        dropped_rows=0,
        forward_returns=pd.Series(rng.standard_normal(n) * 0.05, index=idx),
    )


# --------------------------------------------------------------------------- INT-001


def _bars(n: int = 800) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    close = pd.Series(30000 + np.cumsum(rng.standard_normal(n) * 50), dtype=np.float64)
    return pd.DataFrame(
        {
            "open": close * 0.999,
            "high": close + np.abs(rng.standard_normal(n) * 30),
            "low": close - np.abs(rng.standard_normal(n) * 30),
            "close": close,
            "volume": np.abs(rng.standard_normal(n) * 100 + 500),
        }
    )


def test_pipeline_forward_returns_follow_the_label_not_the_bar():
    fm = build_feature_matrix(_bars())
    assert fm.forward_returns is not None
    assert fm.forward_returns.index.equals(fm.labels.index)
    assert fm.forward_returns.notna().all()
    # A profit-take label means the price ROSE to the exit, a stop-loss that it FELL.
    assert (fm.forward_returns[fm.labels == 1] > 0).all()
    assert (fm.forward_returns[fm.labels == 0] < 0).all()
    # And it is not the concurrent bar return.
    assert not np.allclose(fm.forward_returns.to_numpy(), fm.log_returns.to_numpy())


def test_oos_scoring_uses_forward_returns():
    fm = _fm()
    assert np.array_equal(evaluation_returns(fm), fm.forward_returns.to_numpy())
    seen: list[np.ndarray] = []

    import src.models.trainer as trainer_mod

    real = trainer_mod.oos_sharpe_and_drawdown

    def spy(y_pred, rets, **kw):
        seen.append(np.asarray(rets))
        return real(y_pred, rets, **kw)

    with patch.object(trainer_mod, "oos_sharpe_and_drawdown", side_effect=spy):
        _trainer().train_direction(fm)
    pool = np.concatenate(seen)
    assert np.isin(pool, fm.forward_returns.to_numpy()).all()
    assert not np.isin(pool, fm.log_returns.to_numpy()).any()


# --------------------------------------------------------------------------- INT-002


def test_ensemble_is_trained_on_forward_returns():
    fm = _fm()
    captured: dict[str, pd.Series] = {}

    def fake_fit(self, X, y, label_horizon=0):
        captured["y"] = y
        captured["h"] = label_horizon

    with patch.object(EnsemblePredictor, "fit", fake_fit):
        _trainer().train_ensemble(fm)
    assert np.array_equal(captured["y"].to_numpy(), fm.forward_returns.to_numpy())
    assert captured["h"] == _FEAT.triple_barrier_max_holding_bars


# --------------------------------------------------------------------------- INT-003


def test_meta_labels_use_out_of_fold_predictions():
    # Labels are pure noise: an out-of-fold primary model agrees with them about half
    # the time, while an in-sample one (deep, many trees) agrees far more often.
    fm = _fm(n=400, noise_labels=True)
    trainer = ModelTrainer(
        "BTC/USDT",
        "15m",
        xgb_cfg=XGBoostSettings(n_estimators=60, max_depth=5, early_stopping_rounds=5),
        feature_cfg=_FEAT,
    )
    _x, meta_y, keep = trainer._meta_dataset(fm, FEATURES)
    assert keep.sum() == len(meta_y) > 200
    assert meta_y.mean() < 0.65


def test_train_meta_label_never_consults_the_in_sample_direction_model():
    fm = _fm()
    boom = MagicMock()
    boom.predict_proba.side_effect = AssertionError("in-sample primary predictions used")
    result = _trainer().train_meta_label(fm, boom)
    boom.predict_proba.assert_not_called()
    assert result.model is not None


# --------------------------------------------------------------------------- INT-004


@pytest.mark.parametrize("purge_gap,embargo_pct", [(5, 0.01), (8, 0.02)])
def test_cpcv_purges_and_embargoes_every_test_block(purge_gap, embargo_pct):
    n = 1000
    folds = build_cpcv_folds(n, 10, 2, purge_gap, embargo_pct)
    embargo = max(1, int(n * embargo_pct))
    non_adjacent = 0
    for fold in folds:
        test = np.unique(fold.test_idx)
        starts = test[np.r_[True, np.diff(test) > 1]]
        ends = test[np.r_[np.diff(test) > 1, True]]
        if len(starts) > 1:
            non_adjacent += 1
        train = set(fold.train_idx.tolist())
        for bs, be in zip(starts, ends, strict=True):
            before = set(range(max(0, bs - purge_gap), bs))
            after = set(range(be + 1, min(n, be + 1 + embargo)))
            assert not (train & before), f"fold {fold.fold_id}: train inside purge zone"
            assert not (train & after), f"fold {fold.fold_id}: train inside embargo zone"
    assert non_adjacent > 0


# --------------------------------------------------------------------------- INT-005


def test_collapse_counts_each_sample_once_and_votes():
    idx = [np.array([0, 1, 2]), np.array([1, 2, 3]), np.array([2, 3, 4])]
    ret = [np.array([0.1, 0.2, 0.3]), np.array([0.2, 0.3, 0.4]), np.array([0.3, 0.4, 0.5])]
    pred = [np.array([1, 1, 0]), np.array([1, 0, 0]), np.array([0, 0, 0])]
    r, p = collapse_oos_predictions(idx, ret, pred)
    assert r.tolist() == pytest.approx([0.1, 0.2, 0.3, 0.4, 0.5])
    assert p.tolist() == [1, 1, 0, 0, 0]  # sample 1: votes 1,1 -> long; sample 2: 0,0,0 -> short


def test_sharpe_does_not_grow_with_duplicated_samples():
    rng = np.random.default_rng(3)
    ret = rng.standard_normal(200) * 0.01 + 0.001
    pred = (rng.random(200) > 0.4).astype(int)
    one, _ = oos_sharpe_and_drawdown(pred, ret, periods_per_year=1000.0)
    nine, _ = oos_sharpe_and_drawdown(np.tile(pred, 9), np.tile(ret, 9), periods_per_year=1000.0)
    assert nine == pytest.approx(one, rel=0.01)


def test_n_trades_counts_unique_test_samples():
    n = 400
    result = _trainer().train_direction(_fm(n=n))
    # 4 groups, 2 test groups per fold: every sample is tested in 3 folds.
    assert sum(f.n_test for f in result.fold_metrics) > n
    assert 0 < result.n_trades <= n


# --------------------------------------------------------------------------- INT-007


def test_ensemble_member_scores_are_out_of_sample():
    rng = np.random.default_rng(0)
    n = 200
    X = pd.DataFrame(rng.standard_normal((n, 4)), columns=list("abcd"))
    y = pd.Series(rng.standard_normal(n) * 0.01)  # unpredictable from X
    ep = EnsemblePredictor()
    ep.models = {"xgboost": XGBoostPredictor(), "tree_ensemble": TreeEnsemblePredictor()}
    ep.fit(X, y, label_horizon=3)
    for name, member in ep.models.items():
        assert member.is_fitted
        # In-sample these fit noise far below its std; out of sample they cannot.
        assert member.rmse > 0.8 * y.std(), name
    assert sum(ep.weights.values()) == pytest.approx(1.0)


def test_ensemble_without_holdout_data_gets_no_optimistic_score(tmp_path):
    rng = np.random.default_rng(1)
    X = pd.DataFrame(rng.standard_normal((20, 3)), columns=list("abc"))
    y = pd.Series(rng.standard_normal(20))
    ep = EnsemblePredictor()
    ep.models = {"xgboost": XGBoostPredictor()}
    ep.fit(X, y)
    assert ep.models["xgboost"].rmse == np.inf
    assert ep.weights["xgboost"] == 0.0
    with pytest.raises(RuntimeError, match="no ensemble member has a valid out-of-sample score"):
        ep.predict(pd.DataFrame(rng.standard_normal((1, 3)), columns=list("abc")))
    ep.save(tmp_path, "BTC/USDT", "15m")
    restored = EnsemblePredictor.load(tmp_path, "BTC/USDT", "15m")
    assert restored.weights["xgboost"] == 0.0
    with pytest.raises(RuntimeError, match="no ensemble member has a valid out-of-sample score"):
        restored.predict(pd.DataFrame(rng.standard_normal((1, 3)), columns=list("abc")))
