"""Regression tests for the standalone crypto-predictor research package.

Covers: forming candles dropped by both fetchers (SCR-007); unlabelable tail
rows kept as NaN instead of fabricated "down" labels (SCR-008); the training
purge gap, non-overlapping P&L with horizon-correct annualisation, and
time-ordered calibration folds (DOC-014). Network is replaced by fakes.

Decides:
  - REG-1280 — Standalone predictor drops the still-forming candle
  - REG-1281 — Predictor labels never fabricate a down move for unlabelable tail rows
  - REG-1282 — Walk-forward training purges labels that overlap the test window
  - REG-1283 — Backtest P&L uses non-overlapping holds and horizon-correct annualisation
  - REG-1284 — Probability calibration folds are time-ordered
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit

PKG = Path(__file__).resolve().parents[1] / "crypto-predictor"
sys.path.insert(0, str(PKG))

import backtest  # noqa: E402
import data_fetch  # noqa: E402
import data_fetch_kraken  # noqa: E402
from indicators import forward_direction_label  # noqa: E402

import risk  # noqa: E402


class _Resp:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def _binance_row(open_ms: int, close_ms: int, close: str) -> list:
    return [open_ms, "1", "1", "1", close, "1", close_ms, "0", 0, "0", "0", "0"]


def test_binance_drops_the_still_open_candle(monkeypatch):
    now_ms = int(time.time() * 1000)
    hour = 3_600_000
    closed_open = now_ms - 2 * hour
    forming_open = now_ms - 1 * hour // 2
    raw = [
        _binance_row(closed_open, closed_open + hour - 1, "100"),
        _binance_row(forming_open, forming_open + hour - 1, "101"),
    ]
    monkeypatch.setattr(data_fetch.requests, "get", lambda *a, **k: _Resp(raw))

    df = data_fetch.fetch_ohlcv("BTCUSDT", "1h", 2)

    assert len(df) == 1
    assert df["close"].iloc[-1] == 100.0


def test_kraken_drops_the_uncommitted_last_entry(monkeypatch):
    rows = [
        [1_700_000_000, "1", "2", "0.5", "100", "1", "1", 5],
        [1_700_003_600, "1", "2", "0.5", "110", "1", "1", 5],
        [1_700_007_200, "1", "2", "0.5", "120", "1", "1", 5],
    ]
    payload = {"error": [], "result": {"XXBTZUSD": rows, "last": 1_700_007_200}}
    monkeypatch.setattr(data_fetch_kraken.requests, "get", lambda *a, **k: _Resp(payload))

    df = data_fetch_kraken.fetch_ohlcv("XBTUSD", "1h")

    assert list(df["close"]) == [100.0, 110.0]
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]


def test_forward_label_is_nan_where_no_future_close_exists():
    close = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

    label = forward_direction_label(close, horizon=2)

    assert list(label.iloc[:4]) == [1.0, 1.0, 1.0, 1.0]
    assert label.iloc[4:].isna().all()


def test_walk_forward_purges_the_last_horizon_rows_before_each_test(monkeypatch):
    horizon = 4
    n = 40
    data = pd.DataFrame(
        {
            "f1": np.arange(n, dtype=float),
            "label": np.arange(n) % 2,
            "future_return": np.full(n, 0.01),
        }
    )
    folds: list[tuple[pd.Index, pd.Index]] = []

    class _FakeModel:
        def __init__(self, **kwargs):
            pass

        def fit(self, X, y):
            pass

    def _fake_calibrate(model, X_train, y_train, X_test, method):
        folds.append((X_train.index, X_test.index))
        return np.full(len(X_test), 0.5), None

    monkeypatch.setattr(backtest, "XGBClassifier", _FakeModel)
    monkeypatch.setattr(backtest, "calibrate_probabilities", _fake_calibrate)

    backtest.walk_forward_backtest(data, train_window=10, test_window=5, horizon=horizon)

    assert folds, "expected at least one walk-forward fold"
    for train_idx, test_idx in folds:
        # Row i is labelled with the close at i + horizon, so no training label
        # may reach into the test block.
        assert train_idx.max() + horizon < test_idx.min()
        assert len(train_idx) == 10 - horizon


def test_evaluate_compounds_non_overlapping_periods_only():
    n = 8
    results = pd.DataFrame(
        {
            "pred": np.ones(n, dtype=int),
            "label": np.ones(n, dtype=int),
            "position_size": np.full(n, 0.1),
            "future_return": np.full(n, 0.01),
        },
        index=pd.RangeIndex(n),
    )
    cost = backtest.FEE_RATE + backtest.SLIPPAGE_RATE

    metrics = backtest.evaluate(results, horizon=4)

    # Two non-overlapping 4-candle holds, not eight overlapping ones.
    expected_pct = ((1 + 0.1 * (0.01 - cost)) ** 2 - 1) * 100
    assert metrics["n_trades"] == 2
    assert metrics["total_return_pct"] == pytest.approx(expected_pct)


def test_evaluate_annualises_by_the_holding_period():
    horizon = 4
    future = np.array([0.02, 0, 0, 0, 0.01, 0, 0, 0])
    results = pd.DataFrame(
        {
            "pred": np.ones(8, dtype=int),
            "label": np.ones(8, dtype=int),
            "position_size": np.full(8, 0.1),
            "future_return": future,
        },
        index=pd.RangeIndex(8),
    )
    cost = backtest.FEE_RATE + backtest.SLIPPAGE_RATE
    sim = np.array([0.1 * (0.02 - cost), 0.1 * (0.01 - cost)])

    metrics = backtest.evaluate(results, horizon=horizon)

    expected = sim.mean() / sim.std(ddof=1) * np.sqrt(365 * 24 / horizon)
    assert metrics["sharpe"] == pytest.approx(expected)


def test_calibration_uses_time_ordered_folds(monkeypatch):
    seen: dict = {}

    class _SpyCalibrated(risk.CalibratedClassifierCV):
        def __init__(self, *args, **kwargs):
            seen.update(kwargs)
            super().__init__(*args, **kwargs)

    monkeypatch.setattr(risk, "CalibratedClassifierCV", _SpyCalibrated)
    n = 60
    X = pd.DataFrame({"x": np.arange(n, dtype=float)})
    y = pd.Series(np.arange(n) % 2)

    probs, _ = risk.calibrate_probabilities(
        LogisticRegression(), X, y, X.iloc[:5], method="sigmoid"
    )

    assert isinstance(seen["cv"], TimeSeriesSplit)
    assert probs.shape == (5,)
