"""Regression tests for the Phase 6 data/intelligence Low findings.

Decides:
  - REG-1430 -- low-severity data and intelligence defects (DAT-021/022/023, INT-027/030/035/036)
"""

from __future__ import annotations

import asyncio
import math
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.data.clock import ClockError
from src.data.quality_gate import OHLCV_REALTIME_BUDGET, DataQualityGate
from src.eventbus import EventBus
from src.eventbus.bus import TOPICS
from src.intelligence.probabilistic_adapter import ProbabilisticMetricsAdapter
from src.intelligence.providers.bybit_provider import BybitIntelligenceProvider
from src.intelligence.providers.okx_provider import OKXIntelligenceProvider
from src.intelligence.risk_quantification import RiskQuantifier


def test_bus_total_dropped_keeps_detached_subscriber_drops() -> None:
    """DAT-023: a starved subscriber's drops survive its detach in total_dropped."""
    bus = EventBus()
    topic = sorted(TOPICS)[0]
    sub = bus.subscribe([topic])
    for i in range(sub.maxlen + 5):
        bus.publish(topic, {"i": i})
    before = bus.total_dropped
    assert before == 5
    sub.close()
    assert bus.subscriber_count == 0
    assert bus.total_dropped == before
    sub.close()
    assert bus.total_dropped == before


def test_quality_gate_naive_now_raises_clock_error() -> None:
    """DAT-022: a naive ``now`` is refused with ClockError, not a bare TypeError."""
    gate = DataQualityGate()
    ts = pd.Series(pd.to_datetime([datetime.now(UTC)], utc=True))
    with pytest.raises(ClockError):
        gate._check_staleness(ts, OHLCV_REALTIME_BUDGET, datetime(2026, 1, 1))


def test_storage_ddl_defaults_to_synchronous_full() -> None:
    """DAT-021: durability must not depend on whether a bulk write ran earlier."""
    src = Path("src/data/storage.py").read_text()
    assert "PRAGMA synchronous=FULL;" in src
    assert "PRAGMA synchronous=NORMAL;" not in src


@pytest.mark.parametrize("cls", [OKXIntelligenceProvider, BybitIntelligenceProvider])
def test_single_funding_rate_is_reported_in_percent(cls) -> None:
    """INT-027: the <2-rates branch must scale to percent like the normal path."""

    class _Perp:
        async def fetch_funding_rate_history(self, *_a, **_kw):
            return [{"fundingRate": 0.0001}]

    prov = cls.__new__(cls)
    prov._perp = _Perp()
    prov._perp_symbol = "BTC/USDT:USDT"
    prov._cache_ttl = 300
    out = asyncio.run(prov._fetch_funding_data())
    assert out["rate_pct"] == pytest.approx(0.01)


def test_adapter_fails_open_on_nan_inputs() -> None:
    """INT-030: NaN metrics must yield None (gate fails open), never a NaN score."""
    adapter = ProbabilisticMetricsAdapter()
    res = adapter.process(
        {
            "exchange_stress_score": 0.3,
            "exchange_reserve_ratio": float("nan"),
            "whale_buy_sell_ratio": float("nan"),
        }
    )
    assert res.exchange_stress_score is None
    assert res.whale_buy_sell_ratio is None


@pytest.mark.parametrize("bad", [[], [0.01, float("nan"), -0.02]])
def test_value_at_risk_rejects_empty_or_nan_returns(bad) -> None:
    """INT-036: empty or NaN returns raise rather than propagate NaN into CVaR caps."""
    with pytest.raises(ValueError):
        RiskQuantifier().value_at_risk(np.array(bad), method="historical")
    assert math.isfinite(
        RiskQuantifier().value_at_risk(np.linspace(-0.05, 0.05, 200))["var"]
    )


# ---------------------------------------------------------------------------
# Second batch: DAT-020/022/025, INT-028/029/032/036
# ---------------------------------------------------------------------------


def test_feeds_publish_ohlcv_carries_published_ts_and_consumer_requires_enter() -> None:
    """DAT-020: published_ts survives a bar's own ts; iterating an unstarted consumer raises."""
    from src.data.feeds import RedpandaConsumer, RedpandaFeeds

    sent: list[dict] = []

    class _Producer:
        async def send_and_wait(self, _topic, payload):
            sent.append(payload)

    feeds = RedpandaFeeds()
    feeds._producer = _Producer()
    asyncio.run(feeds.publish_ohlcv("BTC/USDT", "1h", {"ts": 123, "close": 1.0}))
    assert sent[0]["ts"] == 123
    assert sent[0]["published_ts"] > 123

    async def _iterate() -> None:
        async for _ in RedpandaConsumer("crypto.ecc"):
            break

    with pytest.raises(RuntimeError):
        asyncio.run(_iterate())


def test_quality_gate_rejects_datetime_index_and_scales_extreme_return() -> None:
    """DAT-022: a DatetimeIndex is refused; 4h budgets tolerate larger moves than 15m."""
    from src.data.quality_gate import FreshnessBudget

    bars = pd.DataFrame(
        {"open": [1.0], "high": [1.0], "low": [1.0], "close": [1.0], "volume": [1.0]},
        index=pd.to_datetime([datetime.now(UTC)]),
    )
    res = DataQualityGate().check_bars(bars)
    assert not res.passed
    assert "index_not_integer_ms" in res.reason
    assert FreshnessBudget.for_timeframe(900).max_abs_return == pytest.approx(0.15)
    assert FreshnessBudget.for_timeframe(14400).max_abs_return == pytest.approx(0.30)


def test_registry_node_selector_and_missing_vocabulary_key(tmp_path: Path) -> None:
    """DAT-025: a renamed ::test is refused; a missing vocabulary key is a RegistryError."""
    import json
    from types import SimpleNamespace

    from src.quality.registry import PROJECT_ROOT, RegistryError, _check_node_selector, load_registry

    f = tmp_path / "test_x.py"
    f.write_text("def test_real():\n    pass\n")
    _check_node_selector("REG-1", SimpleNamespace(path="test_x.py", node="test_real"), tmp_path)
    with pytest.raises(RegistryError):
        _check_node_selector("REG-1", SimpleNamespace(path="test_x.py", node="test_gone"), tmp_path)

    raw = json.loads((PROJECT_ROOT / "config/quality_registry.json").read_text())
    del raw["kind_definitions"]
    broken = tmp_path / "reg.json"
    broken.write_text(json.dumps(raw))
    with pytest.raises(RegistryError):
        load_registry(broken, root=PROJECT_ROOT)


def test_cryptoquant_reserve_ratio_needs_live_price_and_limiters_burst() -> None:
    """INT-028/029: no hardcoded price; rate limiters hold a per-minute burst."""
    from src.intelligence.onchain.base import RateLimiter
    from src.intelligence.onchain.coinglass_provider import CoinglassProvider
    from src.intelligence.onchain.cryptoquant_provider import CryptoQuantProvider, _reserve_ratio

    assert _reserve_ratio({"result": {"data": [{"reserve_usd": 1e9}]}}) is None
    ratio = _reserve_ratio({"result": {"data": [{"reserve_usd": 21e9, "price": 100.0}]}})
    assert ratio == pytest.approx(21e9 / (21_000_000 * 100.0))
    for cls in (CryptoQuantProvider, CoinglassProvider):
        assert cls._RATE_WINDOW_S == 60.0
        assert cls._RATE >= 10.0
        assert RateLimiter(cls._RATE, cls._RATE_WINDOW_S)._tokens >= 10.0


def test_models_patchtst_short_input_and_chomp_zero() -> None:
    """INT-032: PatchTST accepts T < seq_len; _Chomp1d(0) is the identity."""
    torch = pytest.importorskip("torch")
    from src.models.patchtst import PatchTSTHead
    from src.models.tcn import _Chomp1d

    x = torch.ones(2, 3, 5)
    assert _Chomp1d(0)(x).shape == x.shape
    head = PatchTSTHead(n_channels=5, seq_len=64, n_layers=1).eval()
    assert head(torch.randn(2, 5, 32)).shape == (2, 128)


def test_probability_helper_guards() -> None:
    """INT-036: brier range check, 0.0 prior honoured, unknown regime falls back."""
    from src.intelligence.calibration import brier_score
    from src.intelligence.probabilistic import BayesianWhaleActivityModel

    with pytest.raises(ValueError):
        brier_score([1.5], [1.0])
    model = BayesianWhaleActivityModel()
    zero = model.estimate_true_ratio(1.0, 10, prior_mean=0.0)
    default = model.estimate_true_ratio(1.0, 10)
    assert zero.point_estimate != default.point_estimate
    assert model.estimate_market_impact(1.0, "sideways")["causal_effect"] == pytest.approx(-0.012)
