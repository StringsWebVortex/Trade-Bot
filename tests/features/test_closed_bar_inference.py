"""REG-1070 / REG-1071: live inference reads the latest closed bar; forming candles never stored."""

from __future__ import annotations

from datetime import UTC, datetime

from src.config import TIMEFRAME_SECONDS, Timeframe
from src.data.fetcher import _raw_to_bar_records
from src.features.pipeline import build_feature_matrix, build_inference_features
from tests.features.test_feature_determinism import make_bars


def test_fast_path_scores_last_input_bar():
    """DAT-001: the fast path returned the last *labelled* (older) row, chosen by later prices.

    Fails before the fix because the newest bars cannot have hit a barrier and
    were absent from ``fm.features``.
    """
    bars = make_bars()
    fm = build_feature_matrix(bars)
    assert fm.features.index[-1] != bars.index[-1]  # labelled frame is stale
    assert fm.features_all is not None
    assert fm.features_all.index[-1] == bars.index[-1]
    vec = build_inference_features(bars, feature_matrix=fm)
    assert vec is not None
    assert vec.equals(fm.features_all.iloc[-1].astype("float64"))


def test_fast_path_refuses_stale_row():
    """DAT-001: if the matrix does not end at the last bar, inference is refused."""
    bars = make_bars()
    fm = build_feature_matrix(bars.iloc[:-5])
    assert build_inference_features(bars, feature_matrix=fm) is None


def test_forming_candle_dropped_from_raw_rows():
    """DAT-002: an open candle returned by fetch_ohlcv must not become a BarRecord."""
    tf_ms = TIMEFRAME_SECONDS[Timeframe.INTRADAY] * 1000
    now_ms = int(datetime.now(tz=UTC).timestamp() * 1000)
    closed_ts = (now_ms // tf_ms - 1) * tf_ms
    forming_ts = (now_ms // tf_ms) * tf_ms
    raw = [
        [closed_ts, 1, 2, 0.5, 1.5, 10],
        [forming_ts, 1.5, 1.6, 1.4, 1.55, 1],
    ]
    out = _raw_to_bar_records("BTC/USDT", Timeframe.INTRADAY.value, raw)
    assert [b.ts for b in out] == [closed_ts]
