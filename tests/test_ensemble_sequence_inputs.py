"""Ensemble sequence members consume the realised return window at inference.

Decides:
  - REG-1714 — ARIMA and the LSTM forecast from the realised closed-bar
    log-return window, never from the tabular feature row, and abstain
    (raise, so the ensemble excludes them) when that window is missing,
    too short or non-finite.
"""

from __future__ import annotations

from contextlib import nullcontext
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from src.intelligence.ensemble_predictor import (
    ARIMAPredictor,
    EnsemblePredictor,
    LSTMPredictor,
)

_ROW = pd.DataFrame({"a": [0.3], "b": [-1.2], "c": [7.0]})


def _returns(n: int, seed: int = 7) -> np.ndarray:
    return np.random.default_rng(seed).standard_normal(n) * 0.01


@pytest.fixture(scope="module")
def fitted_arima() -> ARIMAPredictor:
    pytest.importorskip("statsmodels")
    p = ARIMAPredictor()
    p.fit(pd.Series(_returns(80)))
    assert p.model is not None
    return p


class _Recorder:
    """Stands in for the fitted torch net and records what it was fed."""

    def __init__(self) -> None:
        self.inputs: list[np.ndarray] = []

    def eval(self) -> None:
        pass

    def __call__(self, tensor: np.ndarray) -> SimpleNamespace:
        self.inputs.append(np.asarray(tensor))
        return SimpleNamespace(numpy=lambda: np.array([[float(np.asarray(tensor).sum())]]))


def _lstm_with_recorder(lookback: int = 5) -> tuple[LSTMPredictor, _Recorder]:
    p = LSTMPredictor(hidden_dim=4, lookback=lookback, epochs=1)
    recorder = _Recorder()
    p.model = recorder
    return p, recorder


_FAKE_TORCH = SimpleNamespace(
    torch=SimpleNamespace(
        no_grad=nullcontext,
        tensor=lambda values, dtype=None: np.asarray(values),
        float32=np.float32,
    )
)


@pytest.fixture
def fake_torch():
    with (
        patch("src.intelligence.ensemble_predictor._torch_installed", return_value=True),
        patch("src.intelligence.ensemble_predictor._load_torch_runtime", return_value=_FAKE_TORCH),
    ):
        yield


# ---------------------------------------------------------------------------
# LSTM
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("fake_torch")
@pytest.mark.parametrize("n_features", [1, 3, 20, 26])
def test_lstm_input_is_the_last_lookback_returns_for_any_feature_count(n_features: int) -> None:
    p, recorder = _lstm_with_recorder(lookback=5)
    row = pd.DataFrame([np.arange(n_features, dtype=float)])
    window = _returns(9)

    p.predict(row, recent_returns=window)

    (fed,) = recorder.inputs
    assert fed.shape == (1, 5, 1)
    np.testing.assert_allclose(fed.ravel(), window[-5:])


@pytest.mark.usefixtures("fake_torch")
def test_lstm_forecast_moves_with_the_window_not_the_row() -> None:
    p, _ = _lstm_with_recorder(lookback=5)
    window = _returns(5)
    first = p.predict(_ROW, recent_returns=window)
    assert p.predict(_ROW * 100.0, recent_returns=window) == first
    assert p.predict(_ROW, recent_returns=window + 0.01) != first


@pytest.mark.usefixtures("fake_torch")
@pytest.mark.parametrize(
    "window",
    [None, _returns(4), np.r_[_returns(4), np.nan], np.r_[_returns(2), np.inf, _returns(2)]],
    ids=["missing", "short", "nan", "inf"],
)
def test_lstm_abstains_without_a_full_finite_window(window) -> None:
    p, recorder = _lstm_with_recorder(lookback=5)
    with pytest.raises(ValueError, match="lstm"):
        p.predict(_ROW, recent_returns=window)
    assert recorder.inputs == []


@pytest.mark.usefixtures("fake_torch")
def test_lstm_ignores_a_bad_value_older_than_its_lookback() -> None:
    p, recorder = _lstm_with_recorder(lookback=5)
    window = np.r_[np.nan, _returns(5)]
    p.predict(_ROW, recent_returns=window)
    np.testing.assert_allclose(recorder.inputs[0].ravel(), window[-5:])


# ---------------------------------------------------------------------------
# ARIMA
# ---------------------------------------------------------------------------


def test_arima_forecast_moves_with_new_observations(fitted_arima: ARIMAPredictor) -> None:
    window = _returns(40, seed=3)
    first = fitted_arima.predict(_ROW, recent_returns=window)
    again = fitted_arima.predict(_ROW, recent_returns=window)
    moved = fitted_arima.predict(_ROW, recent_returns=np.r_[window, 0.05])

    assert np.isfinite(first)
    assert again == first
    assert moved != first


def test_arima_keeps_the_fitted_parameters() -> None:
    p = ARIMAPredictor()
    p.model = MagicMock()
    p.model.apply.return_value.forecast.return_value = np.array([0.004])
    window = _returns(25)

    assert p.predict(_ROW, recent_returns=window) == pytest.approx(0.004)

    args, kwargs = p.model.apply.call_args
    np.testing.assert_allclose(args[0], window)
    assert kwargs == {"refit": False}
    p.model.forecast.assert_not_called()


@pytest.mark.parametrize(
    "window",
    [None, _returns(ARIMAPredictor.min_window - 1), np.r_[_returns(30), np.nan]],
    ids=["missing", "short", "nan"],
)
def test_arima_abstains_without_a_full_finite_window(window) -> None:
    p = ARIMAPredictor()
    p.model = MagicMock()
    with pytest.raises(ValueError, match="arima"):
        p.predict(_ROW, recent_returns=window)
    p.model.apply.assert_not_called()


# ---------------------------------------------------------------------------
# Ensemble wiring
# ---------------------------------------------------------------------------


class _TabularMember:
    rmse = 0.1
    model = object()
    is_fitted = True

    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def predict_with_uncertainty(self, features: pd.DataFrame) -> tuple[float, float]:
        self.calls.append((features,))
        return 0.01, self.rmse

    def get_performance_metrics(self) -> dict[str, float]:
        return {"rmse": self.rmse}


def _ensemble(arima: ARIMAPredictor) -> tuple[EnsemblePredictor, _TabularMember]:
    tabular = _TabularMember()
    ens = EnsemblePredictor()
    ens.models = {"arima": arima, "xgboost": tabular}
    ens._update_weights()
    return ens, tabular


def test_ensemble_excludes_sequence_members_without_a_window(
    fitted_arima: ARIMAPredictor,
) -> None:
    ens, tabular = _ensemble(fitted_arima)

    result = ens.predict(_ROW)

    assert result.failed_models == ("arima",)
    assert set(result.individual_predictions) == {"xgboost"}
    assert len(tabular.calls) == 1


def test_ensemble_routes_the_window_to_sequence_members_only(
    fitted_arima: ARIMAPredictor,
) -> None:
    ens, tabular = _ensemble(fitted_arima)
    window = _returns(40, seed=5)

    result = ens.predict(_ROW, recent_returns=window)

    assert result.failed_models == ()
    assert result.individual_predictions["arima"] == pytest.approx(
        fitted_arima.predict(_ROW, recent_returns=window)
    )
    (call,) = tabular.calls
    assert len(call) == 1  # the tabular member never sees the window
