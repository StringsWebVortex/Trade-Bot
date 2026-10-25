"""Regression tests for the Phase 5 math/strategy audit findings.

MTH-002/004/005/012/014 and STR-07..STR-16. Each test fails on the code as it
stood before the fix.

Decides:
  - REG-1360 — HNP key recovery is correct for a non-zero leaked nonce prefix
  - REG-1361 — ECDSA scanner does not report a re-seen transaction as nonce reuse
  - REG-1362 — Cluster flow score is flagged unavailable when no flow data exists
  - REG-1363 — UTXO age falls back to confirmations and excludes unknown ages
  - REG-1364 — Tornado detection handles HexBytes input and matches withdrawals by pool
  - REG-1365 — Engine backtest annualises per sample, scores at horizon, applies documented gate
  - REG-1366 — E-09 retrain uses the inference feature set and a held-out gate before saving
  - REG-1367 — E-14 abstains without history and is neutral on a degenerate window
  - REG-1368 — Engine rolling state is keyed by symbol
  - REG-1369 — Consensus dispersion excludes abstentions and the breaker holds real spot
  - REG-1370 — E-07 PCA direction follows the recent PC1 score with a fixed sign
  - REG-1371 — Capital allocator does not mix warm-up shares with raw scores
  - REG-1372 — Slippage calibration ADV is a daily volume
  - REG-1373 — Entropy harness does not report an identical win-rate metric
  - REG-1374 — Strategy selector exposes no dead funding-carry parameter
"""

from __future__ import annotations

import inspect
import random
from datetime import UTC, datetime
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from src.engines.schema import EngineOutput


def _ohlcv(n: int = 200, seed: int = 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    closes = np.cumprod(1 + rng.normal(0.0002, 0.01, n)) * 50_000.0
    return pd.DataFrame(
        {
            "timestamp_utc": pd.date_range("2025-01-01", periods=n, freq="h", tz="UTC"),
            "open": closes * 0.999,
            "high": closes * 1.004,
            "low": closes * 0.996,
            "close": closes,
            "volume": rng.uniform(1000, 5000, n),
        }
    )


def _out(engine_id: str, price: float, conf: float, **meta: object) -> EngineOutput:
    return EngineOutput(
        engine_id=engine_id,
        symbol="BTC/USDT",
        timestamp_utc=datetime.now(UTC),
        predicted_price=price,
        confidence=conf,
        direction=0,
        horizon_hours=4,
        metadata=dict(meta),
    )


# ---- MTH-014 ---------------------------------------------------------------


def test_hnp_recovers_the_key_with_a_non_zero_leaked_prefix() -> None:
    from src.mathcore.lattice.hnp import Signature, recover_private_key

    order, modulus = 1_000_003, 2_000_003
    bits = order.bit_length()
    for seed in range(3):
        rng = random.Random(seed)
        key = rng.randrange(1, order)
        sigs = []
        for _ in range(5):
            z = rng.randrange(order)
            prefix = 0x0A5
            k = (prefix << 8) + rng.randrange(1, 256)
            r = pow(5, k, modulus) % order or 1
            s = (pow(k, -1, order) * (z + r * key)) % order
            sigs.append(Signature(r, s, z, known_high_bits=bits - 8, known_value=prefix << 8))
        assert recover_private_key(sigs, order, bits) == key


# ---- MTH-002 ---------------------------------------------------------------


def test_rescanning_the_same_transaction_is_not_nonce_reuse(monkeypatch) -> None:
    from src.ecc import ecdsa_scan

    sig = (12345, 678, b"\x02" + b"\x11" * 32, "tx-a")
    monkeypatch.setattr(ecdsa_scan, "extract_ecdsa_signatures", lambda _raw: [sig])
    scanner = ecdsa_scan.ECDSAScanner()
    assert scanner.scan_transaction("00") == []
    assert scanner.scan_transaction("00") == []  # re-broadcast / overlapping feed
    other = (12345, 999, b"\x02" + b"\x11" * 32, "tx-b")
    monkeypatch.setattr(ecdsa_scan, "extract_ecdsa_signatures", lambda _raw: [other])
    assert len(scanner.scan_transaction("00")) == 1  # genuine reuse across txids


# ---- MTH-004 ---------------------------------------------------------------


def test_cluster_flow_is_flagged_unavailable_without_flow_data() -> None:
    from src.ecc.secp256k1_cluster import AddressClusterer, ClusterInfo, ClusteringResult

    whale = ClusterInfo(cluster_id=0, total_btc=1e9, addresses=["a"])
    assert AddressClusterer.has_flow_data([whale]) is False
    whale.inflow_btc = 5.0
    assert AddressClusterer.has_flow_data([whale]) is True
    assert ClusteringResult(0.0, 0, 0.0).flow_available is False


# ---- MTH-005 ---------------------------------------------------------------


def test_utxo_age_uses_confirmations_and_excludes_unknown_age() -> None:
    from src.ecc.utxo_curve import compute_hodler_index

    old = {"value_btc": 10.0, "confirmations": 144 * 365 * 5}
    assert compute_hodler_index([old]).hodler_index > 0.5
    undated = {"value_btc": 1000.0}
    assert compute_hodler_index([old, undated]).hodler_index > 0.9
    assert compute_hodler_index([undated]).mean_age_days == 0.0


# ---- MTH-012 ---------------------------------------------------------------


def test_tornado_detection_accepts_bytes_input_and_matches_by_pool() -> None:
    from src.ecc.zksnark_detect import (
        _TORNADO_CONTRACTS,
        _is_tornado_deposit,
        _is_tornado_withdrawal,
        trace_spend_cluster,
    )

    pool = sorted(_TORNADO_CONTRACTS)[0]
    deposit = {
        "to": pool,
        "input": bytes.fromhex("b214faa5" + "00" * 4),
        "value": 10**18,
        "hash": "0xd",
    }
    withdrawal = {
        "to": pool,
        "input": bytes.fromhex("21a0adb5" + "00" * 4),
        "value": 0,
        "hash": "0xw",
    }
    assert _is_tornado_deposit(deposit)
    assert _is_tornado_withdrawal(withdrawal)
    assert trace_spend_cluster(deposit, [withdrawal]) == [withdrawal]


# ---- STR-07 ----------------------------------------------------------------


def test_signal_sharpe_annualises_by_sample_frequency() -> None:
    from src.tuning.engine_backtest import signal_sharpe

    rets = np.array([0.01, -0.004, 0.006, 0.002, -0.001])
    assert signal_sharpe(rets, 8760.0 / 30) == pytest.approx(signal_sharpe(rets) / np.sqrt(30))


@pytest.mark.asyncio
async def test_backtest_scores_at_the_declared_horizon_and_applies_the_sharpe_gate() -> None:
    from src.tuning.engine_backtest import EngineWalkForwardBacktest

    n = 212  # exactly one walk-forward window: start == 181
    close = np.full(n, 100.0)
    close[181] = 99.0  # next bar is down ...
    close[184:] = 110.0  # ... but the 4h horizon is up
    df = pd.DataFrame(
        {
            "timestamp_utc": pd.date_range("2025-01-01", periods=n, freq="h", tz="UTC"),
            "open": close,
            "high": close,
            "low": close,
            "close": close,
            "volume": np.ones(n),
        }
    )

    async def engine(_symbol: str, _data: dict) -> SimpleNamespace:
        return SimpleNamespace(direction=1, predicted_price=110.0, horizon_hours=4)

    result = await EngineWalkForwardBacktest("E-99", engine).run(df)
    assert result.directional_accuracy == 1.0
    # One window gives Sharpe 0: below the documented > 1.0 threshold.
    assert result.passes_gate is False


# ---- STR-08 ----------------------------------------------------------------


def test_e09_features_match_what_training_can_build() -> None:
    from src.engines import e09_ml_meta

    assert [f"E-{i:02d}" for i in range(1, 9)] == e09_ml_meta._FEATURE_ENGINE_IDS


def test_e09_oos_accuracy_needs_two_classes_and_scores_a_held_out_tail() -> None:
    from src.tuning.engine_backtest import _e09_oos_accuracy

    X = np.arange(40, dtype=np.float32).reshape(-1, 1)
    assert _e09_oos_accuracy(X, np.ones(40, dtype=np.int32)) is None
    y = (np.arange(40) % 2).astype(np.int32)
    X2 = y.astype(np.float32).reshape(-1, 1)  # perfectly predictive feature
    assert _e09_oos_accuracy(X2, y) == 1.0


# ---- STR-09 / STR-10 (E-14) --------------------------------------------------


def test_contrarian_signal_is_neutral_for_a_degenerate_window() -> None:
    from src.engines.e14_sentiment import contrarian_signal

    assert contrarian_signal(0.5, 0.5, 0.5) == 0.0


@pytest.mark.asyncio
async def test_e14_abstains_until_history_exists_and_keeps_it_per_symbol() -> None:
    from src.engines.e14_sentiment import E14Sentiment

    e = E14Sentiment()
    sentiment = {"fg_score": 40.0, "vader_compound": 0.0}
    first = await e.run("BTC/USDT", {"spot": 50_000.0, "sentiment": sentiment})
    assert first.confidence == 0.0 and first.direction == 0
    for fg in (30.0, 50.0, 60.0, 45.0):
        await e.run("BTC/USDT", {"spot": 50_000.0, "sentiment": {"fg_score": fg}})
    other = await e.run("ETH/USDT", {"spot": 3_000.0, "sentiment": sentiment})
    assert other.confidence == 0.0 and other.direction == 0  # not BTC's history


@pytest.mark.asyncio
async def test_e13_contagion_baseline_is_per_symbol() -> None:
    from src.engines.e13_contagion import E13Contagion

    rng = np.random.default_rng(5)
    macro = {
        "spx_ret": 0.004,
        "dxy_ret": -0.002,
        "spx_series": rng.normal(0, 0.01, 200).tolist(),
        "dxy_series": rng.normal(0, 0.005, 200).tolist(),
    }
    e = E13Contagion()
    btc = _ohlcv(seed=1)
    eth = _ohlcv(seed=2)
    await e.run("BTC/USDT", {"ohlcv": btc, "spot": 1.0, "macro": macro})
    out = await e.run("ETH/USDT", {"ohlcv": eth, "spot": 1.0, "macro": macro})
    assert out.metadata["contagion_score"] == 0.0  # no ETH baseline yet


@pytest.mark.asyncio
async def test_e08_wasserstein_history_is_per_symbol() -> None:
    from src.engines.e08_topology import E08Topology

    df = _ohlcv()
    e = E08Topology()
    e._compute_tda = lambda embedding: (0.1, 0.1)  # type: ignore[method-assign]
    for _ in range(12):
        await e.run("BTC/USDT", {"ohlcv": df, "spot": 1.0})
    e._compute_tda = lambda embedding: (99.0, 0.1)  # type: ignore[method-assign]
    out = await e.run("ETH/USDT", {"ohlcv": df, "spot": 1.0})
    assert out.metadata["regime_break"] is False


# ---- STR-11 ----------------------------------------------------------------


def test_abstentions_do_not_dilute_agreement_or_hide_outliers() -> None:
    from src.engines.consensus import ConsensusLayer

    outputs = [
        _out("E-01", 100.0, 0.8),
        _out("E-02", 100.0, 0.8),
        _out("E-03", 150.0, 0.0),  # abstention carrying a stale price
    ]
    result = ConsensusLayer().compute(outputs, "Trending")
    assert result.agreement_score == pytest.approx(1.0)
    assert result.outlier_ids == []


def test_circuit_breaker_holds_the_real_spot() -> None:
    from src.engines.consensus import ConsensusLayer

    outputs = [_out("E-01", 50_500.0, 0.8), _out("E-16", 50_000.0, 0.9, manipulation_flag=True)]
    result = ConsensusLayer().compute(outputs, "Trending", spot=48_000.0)
    assert result.circuit_breaker_triggered is True
    assert result.consensus_price == 48_000.0


# ---- STR-12 ----------------------------------------------------------------


@pytest.mark.parametrize("tail", [0.05, -0.05])
def test_pca_direction_follows_the_recent_pc1_score(tail: float) -> None:
    from src.engines.e07_linear_algebra import E07LinearAlgebra

    rng = np.random.default_rng(3)
    factor = rng.normal(0, 0.01, 100)
    factor[-5:] = tail

    def frame(loading: float) -> pd.DataFrame:
        r = factor * loading + rng.normal(0, 1e-4, 100)
        return pd.DataFrame({"close": 100.0 * np.cumprod(1 + r)})

    direction = E07LinearAlgebra._pca_signal(frame(1.0), {"ETH": frame(1.2)})
    assert direction == (1 if tail > 0 else -1)


# ---- STR-13 ----------------------------------------------------------------


class _Strat:
    def __init__(self, strategy_id: str) -> None:
        self.strategy_id = strategy_id

    def generate_signal(self, bar: object) -> object:
        return None

    def required_capital_fraction(self) -> float:
        return 1.0


def test_warm_up_share_is_not_mixed_with_raw_scores() -> None:
    from src.diagnostics.attribution import AttributedFill, get_attribution_tracker
    from src.strategies.capital_allocator import (
        _MIN_TRADES_FOR_SHARPE,
        performance_weighted_allocate,
    )

    tracker = get_attribution_tracker()
    tracker.reset()
    try:
        for i in range(_MIN_TRADES_FOR_SHARPE + 5):
            pnl = 10.0 if i % 2 else 2.0
            tracker.record(
                AttributedFill(strategy_id="mature", pnl_usd=pnl, entry_ts=i, exit_ts=i + 1)
            )
        result = performance_weighted_allocate(
            (_Strat("mature"), _Strat("fresh")), {"mature", "fresh"}, metric="sharpe"
        )
    finally:
        tracker.reset()
    # The warm-up strategy keeps its equal share; the mature one gets the rest.
    assert result.fractions["fresh"] == pytest.approx(0.5)
    assert result.fractions["mature"] == pytest.approx(0.5)


# ---- STR-14 ----------------------------------------------------------------


def test_bars_per_day_scales_slippage_adv_to_daily_volume() -> None:
    from src.tuning.scheduler import bars_per_day

    assert bars_per_day("15m") == 96.0
    assert bars_per_day("4h") == 6.0
    assert bars_per_day("1d") == 1.0
    with pytest.raises(ValueError):
        bars_per_day("bogus")


# ---- STR-15 ----------------------------------------------------------------


def test_entropy_harness_does_not_report_a_dead_win_rate() -> None:
    from src.tuning.backtest_harness import TradeSample, run_entropy_threshold_backtest

    samples = [
        TradeSample(raw_return=0.01 * (1 if i % 3 else -1), entropy=0.1 * (i % 9))
        for i in range(120)
    ]
    names = {c.metric_name for c in run_entropy_threshold_backtest(samples, 0.5, 0.5, 0.4, 0.6)}
    assert "win_rate" not in names


# ---- STR-16 ----------------------------------------------------------------


def test_selector_has_no_dead_funding_carry_parameter() -> None:
    from src.strategies import regime_strategy_selector as sel

    assert "allow_funding_carry" not in inspect.signature(sel.select_strategy).parameters
    assert not hasattr(sel, "STRATEGY_FUNDING_CARRY")
