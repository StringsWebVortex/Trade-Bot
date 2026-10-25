"""Regression tests for phase-6 Low findings (MTH-003/007/008/021/023, STR-17).

Decides:
  - REG-1460 — Dead ECDSA r-registry prune helper removed
  - REG-1461 — Failed model artifact log returns no run id
  - REG-1462 — DVC git tag name is validated
  - REG-1463 — Negative DH public values rejected
  - REG-1464 — Non-finite Mosca inputs rejected
  - REG-1465 — Fourier engine detrends and derives direction after adjustments
  - REG-1466 — Pohlig-Hellman trial division is bounded
  - REG-1467 — Committee size uses a closed form
  - REG-1468 — Birthday minimum draws is exact for huge spaces
  - REG-1469 — Constants module does not mutate the global decimal context
  - REG-1470 — GBM Monte Carlo default RNG is seeded
  - REG-1471 — Filters reject invalid direction values
"""

from __future__ import annotations

import asyncio

import numpy as np
import pandas as pd
import pytest

from src.ecc.ecdsa_scan import ECDSAScanner
from src.engines.e04_fourier import E04Fourier
from src.mathcore.numbertheory.safe_primes import is_valid_public_value
from src.mathcore.quantum.shor import QuantumAssessmentError, migration_verdict
from src.upgrade.registry import ModelRegistry


def test_mth003_dead_prune_helper_removed() -> None:
    assert not hasattr(ECDSAScanner, "clear_old_entries")


class _FailingPytorch:
    def log_model(self, *_a: object, **_k: object) -> None:
        raise RuntimeError("artifact store down")


class _Run:
    class info:  # noqa: N801
        run_id = "run-1"

    def __enter__(self) -> _Run:
        return self

    def __exit__(self, *_a: object) -> None:
        return None


class _FakeMlflow:
    pytorch = _FailingPytorch()

    def start_run(self, **_k: object) -> _Run:
        return _Run()

    def log_params(self, *_a: object) -> None: ...
    def log_metrics(self, *_a: object) -> None: ...


def test_mth007_failed_artifact_log_returns_none() -> None:
    reg = object.__new__(ModelRegistry)
    reg._mlflow = _FakeMlflow()
    reg._experiment_id = "1"
    assert reg.log_model(object(), "m", 0, {"x": 1.0}) is None


@pytest.mark.parametrize("name", ["--force", "-a", "bad name", "x;rm", ""])
def test_mth008_tag_name_validated(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    import subprocess

    calls: list[object] = []
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: calls.append(a))
    reg = object.__new__(ModelRegistry)
    assert reg.tag_dvc(name) is False
    assert calls == []


def test_mth021_negative_public_value_rejected() -> None:
    assert is_valid_public_value(-4, 23) is False


def test_mth023_non_finite_years_rejected() -> None:
    with pytest.raises(QuantumAssessmentError):
        migration_verdict(
            "RSA-2048",
            confidentiality_years=float("nan"),
            migration_years=1.0,
            years_until_capable_machine=5.0,
        )


def test_str17_direction_agrees_with_final_price_and_no_overlay_without_height() -> None:
    n = 400
    close = 100 * np.exp(np.cumsum(np.full(n, 0.0005)) + 0.01 * np.sin(np.arange(n) / 5))
    df = pd.DataFrame({"close": close})
    out = asyncio.run(E04Fourier().run("BTC/USDT", {"ohlcv": df, "spot": float(close[-1])}))
    spot = float(close[-1])
    expected = (
        1
        if out.predicted_price > spot * 1.002
        else (-1 if out.predicted_price < spot * 0.998 else 0)
    )
    assert out.direction == expected
    out0 = asyncio.run(E04Fourier().run("BTC/USDT", {"ohlcv": df, "spot": spot, "block_height": 0}))
    outx = asyncio.run(E04Fourier().run("ETH/USDT", {"ohlcv": df, "spot": spot}))
    assert out0.predicted_price == pytest.approx(outx.predicted_price)


def test_mth015_trial_division_is_bounded() -> None:
    from src.mathcore.numbertheory.dlp_bounds import pohlig_hellman_security_bits

    big_prime = (1 << 255) - 19
    with pytest.raises(ValueError):
        pohlig_hellman_security_bits(big_prime)


def test_mth016_min_committee_size_fast_and_exact() -> None:
    from src.mathcore.probability.committee import chernoff_committee_bound, min_committee_size

    n = min_committee_size(0.25, 0.5, 1e-9)
    assert chernoff_committee_bound(0.25, n, 0.5) <= 1e-9
    assert chernoff_committee_bound(0.25, n - 1, 0.5) > 1e-9


def test_mth017_birthday_exact_for_huge_space() -> None:
    import inspect

    from src.mathcore.probability import birthday

    fn = next(
        f
        for _, f in inspect.getmembers(birthday, inspect.isfunction)
        if "threshold" in inspect.signature(f).parameters
    )
    k = fn(1 << 80, 0.5)
    p = birthday.birthday_collision_probability
    assert p(k, 1 << 80) >= 0.5 > p(k - 1, 1 << 80)


def test_mth018_import_does_not_mutate_global_decimal_context() -> None:
    import decimal

    from src.mathcore.constants import nutms

    assert decimal.getcontext().prec == 28
    assert nutms.tea_delta() == 0x9E3779B9
    assert decimal.getcontext().prec == 28


def test_str18_gbm_default_is_deterministic() -> None:
    from src.engines.e11_stochastic import gbm_mc

    assert np.array_equal(gbm_mc(100.0, 0.1, 0.5, 24.0), gbm_mc(100.0, 0.1, 0.5, 24.0))


def test_str19_invalid_direction_rejected() -> None:
    from src.strategies.filters import trend_filter_passes

    with pytest.raises(ValueError):
        trend_filter_passes(pd.Series(np.arange(1.0, 200.0)), 5)
