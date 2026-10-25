"""Regression tests for phase-6 Low findings (MTH-003/007/008/021/023, STR-17)."""

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
    expected = 1 if out.predicted_price > spot * 1.002 else (-1 if out.predicted_price < spot * 0.998 else 0)
    assert out.direction == expected
    out0 = asyncio.run(
        E04Fourier().run("BTC/USDT", {"ohlcv": df, "spot": spot, "block_height": 0})
    )
    outx = asyncio.run(E04Fourier().run("ETH/USDT", {"ohlcv": df, "spot": spot}))
    assert out0.predicted_price == pytest.approx(outx.predicted_price)
