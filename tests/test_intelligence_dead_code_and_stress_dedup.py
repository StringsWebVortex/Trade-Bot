"""REG-1713: no wrong ruin estimate, no orphan causal module, one stress formula.

RiskQuantifier.estimate_probability_of_ruin counted every day below the 90th
percentile as a tail excess, so it reported roughly 90% of days as ruin, and it
never measured a drawdown. Nothing called it. src/intelligence/causal_inference.py
had no importer. Both were removed rather than kept as callable traps.

The Binance, OKX and Bybit providers each carried a copy of the exchange stress
formula; they now share base.exchange_stress_score, so the venues cannot drift.
"""

from __future__ import annotations

import importlib.util

import pytest

from src.intelligence.providers import base
from src.intelligence.providers.binance_provider import BinanceIntelligenceProvider
from src.intelligence.providers.bybit_provider import BybitIntelligenceProvider
from src.intelligence.providers.okx_provider import OKXIntelligenceProvider
from src.intelligence.risk_quantification import RiskQuantifier


def test_the_wrong_probability_of_ruin_estimate_is_gone():
    assert not hasattr(RiskQuantifier, "estimate_probability_of_ruin")


def test_the_unimported_causal_inference_module_is_gone():
    assert importlib.util.find_spec("src.intelligence.causal_inference") is None


@pytest.mark.parametrize(
    "provider",
    [BinanceIntelligenceProvider, OKXIntelligenceProvider, BybitIntelligenceProvider],
)
def test_every_venue_uses_the_shared_stress_formula(provider):
    assert provider._compute_stress_score is base.exchange_stress_score


def test_stress_weights_sum_to_one():
    total = base.STRESS_WEIGHT_BASIS + base.STRESS_WEIGHT_FUNDING_Z + base.STRESS_WEIGHT_OI
    assert total == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("basis_bps", "funding_zscore", "oi_change_pct", "expected"),
    [
        (0.0, 0.0, 0.0, 0.0),
        (100.0, 0.0, 0.0, 0.35),
        (-100.0, 0.0, 0.0, 0.35),
        (0.0, -3.0, 0.0, 0.4),
        (0.0, 0.0, -5.0, 0.25),
        (0.0, 0.0, 10.0, 0.0),
        (1000.0, 100.0, -100.0, 1.0),
        (50.0, 1.5, -2.5, 0.5),
    ],
)
def test_stress_score_components_saturate_and_weight(
    basis_bps, funding_zscore, oi_change_pct, expected
):
    score = base.exchange_stress_score(basis_bps, funding_zscore, oi_change_pct)
    assert score == pytest.approx(expected)
