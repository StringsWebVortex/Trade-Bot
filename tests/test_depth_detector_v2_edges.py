"""Edge-case coverage for src/regime/depth_detector_v2.py.

Complements tests/test_depth_detector_v2.py (which covers the main fit/
predict path) with the error and fallback branches: the no-matching-columns
guard, the empty-slice guard, the non-"full" covariance branches of
_assign_labels, and the except-return-0.0 paths in the ADX/BB helpers.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

from src.regime.depth_detector_v2 import (
    FEATURE_COLS_V2,
    DepthDetectorV2,
    _compute_adx,
    _compute_bb_width,
    build_v2_features_from_engine_outputs,
)


def test_fit_raises_when_no_feature_columns_match():
    detector = DepthDetectorV2()
    with pytest.raises(ValueError, match="No matching feature columns"):
        detector.fit(pd.DataFrame({"totally_unrelated": [1.0, 2.0]}))


def test_predict_before_fit_returns_neutral_default():
    detector = DepthDetectorV2()
    pred = detector.predict(pd.DataFrame({"adx_14": [20.0]}))
    from src.engines.consensus import REGIME_WEIGHTS

    assert pred.label == "Unknown"
    assert pred.confidence == 0.0
    assert pred.weight_vector == REGIME_WEIGHTS["Transition"]
    assert len(pred.weight_vector) == 18
    assert pred.raw_state == 0


def test_predict_with_empty_frame_returns_neutral_default():
    detector = DepthDetectorV2()
    # Model and scaler present, but the slice has no rows -> second guard.
    detector._model = MagicMock()
    detector._scaler = MagicMock()
    pred = detector.predict(pd.DataFrame({"adx_14": []}))
    assert pred.confidence == 0.0
    assert pred.label == "Unknown"


def test_load_returns_false_when_artifacts_absent(tmp_path: Path):
    detector = DepthDetectorV2()
    assert detector.load(tmp_path) is False


def test_model_stem_is_stable_and_symbol_specific():
    a = DepthDetectorV2(symbol="BTC/USDT", timeframe="1h")
    b = DepthDetectorV2(symbol="BTC/USDT", timeframe="1h")
    c = DepthDetectorV2(symbol="ETH/USDT", timeframe="1h")
    assert a._model_stem() == b._model_stem()
    assert a._model_stem() != c._model_stem()
    assert len(a._model_stem()) == 8


def _fake_hmm(covariance_type: str, covars, means=None) -> MagicMock:
    model = MagicMock()
    model.covariance_type = covariance_type
    model.covars_ = covars
    model.means_ = means if means is not None else np.zeros((9, 3))
    model.predict_proba.return_value = np.eye(9)[np.repeat(np.arange(9), 10)]
    return model


def test_assign_labels_full_covariance_ranks_by_trace():
    detector = DepthDetectorV2()
    # 9 states, ascending trace; unsupported specialist labels are never invented.
    covars = np.array([np.eye(2) * (i + 1) for i in range(9)])
    labels = detector._assign_labels(
        _fake_hmm("full", covars), np.zeros((90, 2)), list(FEATURE_COLS_V2[:2])
    )
    assert labels[0] == "Ranging"
    assert labels[8] == "Volatile"
    specialist_labels = {
        "Accumulation",
        "OptionsDriven",
        "MacroDominated",
        "LiquidityCrisis",
        "Capitulation",
    }
    assert not set(labels.values()).intersection(specialist_labels)


def test_assign_labels_diag_covariance_uses_sum():
    detector = DepthDetectorV2()
    covars = np.array([[float(i + 1), float(i + 1)] for i in range(9)])
    labels = detector._assign_labels(
        _fake_hmm("diag", covars), np.zeros((90, 2)), FEATURE_COLS_V2[:2]
    )
    assert len(labels) == 9
    assert labels[0] == "Ranging"
    specialist_labels = {
        "Accumulation",
        "OptionsDriven",
        "MacroDominated",
        "LiquidityCrisis",
        "Capitulation",
    }
    assert not set(labels.values()).intersection(specialist_labels)


def test_assign_labels_tied_covariance_falls_back_to_mean_variance():
    detector = DepthDetectorV2()
    means = np.array([[float(i), float(i) * 2.0, 0.0] for i in range(9)])
    labels = detector._assign_labels(
        _fake_hmm("tied", np.eye(3), means=means), np.zeros((90, 3)), list(FEATURE_COLS_V2[:3])
    )
    assert len(labels) == 9
    assert set(labels.values()).issubset({"Ranging", "Transition", "Trending", "Volatile"})
    assert len(set(labels.values())) >= 2


def test_compute_adx_returns_zero_for_short_series():
    s = pd.Series([1.0, 2.0])
    assert _compute_adx(s, s, s, period=14) == 0.0


def test_compute_adx_returns_zero_on_exception():
    # Long enough to clear the length guard, but the arithmetic inside raises
    # on non-numeric data -- the except branch must swallow it, not propagate.
    bad = pd.Series(["a"] * 30)
    assert _compute_adx(bad, bad, bad) == 0.0


def test_compute_adx_normal_series_in_range():
    n = 60
    close = pd.Series(np.linspace(100, 130, n))
    high = close + 1.0
    low = close - 1.0
    adx = _compute_adx(high, low, close)
    assert 0.0 <= adx <= 100.0


def test_compute_bb_width_returns_zero_for_short_series():
    assert _compute_bb_width(pd.Series([1.0, 2.0]), period=20) == 0.0


def test_compute_bb_width_returns_zero_on_exception():
    # Clears the length guard, then rolling().mean() raises on non-numeric data.
    assert _compute_bb_width(pd.Series(["a"] * 30)) == 0.0


def test_compute_bb_width_normal_series_is_positive():
    close = pd.Series(np.random.default_rng(0).normal(100, 5, 60))
    assert _compute_bb_width(close) > 0.0


def test_compute_bb_width_flat_series_is_zero():
    close = pd.Series([100.0] * 60)
    assert _compute_bb_width(close) == 0.0


def test_predict_with_missing_trained_feature_returns_unknown() -> None:
    detector = DepthDetectorV2()
    detector._model = MagicMock()
    detector._scaler = MagicMock()
    detector._feature_cols = ["e01_confidence"]
    pred = detector.predict(pd.DataFrame({"unrelated": [1.0]}))
    assert pred.label == "Unknown"
    assert pred.confidence == 0.0


def test_predict_with_expected_but_empty_feature_column_returns_unknown() -> None:
    detector = DepthDetectorV2()
    detector._model = MagicMock()
    detector._scaler = MagicMock()
    detector._feature_cols = ["adx_14"]
    pred = detector.predict(pd.DataFrame({"adx_14": []}))
    assert pred.label == "Unknown"
    assert pred.confidence == 0.0


def test_load_rejects_invalid_label_metadata(tmp_path: Path) -> None:
    from unittest.mock import patch

    import joblib

    detector = DepthDetectorV2()
    stem = detector._model_stem()
    names = (
        f"{stem}_hmm9.pkl",
        f"{stem}_scaler9.pkl",
        f"{stem}_labels9.pkl",
        f"{stem}_features9.pkl",
    )
    for name in names:
        (tmp_path / name).touch()
    with (
        patch("src.regime.detector._verify_manifest"),
        patch.object(
            joblib, "load", side_effect=[MagicMock(), MagicMock(), [], list(FEATURE_COLS_V2)]
        ),
    ):
        assert detector.load(tmp_path) is False


def test_assign_labels_uses_broad_fallback_for_low_confidence_rows() -> None:
    detector = DepthDetectorV2()
    covars = np.array([np.eye(12) * (i + 1) for i in range(9)])
    model = _fake_hmm("full", covars)
    model.predict_proba.return_value = np.full((90, 9), 1.0 / 9.0)
    labels = detector._assign_labels(model, np.zeros((90, 12)), list(FEATURE_COLS_V2))
    assert len(labels) == 9
    assert labels[0] == "Ranging"
    assert labels[8] == "Volatile"
    assert set(labels.values()).issubset({"Ranging", "Transition", "Volatile"})


def test_assign_labels_requires_expected_posterior_shape() -> None:
    detector = DepthDetectorV2()
    covars = np.array([np.eye(12) * (i + 1) for i in range(9)])
    model = _fake_hmm("full", covars)
    model.predict_proba.return_value = np.ones((1, 9))
    with pytest.raises(ValueError, match="unexpected shape"):
        detector._assign_labels(model, np.zeros((90, 12)), list(FEATURE_COLS_V2))


def test_assign_labels_emits_specialist_labels_only_with_feature_evidence() -> None:
    detector = DepthDetectorV2()
    covars = np.array([np.eye(12) * (i + 1) for i in range(9)])
    model = _fake_hmm("full", covars)
    model.predict_proba.return_value = np.eye(9)[np.repeat(np.arange(9), 5)]
    matrix = np.zeros((45, len(FEATURE_COLS_V2)))
    columns = {name: index for index, name in enumerate(FEATURE_COLS_V2)}

    def evidence(state: int, feature: str, value: float) -> None:
        matrix[state * 5 : (state + 1) * 5, columns[feature]] = value

    evidence(0, "e05_net_flow", -1.0)
    evidence(0, "e14_contrarian_signal", 1.0)
    evidence(0, "e17_amihud_ratio", 0.8)
    evidence(1, "e17_amihud_ratio", 1.0)
    evidence(2, "e13_contagion_score", 1.0)
    evidence(3, "e12_gex", 1.0)
    evidence(4, "e05_net_flow", 1.0)
    evidence(5, "adx_14", 1.0)
    evidence(6, "e03_entropy_score", 1.0)

    labels = detector._assign_labels(model, matrix, list(FEATURE_COLS_V2))
    assert labels[0] == "Capitulation"
    assert labels[1] == "LiquidityCrisis"
    assert labels[2] == "MacroDominated"
    assert labels[3] == "OptionsDriven"
    assert labels[4] == "Accumulation"
    assert labels[5] == "Trending"
    assert labels[6] == "Transition"


def test_build_features_reads_e01_confidence_metadata() -> None:
    from datetime import UTC, datetime

    from src.engines.schema import EngineOutput

    output = EngineOutput(
        engine_id="E-01",
        symbol="BTC/USDT",
        timestamp_utc=datetime.now(UTC),
        predicted_price=50_000.0,
        confidence=0.73,
        direction=1,
        horizon_hours=4,
        metadata={},
    )
    frame = build_v2_features_from_engine_outputs({"E-01": output})
    assert frame["e01_confidence"].iloc[0] == pytest.approx(0.73)
