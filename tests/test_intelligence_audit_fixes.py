"""Regression tests for the Phase 5 intelligence audit fixes (INT-008, INT-012..INT-026).

Decides: REG-1340, REG-1341, REG-1342, REG-1343, REG-1344, REG-1345, REG-1346, REG-1347, REG-1348, REG-1349, REG-1350, REG-1351, REG-1352, REG-1353, REG-1354"""

from __future__ import annotations

import asyncio
import inspect
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import numpy as np
import pandas as pd
import pytest
import structlog

# ---------------------------------------------------------------------------
# INT-026 / INT-025: trainer
# ---------------------------------------------------------------------------


def test_int026_sample_weights_have_mean_one() -> None:
    from src.models.trainer import compute_sample_weights

    w = compute_sample_weights(pd.Series(np.linspace(-0.02, 0.02, 1800)))
    assert w.mean() == pytest.approx(1.0)
    assert w.sum() == pytest.approx(1800.0)


def test_int025_final_model_refit_on_all_rows_with_purge(monkeypatch) -> None:
    from src.models import trainer

    made: list[SimpleNamespace] = []

    class FakeModel:
        best_iteration = 7

        def __init__(self) -> None:
            self.fit_rows = None
            self.eval_set = None
            self.params: dict = {}
            made.append(self)  # type: ignore[arg-type]

        def fit(self, x, y, sample_weight=None, eval_set=None, verbose=False):
            self.fit_rows = len(x)
            self.eval_set = eval_set

        def set_params(self, **kw):
            self.params.update(kw)

    monkeypatch.setattr(trainer, "_build_xgb", lambda cfg, scale_pos_weight=1.0: FakeModel())
    n = 200
    x = np.zeros((n, 3))
    # Both the fit and early-stopping slices need both classes for the probe
    # path to be exercised; production intentionally skips probing otherwise.
    y = np.tile(np.array([0.0, 1.0]), n // 2)
    w = np.ones(n)
    cfg = SimpleNamespace(n_estimators=500)
    final = trainer._fit_final_xgb(cfg, x, y, w, 1.0, purge_gap=10)
    probe, refit = made
    assert probe.eval_set is not None
    assert probe.fit_rows == int(n * 0.85) - 10  # purge gap before the eval slice
    assert final is refit
    assert refit.fit_rows == n  # newest bars are in the final fit
    assert refit.params["n_estimators"] == 8
    assert refit.params["early_stopping_rounds"] is None


# ---------------------------------------------------------------------------
# INT-012 / INT-013: on-chain base
# ---------------------------------------------------------------------------


def _fake_session(payloads: list[dict]):
    calls = {"n": 0}

    class Resp:
        def __init__(self, data):
            self._d = data

        def raise_for_status(self):
            return None

        async def json(self, content_type=None):
            return self._d

    class Ctx:
        def __init__(self, data):
            self._r = Resp(data)

        async def __aenter__(self):
            return self._r

        async def __aexit__(self, *a):
            return False

    class Session:
        def get(self, url, headers=None, params=None):
            data = payloads[min(calls["n"], len(payloads) - 1)]
            calls["n"] += 1
            return Ctx(data)

    return Session(), calls


def test_int012_uncached_get_sees_state_change() -> None:
    from src.intelligence.onchain.defillama_provider import DeFiLlamaProvider

    async def run():
        prov = DeFiLlamaProvider(cache_ttl_s=3600)
        prov._limiter.acquire = AsyncMock()
        session, calls = _fake_session([{"state": "PENDING"}, {"state": "COMPLETED"}])
        prov._ensure_session = AsyncMock(return_value=session)
        first = await prov._get("http://x/execution/1/results", use_cache=False)
        second = await prov._get("http://x/execution/1/results", use_cache=False)
        return first, second, calls["n"]

    first, second, n = asyncio.run(run())
    assert first == {"state": "PENDING"}
    assert second == {"state": "COMPLETED"}
    assert n == 2


def test_int012_default_get_still_caches() -> None:
    from src.intelligence.onchain.defillama_provider import DeFiLlamaProvider

    async def run():
        prov = DeFiLlamaProvider(cache_ttl_s=3600)
        prov._limiter.acquire = AsyncMock()
        session, calls = _fake_session([{"a": 1}, {"a": 2}])
        prov._ensure_session = AsyncMock(return_value=session)
        await prov._get("http://x/y")
        await prov._get("http://x/y")
        return calls["n"]

    assert asyncio.run(run()) == 1


@pytest.mark.parametrize(
    ("module", "cls", "args"),
    [
        ("defillama_provider", "DeFiLlamaProvider", {}),
        ("dune_provider", "DuneProvider", {"api_key": "k"}),
        ("arkham_provider", "ArkhamProvider", {"api_key": "k"}),
        ("cryptoquant_provider", "CryptoQuantProvider", {"api_key": "k"}),
        ("coinglass_provider", "CoinglassProvider", {"api_key": "k"}),
    ],
)
def test_int013_configured_cache_ttl_reaches_cache(module, cls, args) -> None:
    import importlib

    mod = importlib.import_module(f"src.intelligence.onchain.{module}")
    prov = getattr(mod, cls)(cache_ttl_s=7, **args)
    assert prov._async_cache._default_ttl == 7


# ---------------------------------------------------------------------------
# INT-014: MVRV contribution
# ---------------------------------------------------------------------------


def test_int014_mvrv_contribution_survives_validate_then_merge() -> None:
    from src.intelligence.onchain.schema import merge_onchain_results, validate_provider_result

    raw = {
        "exchange_stress_score": 0.2,
        "exchange_stress_score_mvrv_contrib": 0.3,
        "confidence": 1.0,
        "timestamp": 1.0,
    }
    clean = validate_provider_result(raw, "cq")
    merged = merge_onchain_results([clean])
    assert merged["exchange_stress_score"] == pytest.approx(0.5)
    assert "exchange_stress_score_mvrv_contrib" not in merged


def test_int014_missing_realized_cap_gives_zero_contribution() -> None:
    from src.intelligence.onchain.cryptoquant_provider import _mvrv_stress_contrib

    assert _mvrv_stress_contrib({"data": [{"market_cap": 1e12}]}) == 0.0
    assert _mvrv_stress_contrib({"data": [{"market_cap": 1e12, "realized_cap": 0}]}) == 0.0


# ---------------------------------------------------------------------------
# INT-015: uncalibrated status explicit
# ---------------------------------------------------------------------------


def test_int015_stress_model_declares_uncalibrated_and_has_no_dead_intercepts() -> None:
    from src.intelligence.probabilistic import BayesianExchangeStressModel

    m = BayesianExchangeStressModel()
    assert m.CALIBRATED is False
    assert all(set(v) == {"slope"} for v in m.indicator_weights.values())
    doc = BayesianExchangeStressModel.__doc__ or ""
    assert "UNCALIBRATED" in doc
    assert "Training data" not in doc


# ---------------------------------------------------------------------------
# INT-016 / INT-017 / INT-008: intel.py, adapter, orchestrator
# ---------------------------------------------------------------------------


def test_int016_result_collection_runs_off_the_event_loop() -> None:
    from src.intel import CryptoIntelligence

    assert "asyncio.to_thread" in inspect.getsource(CryptoIntelligence.on_bar)


def test_int017_no_default_btc_rpc_credentials(monkeypatch) -> None:
    from src.intel import resolve_btc_rpc
    from src.workers.orchestrator import WorkerOrchestrator

    monkeypatch.delenv("BTC_RPC_USER", raising=False)
    monkeypatch.delenv("BTC_RPC_PASS", raising=False)
    _, user, password = resolve_btc_rpc({"btc_node_rpc": {"url": "http://h:1"}})
    assert (user, password) == ("", "")
    assert "crypto" not in inspect.getsource(resolve_btc_rpc)
    assert WorkerOrchestrator(n_workers=2)._ecc_enabled is False
    monkeypatch.setenv("BTC_RPC_USER", "u")
    monkeypatch.setenv("BTC_RPC_PASS", "p")
    assert resolve_btc_rpc({})[1:] == ("u", "p")


def test_int008_adapter_forwards_risk_context() -> None:
    from src.intelligence.intelligence_adapter import IntelligenceAdapter

    intel = SimpleNamespace(on_bar=AsyncMock(return_value=None))
    adapter = IntelligenceAdapter(intel, MagicMock())
    ctx = {"atr": 0.01}
    asyncio.run(
        adapter.on_bar(
            symbol="BTC/USDT",
            timeframe="1m",
            bar_ts_ms=60_000,
            ohlcv={"close": 1.0},
            risk_context=ctx,
        )
    )
    assert intel.on_bar.await_args.kwargs["risk_context"] is ctx


def _risk_ctx_orchestrator(n_trades: int, n_bars: int = 20):
    from src.engine import orchestrator as om

    orch = object.__new__(om.Orchestrator)
    orch._symbol = "BTC/USDT"
    orch._primary_tf = om.Timeframe.SCALPING
    orch._log = structlog.get_logger("test")
    orch._cfg = SimpleNamespace(trading_mode=SimpleNamespace(value="paper"))
    bars = [
        SimpleNamespace(high=101.0 + i * 0.1, low=99.0 + i * 0.1, close=100.0 + i * 0.1 * (-1) ** i)
        for i in range(n_bars)
    ]
    trades = [SimpleNamespace(pnl_usd=2.0 if i % 2 == 0 else -1.0) for i in range(n_trades)]
    orch._storage = SimpleNamespace(
        latest_bar_ts=AsyncMock(return_value=1_000_000),
        fetch_bars=AsyncMock(return_value=bars),
        fetch_trades=AsyncMock(return_value=trades),
    )
    executor = SimpleNamespace(
        drawdown_tracker=SimpleNamespace(drawdown_from_peak_pct=-5.0),
        get_risk_snapshot=AsyncMock(return_value=(9_900.0, 10_000.0, -100.0)),
    )
    orch._executor_for = lambda tf: executor
    return orch, om


def test_int008_orchestrator_builds_validated_risk_context() -> None:
    from src.intel import _validated_risk_context

    orch, om = _risk_ctx_orchestrator(60)
    ctx = asyncio.run(orch._intelligence_risk_context(om.Timeframe.SCALPING))
    assert ctx is not None
    assert ctx["drawdown"] == pytest.approx(0.05)
    assert ctx["daily_loss"] == pytest.approx(0.01)
    assert ctx["odds"] == pytest.approx(2.0)
    import time

    values, err = _validated_risk_context(ctx, now=time.time(), max_age_seconds=30.0)
    assert err is None
    assert values is not None


def test_int008_risk_context_is_none_without_enough_trades_or_bars() -> None:
    orch, om = _risk_ctx_orchestrator(10)
    assert asyncio.run(orch._intelligence_risk_context(om.Timeframe.SCALPING)) is None
    orch, om = _risk_ctx_orchestrator(60, n_bars=5)
    assert asyncio.run(orch._intelligence_risk_context(om.Timeframe.SCALPING)) is None


def test_int008_process_bar_passes_risk_context_to_adapter() -> None:
    from src.engine.orchestrator import Orchestrator

    src = inspect.getsource(Orchestrator._process_intelligence_bar)
    assert "risk_context=risk_context" in src


# ---------------------------------------------------------------------------
# INT-018 / INT-019: client
# ---------------------------------------------------------------------------


def _agg():
    from src.intelligence.client import IntelligenceAggregator

    s = MagicMock()
    s.glassnode_api_key = "k"
    s.cryptoquant_api_key = "k"
    s.cache_ttl_onchain_seconds = 300
    s.cache_ttl_exchange_seconds = 60
    s.glassnode_base_url = "https://api.glassnode.com/v1/metrics"
    s.glassnode_rate_limit_seconds = 0.0
    s.funding_rate_perp_symbol = "BTCUSDT"
    return IntelligenceAggregator(_settings=s)


def _patch_httpx(monkeypatch, data):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json = MagicMock(return_value=data)
    client = AsyncMock()
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=False)
    client.get = AsyncMock(return_value=resp)
    monkeypatch.setattr("httpx.AsyncClient", lambda *a, **k: client)


def test_int018_netflow_history_zscore_is_trailing_only(monkeypatch) -> None:
    base = [1.0, 2.0, 1.0, 2.0, 1.0, 2.0]
    data = [{"t": 1000 + i, "v": v} for i, v in enumerate(base)]
    _patch_httpx(monkeypatch, data)
    out_a = asyncio.run(_agg().get_exchange_netflow_history("BTC", since_ts=1, until_ts=9))
    # change only the FUTURE tail; earlier z-scores must not move
    data2 = data[:5] + [{"t": 1005, "v": 1000.0}]
    _patch_httpx(monkeypatch, data2)
    out_b = asyncio.run(_agg().get_exchange_netflow_history("BTC", since_ts=1, until_ts=9))
    assert [r["tscore"] for r in out_a[:5]] == [r["tscore"] for r in out_b[:5]]
    assert out_a[0]["tscore"] is None  # no history yet -> missing, not 0.0


def test_int018_whale_history_uses_sorted_series_and_live_definition(monkeypatch) -> None:
    vals = [1.0, 1.0, 1.0, 1.0, 1.0, 4.0, 4.0]
    data = [{"t": 1000 + i, "v": v} for i, v in enumerate(vals)]
    shuffled = list(reversed(data))
    _patch_httpx(monkeypatch, shuffled)
    out = asyncio.run(_agg().get_whale_activity_history("BTC", since_ts=1))
    assert [r["ts"] for r in out] == sorted(r["ts"] for r in out)
    # last bar: recent = [4, 4], prior = [1]*5 -> ratio 4
    assert out[-1]["ratio"] == pytest.approx(4.0)


def test_int019_failures_without_cache_are_missing_not_zero() -> None:
    agg = _agg()
    agg._fetch_glassnode_netflow = AsyncMock(side_effect=RuntimeError("x"))
    agg._fetch_glassnode_whale_activity = AsyncMock(side_effect=RuntimeError("x"))
    agg._fetch_cryptoquant_funding_rate = AsyncMock(side_effect=RuntimeError("x"))
    assert asyncio.run(agg.get_exchange_netflow("BTC")) is None
    assert asyncio.run(agg.get_whale_activity("BTC")) is None
    assert asyncio.run(agg.get_funding_rate()) is None


def test_int019_rate_limiter_stamps_before_request_and_is_locked() -> None:
    agg = _agg()
    assert agg._last_glassnode_call is None
    asyncio.run(agg._rate_limit_glassnode())
    assert agg._last_glassnode_call is not None
    assert isinstance(agg._glassnode_rate_lock, asyncio.Lock)


# ---------------------------------------------------------------------------
# INT-020 / INT-021 / INT-022: providers
# ---------------------------------------------------------------------------


def test_int020_okx_positioning_ratio_is_not_reported_as_taker_flow() -> None:
    from src.intelligence.providers.okx_provider import OKXIntelligenceProvider

    prov = object.__new__(OKXIntelligenceProvider)
    prov._perp_symbol = "BTC/USDT:USDT"
    prov._get_cache = lambda key: None
    prov._set_cache = MagicMock()
    with pytest.raises(RuntimeError):
        asyncio.run(prov._fetch_whale_taker_ratio())
    prov._set_cache.assert_not_called()  # no fabricated neutral cached


def test_int020_coinglass_does_not_populate_whale_ratio() -> None:
    from src.intelligence.onchain import coinglass_provider

    assert "_ls_ratio(ls_data)" not in inspect.getsource(coinglass_provider.CoinglassProvider)


@pytest.mark.parametrize(
    ("module", "cls"),
    [
        ("binance_provider", "BinanceIntelligenceProvider"),
        ("okx_provider", "OKXIntelligenceProvider"),
        ("bybit_provider", "BybitIntelligenceProvider"),
    ],
)
def test_int021_singleton_refuses_a_different_symbol(monkeypatch, module, cls) -> None:
    import importlib

    mod = importlib.import_module(f"src.intelligence.providers.{module}")
    factory = next(
        getattr(mod, n) for n in dir(mod) if n.startswith("get_") and n.endswith("_provider")
    )

    class Dummy:
        def __init__(self, symbol, perp_symbol):
            pass

    monkeypatch.setattr(mod, "_provider", None)
    monkeypatch.setattr(mod, cls, Dummy)
    first = factory(symbol="BTC/USDT", perp_symbol="BTC/USDT:USDT")
    assert factory(symbol="BTC/USDT", perp_symbol="BTC/USDT:USDT") is first
    with pytest.raises(ValueError):
        factory(symbol="ETH/USDT", perp_symbol="ETH/USDT:USDT")


def test_int022_cache_hits_do_not_grow_zscore_history() -> None:
    from src.intelligence.providers.coingecko_provider import CoinGeckoIntelligenceProvider

    prov = CoinGeckoIntelligenceProvider(cache_ttl_s=900)
    prov._fetch_global = AsyncMock(
        return_value={"market_cap_percentage": {"btc": 50.0}, "total_market_cap": {"usd": 1e12}}
    )
    for _ in range(6):
        asyncio.run(prov.fetch_metrics())
    assert len(prov._btc_dom_history) == 1


def test_int022_arkham_zscore_is_bounded_without_dispersion() -> None:
    from src.intelligence.onchain.arkham_provider import _zscore

    assert _zscore(5.0, [5.0, 5.0, 5.0]) == 0.0
    assert abs(_zscore(1e9, [1.0, 2.0, 3.0])) <= 3.0


# ---------------------------------------------------------------------------
# INT-023: horizon head-of-line blocking
# ---------------------------------------------------------------------------


def test_int023_rejected_rows_leave_the_head_of_the_queue(tmp_path: Path) -> None:
    from src.models.horizon_learning import HorizonLearningStore

    store = HorizonLearningStore(tmp_path / "state")
    root = tmp_path / "models"
    mlp = [{"id": 0, "seconds": 10, "models": ["mlp"]}]
    for event_id, ts, close in (("e1", 100, 100), ("e2", 110, 101)):
        store.observe_event(
            event_id=event_id,
            symbol="BTC/USDT",
            event_ts=ts,
            close=close,
            features={"price": close},
            horizons=mlp,
            model_root=root,
            defer_training=True,
        )
    cnn = [{"id": 0, "seconds": 10, "models": ["cnn"]}]
    first = store.train_pending(symbol="BTC/USDT", horizons=cnn, model_root=root)
    assert first["rejected"] == 1
    second = store.train_pending(symbol="BTC/USDT", horizons=cnn, model_root=root)
    assert second["attempted"] == 0  # not re-selected
