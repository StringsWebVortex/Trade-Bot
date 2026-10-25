"""Regression tests for the data-layer audit findings DAT-007 .. DAT-017.

Each test names the finding it decides. They fail against the pre-fix code:
the failure mode is stated in the docstring so deleting one loses something.
"""

from __future__ import annotations

import asyncio
import math
import threading
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# DAT-007: Timescale persists/returns V6 fields, validates keys, resets created_at
# ---------------------------------------------------------------------------


class _Conn:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple]] = []

    async def execute(self, query, *params):
        self.calls.append((query, params))
        return "INSERT 0 1"

    async def fetch(self, query, *params):
        self.calls.append((query, params))
        return []


class _Acquire:
    def __init__(self, conn: _Conn) -> None:
        self._conn = conn

    async def __aenter__(self) -> _Conn:
        return self._conn

    async def __aexit__(self, *exc) -> bool:
        return False


class _Pool:
    def __init__(self, conn: _Conn) -> None:
        self._conn = conn

    def acquire(self) -> _Acquire:
        return _Acquire(self._conn)


def _ts_backend(conn: _Conn):
    import structlog

    from src.data.timescale_storage import TimescaleBackend

    backend = TimescaleBackend.__new__(TimescaleBackend)
    backend._pool = _Pool(conn)
    backend._require_pool = lambda: backend._pool
    backend._log = structlog.get_logger("test")
    return backend


def test_timescale_store_writes_v6_fields_dat007() -> None:
    """Pre-fix the Timescale store silently dropped every *_v6 key."""
    conn = _Conn()
    backend = _ts_backend(conn)
    asyncio.run(
        backend.store_intelligence_features(
            "BTCUSDT",
            "1h",
            1,
            {"direction_v6": 1.0, "algo_v6": "x", "freshness_seconds_v6": 3, "ofi_v6": 0.5},
            0.9,
        )
    )
    [(sql, params)] = conn.calls
    assert "direction_v6" in sql and "algo_v6" in sql
    assert 1 in params and "x" in params and "3" in params and 0.5 in params
    # integer column gets an int, text column gets a str (asyncpg is strict)
    assert any(type(p) is int and p == 1 for p in params)


def test_timescale_store_rejects_unknown_keys_like_sqlite_dat007() -> None:
    conn = _Conn()
    backend = _ts_backend(conn)
    with pytest.raises(ValueError, match="unsupported intelligence feature columns"):
        asyncio.run(backend.store_intelligence_features("BTCUSDT", "1h", 1, {"bogus": 1.0}, 0.5))
    assert conn.calls == []


def test_timescale_fetch_selects_v6_fields_dat007() -> None:
    conn = _Conn()
    backend = _ts_backend(conn)
    asyncio.run(backend.fetch_intelligence_features("BTCUSDT", "1h"))
    [(sql, _)] = conn.calls
    assert "direction_v6" in sql and "model_versions_v6" in sql


def test_backends_share_one_intelligence_allowlist_dat007() -> None:
    from src.data import storage, timescale_storage

    assert timescale_storage.INTELLIGENCE_FEATURE_KEYS is storage.INTELLIGENCE_FEATURE_KEYS
    assert len(storage.INTELLIGENCE_V6_KEYS) == 17


def test_timescale_model_metrics_upsert_resets_created_at_dat007() -> None:
    """SQLite INSERT OR REPLACE resets created_at; PG DO UPDATE must too."""
    from src.data.storage import ModelMetricsRecord

    conn = _Conn()
    backend = _ts_backend(conn)
    rec = ModelMetricsRecord(
        model_name="direction",
        timeframe="1h",
        version="v1",
        oos_sharpe=1.0,
        max_drawdown=0.1,
        n_trades=10,
        accuracy=0.5,
        precision_score=0.5,
        recall_score=0.5,
        f1_score=0.5,
        live_gate_pass=False,
    )
    asyncio.run(backend.insert_model_metrics(rec))
    [(sql, _)] = conn.calls
    assert "created_at=" in sql


# ---------------------------------------------------------------------------
# DAT-009: Deribit loop survives disk/loop errors; HTTP status is checked
# ---------------------------------------------------------------------------


def test_deribit_persist_error_does_not_lose_data_dat009(tmp_path: Path) -> None:
    from src.data.deribit_provider import DeribitProvider

    p = DeribitProvider(data_root=tmp_path)
    frame = pd.DataFrame({"iv": [1.0]})
    with (
        patch.object(p, "_fetch_chain", AsyncMock(return_value=frame)),
        patch.object(p, "_persist", side_effect=OSError("disk full")),
    ):
        result = asyncio.run(p.fetch("BTC/USDT"))
    assert result is frame


def test_deribit_run_loop_survives_a_failed_cycle_dat009(tmp_path: Path) -> None:
    """Pre-fix one exception ended polling permanently."""
    from src.data.deribit_provider import DeribitProvider

    p = DeribitProvider(data_root=tmp_path)
    fetch = AsyncMock(side_effect=[RuntimeError("boom"), asyncio.CancelledError()])
    with (
        patch.object(p, "fetch", fetch),
        patch("src.data.deribit_provider.asyncio.sleep", AsyncMock()),
        pytest.raises(asyncio.CancelledError),
    ):
        asyncio.run(p.run_loop("BTC/USDT"))
    assert fetch.await_count == 2


def test_deribit_http_error_status_is_not_parsed_as_empty_result_dat009() -> None:
    from src.data.deribit_provider import DeribitProvider

    resp = AsyncMock()
    resp.raise_for_status = MagicMock(side_effect=RuntimeError("429"))
    resp.json = AsyncMock(return_value={"result": {"mark_iv": 1.0}})
    resp.__aenter__ = AsyncMock(return_value=resp)
    resp.__aexit__ = AsyncMock(return_value=False)
    session = MagicMock()
    session.get = MagicMock(return_value=resp)
    assert asyncio.run(DeribitProvider()._get_orderbook(session, "X")) is None
    resp.json.assert_not_awaited()


# ---------------------------------------------------------------------------
# DAT-010: macro date is the market date; stale cache files are ignored
# ---------------------------------------------------------------------------


def _yf(frame: pd.DataFrame) -> MagicMock:
    return MagicMock(**{"download.return_value": frame})


def test_macro_date_is_last_market_date_not_fetch_date_dat010(tmp_path: Path) -> None:
    from src.data.macro_provider import MacroProvider

    idx = pd.date_range("2020-01-01", periods=3, freq="D")
    frame = pd.DataFrame({"Close": [100.0, 101.0, 102.0]}, index=idx)
    with patch.dict("sys.modules", {"yfinance": _yf(frame)}):
        row = MacroProvider(data_root=tmp_path)._fetch_sync()
    assert row is not None
    assert row["date"] == "2020-01-03"


def test_macro_one_column_close_frame_is_squeezed_dat010(tmp_path: Path) -> None:
    """Newer yfinance returns Close as a one-column frame (MultiIndex)."""
    from src.data.macro_provider import MacroProvider

    idx = pd.date_range("2024-01-01", periods=4, freq="D")
    cols = pd.MultiIndex.from_tuples([("Close", "^GSPC")])
    frame = pd.DataFrame([[100.0], [101.0], [102.0], [103.0]], index=idx, columns=cols)
    with patch.dict("sys.modules", {"yfinance": _yf(frame)}):
        row = MacroProvider(data_root=tmp_path)._fetch_sync()
    assert row is not None
    assert row["spx_close"] == 103.0
    assert all(isinstance(v, float) for v in row["spx_series"])


def test_macro_cache_ignores_files_older_than_the_stale_limit_dat010(tmp_path: Path) -> None:
    from src.data.macro_provider import MacroProvider

    d = tmp_path / "macro"
    d.mkdir()
    pd.DataFrame([{"date": "2020-01-01", "spx_close": 1.0}]).to_parquet(d / "2020-01-01.parquet")
    assert MacroProvider(data_root=tmp_path)._load_cached() is None


# ---------------------------------------------------------------------------
# DAT-011: RSS headlines are deduplicated and carry pubDate
# ---------------------------------------------------------------------------

_RSS = """<?xml version="1.0"?><rss><channel>
<item><title>Bitcoin up</title><guid>g1</guid><pubDate>Mon, 06 Jan 2020 10:00:00 GMT</pubDate></item>
<item><title>Ether flat</title><guid>g2</guid></item>
</channel></rss>"""


def _rss_session() -> MagicMock:
    resp = AsyncMock()
    resp.text = AsyncMock(return_value=_RSS)
    resp.__aenter__ = AsyncMock(return_value=resp)
    resp.__aexit__ = AsyncMock(return_value=False)
    session = AsyncMock()
    session.get = MagicMock(return_value=resp)
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=False)
    return session


def test_rss_repeat_poll_does_not_duplicate_headlines_dat011(tmp_path: Path) -> None:
    from src.data.sentiment_provider import SentimentProvider

    p = SentimentProvider(data_root=tmp_path)

    async def _go() -> None:
        with patch("aiohttp.ClientSession", return_value=_rss_session()):
            await p._fetch_rss()
            first = len(p._headlines)
            await p._fetch_rss()
        assert len(p._headlines) == first == 4  # 2 items x 2 sources, once

    asyncio.run(_go())
    parts = list((tmp_path / "sentiment").glob("*.parquet"))
    assert sum(len(pd.read_parquet(f)) for f in parts) == 4


def test_rss_timestamp_is_pubdate_when_present_dat011() -> None:
    from src.data.sentiment_provider import SentimentProvider

    p = SentimentProvider()
    rows = p._parse_rss(_RSS, "src", p._get_vader())
    by_title = {r["headline"]: r for r in rows}
    assert by_title["Bitcoin up"]["timestamp_utc"].isoformat().startswith("2020-01-06T10:00:00")
    assert by_title["Ether flat"]["timestamp_utc"].year >= 2024  # fetch-time fallback


# ---------------------------------------------------------------------------
# DAT-012: DuckDBStore serialises concurrent writers
# ---------------------------------------------------------------------------


def test_duckdb_store_concurrent_writes_are_all_kept_dat012(tmp_path: Path) -> None:
    """Same-ms writes used to overwrite each other and threads interleaved
    begin/commit on one connection."""
    from src.data.duckdb_store import DuckDBStore

    store = DuckDBStore(path=tmp_path / "t.duckdb")
    errors: list[BaseException] = []

    def _work() -> None:
        try:
            for _ in range(10):
                store.write_horizon_metric(1, "h", 1.0, 0.5, 1)
        except BaseException as exc:  # noqa: BLE001 - surfaced by the assertion below
            errors.append(exc)

    threads = [threading.Thread(target=_work) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert errors == []
    assert len(store.query_horizon_history(1, limit=1000)) == 40
    store.close()


def test_duckdb_feature_log_accepts_none_values_dat012(tmp_path: Path) -> None:
    from src.data.duckdb_store import DuckDBStore

    store = DuckDBStore(path=tmp_path / "t.duckdb")
    store.write_feature_log("BTC", {"a": None, "b": 1.5})  # float(None) used to raise
    store.close()


# ---------------------------------------------------------------------------
# DAT-013: Granger uses Bonferroni and evicts stale results
# ---------------------------------------------------------------------------


def _noise_pair(n: int = 200, seed: int = 11):
    rng = np.random.default_rng(seed)
    return rng.normal(0, 0.01, n), 100.0 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))


def test_granger_pvalue_is_bonferroni_corrected_dat013() -> None:
    from src.causal import granger as g

    def _fake(_df, maxlag):
        return {lag: ({"ssr_ftest": (2.0, 0.02 if lag == 3 else 0.5, 1, 1)},) for lag in range(1, maxlag + 1)}

    btc, alt = _noise_pair()
    det = g.GrangerCausalityDetector(max_lag=5)
    with patch("statsmodels.tsa.stattools.grangercausalitytests", _fake):
        res = det.update(btc, {"ETH": alt})
    assert res["ETH"].best_lag == 3
    assert res["ETH"].min_pvalue == pytest.approx(0.10)  # 0.02 * 5 lags
    assert res["ETH"].is_causal is False  # raw 0.02 would have passed at 0.05


def test_granger_failed_symbol_is_evicted_dat013() -> None:
    from src.causal import granger as g

    btc, alt = _noise_pair()
    det = g.GrangerCausalityDetector()
    det._results["ETH"] = g.GrangerResult("BTC", "ETH", True, 0.001, 1, 9.0)
    with patch("statsmodels.tsa.stattools.grangercausalitytests", side_effect=ValueError("x")):
        det.update(btc, {"ETH": alt})
    assert "ETH" not in det._results


def test_granger_aligns_labelled_series_on_timestamp_dat013() -> None:
    """ALT history ending earlier than BTC must not be tail-aligned."""
    from src.causal import granger as g

    seen: dict = {}

    def _spy(df, maxlag):
        seen["df"] = df
        return {lag: ({"ssr_ftest": (1.0, 0.9, 1, 1)},) for lag in range(1, maxlag + 1)}

    rng = np.random.default_rng(5)
    idx_btc = pd.date_range("2024-01-01", periods=200, freq="h")
    btc = pd.Series(rng.normal(0, 0.01, 200), index=idx_btc)
    idx_alt = idx_btc[:150]  # alt stopped 50 bars earlier
    alt = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, 150))), index=idx_alt)
    with patch("statsmodels.tsa.stattools.grangercausalitytests", _spy):
        g.GrangerCausalityDetector(window=500).update(btc, {"ETH": alt})
    df = seen["df"]
    assert df.index.max() <= idx_alt[-1]
    np.testing.assert_allclose(df["btc"].to_numpy(), btc.loc[df.index].to_numpy())


# ---------------------------------------------------------------------------
# DAT-015: DepthDetectorV2 verifies a sha256 manifest before unpickling
# ---------------------------------------------------------------------------


def _saved_detector(tmp_path: Path):
    from src.regime.depth_detector_v2 import DepthDetectorV2

    d = DepthDetectorV2()
    d._model = {"m": 1}
    d._scaler = {"s": 1}
    d._state_to_label = {0: "Trending"}
    d.save(tmp_path)
    return d


def test_depth_v2_round_trip_with_manifest_dat015(tmp_path: Path) -> None:
    from src.regime.depth_detector_v2 import DepthDetectorV2

    _saved_detector(tmp_path)
    fresh = DepthDetectorV2()
    assert fresh.load(tmp_path) is True
    assert fresh._state_to_label == {0: "Trending"}


def test_depth_v2_refuses_tampered_pickle_dat015(tmp_path: Path) -> None:
    from src.regime.depth_detector_v2 import DepthDetectorV2

    _saved_detector(tmp_path)
    victim = next(tmp_path.glob("*_scaler9.pkl"))
    victim.write_bytes(victim.read_bytes() + b"tamper")
    fresh = DepthDetectorV2()
    assert fresh.load(tmp_path) is False
    assert fresh._scaler is None


def test_depth_v2_refuses_pickles_without_manifest_dat015(tmp_path: Path) -> None:
    from src.regime.depth_detector_v2 import DepthDetectorV2

    _saved_detector(tmp_path)
    for m in tmp_path.glob("*.sha256"):
        m.unlink()
    assert DepthDetectorV2().load(tmp_path) is False


# ---------------------------------------------------------------------------
# DAT-016: GARCH refit must converge; pipeline guard includes garch_window
# ---------------------------------------------------------------------------


def test_garch_non_converged_fit_is_not_used_dat016() -> None:
    from src.regime import garch

    rng = np.random.default_rng(1)
    rets = pd.Series(rng.normal(0, 0.01, 120))
    bad = MagicMock(success=False, message="abnormal", x=np.array([1e-6, 0.1, 0.8]))
    with patch.object(garch, "minimize", return_value=bad):
        out = garch.rolling_garch_forecast(rets, window=60)
    assert out.iloc[60:].isna().all()


def test_build_feature_matrix_min_rows_includes_garch_window_dat016() -> None:
    import inspect

    from src.features import pipeline

    src = inspect.getsource(pipeline.build_feature_matrix)
    head = src.split("if n_input < min_required", 1)[0]
    assert "cfg.garch_window" in head


# ---------------------------------------------------------------------------
# DAT-017: no fabricated Fear & Greed before the first fetch
# ---------------------------------------------------------------------------


def test_sentiment_cache_not_published_before_fear_greed_fetch_dat017(tmp_path: Path) -> None:
    from src.data.sentiment_provider import SentimentProvider

    p = SentimentProvider(data_root=tmp_path)
    assert math.isnan(p.latest_fg()[0])
    p._headlines = [{"headline": "a", "vader_compound": 0.3}]
    with patch("src.data.provider_cache.get_provider_cache") as get_cache:
        p._update_cache()
    get_cache.return_value.set_sentiment.assert_not_called()
