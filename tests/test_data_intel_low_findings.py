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
