"""Regression tests for Low-severity audit findings (phase 6).

Each test fails on the pre-fix behaviour it names.
"""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(rel: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# DOC-016: re-ingesting a source replaces its chunks instead of duplicating them.
def test_reingest_deletes_prior_chunks_before_insert():
    from rag_mongo import ingest

    col = MagicMock()
    with (
        patch("rag_mongo.ingest.get_collection", return_value=col),
        patch("rag_mongo.ingest.embed_batch", return_value=[[0.1]]),
        patch("rag_mongo.ingest.chunk_text", return_value=["c"]),
    ):
        ingest.ingest_text("text", source="a.txt")
    col.delete_many.assert_called_once_with({"source": "a.txt"})
    names = [c[0] for c in col.method_calls]
    assert names.index("delete_many") < names.index("insert_many")


def test_failed_embed_keeps_previous_chunks():
    from rag_mongo import ingest

    col = MagicMock()
    with (
        patch("rag_mongo.ingest.get_collection", return_value=col),
        patch("rag_mongo.ingest.embed_batch", side_effect=RuntimeError("down")),
        patch("rag_mongo.ingest.chunk_text", return_value=["c"]),
        pytest.raises(RuntimeError),
    ):
        ingest.ingest_text("text", source="a.txt")
    col.delete_many.assert_not_called()


# DOC-017: a question with no matching entity grounds on nothing, not arbitrary edges.
def test_kg_candidate_names_ignore_stopwords():
    from kg import query

    nodes_col = MagicMock()
    nodes_col.find.return_value.limit.return_value = []
    with patch("kg.query.get_nodes_collection", return_value=nodes_col):
        query._candidate_names("what is the Alice")
    in_list = nodes_col.find.call_args_list[0][0][0]["name"]["$in"]
    assert "the" not in in_list and "what" not in in_list and "Alice" in in_list


# SCR-009 / DOC-030: no inf reaches the feature matrix; RSI is 100 on a no-loss window.
def _indicators():
    return _load("crypto-predictor/indicators.py", "crypto_predictor_indicators")


def test_feature_matrix_has_no_infinite_values_when_obv_crosses_zero():
    ind = _indicators()
    close = np.array([100.0, 99.0, 100.0] + list(101.0 + np.arange(37)))
    df = pd.DataFrame(
        {
            "open": close,
            "high": close + 1,
            "low": close - 1,
            "close": close,
            "volume": np.full(len(close), 10.0),
        }
    )
    feats = ind.build_feature_matrix(df)
    values = feats.to_numpy(dtype=float)
    assert not np.isinf(values).any()


def test_rsi_is_100_when_window_has_no_losses():
    ind = _indicators()
    rsi = ind.rsi(pd.Series(np.arange(1.0, 40.0)), 14)
    assert rsi.iloc[-1] == pytest.approx(100.0)


def test_rsi_is_neutral_on_a_flat_window():
    ind = _indicators()
    rsi = ind.rsi(pd.Series(np.full(40, 5.0)), 14)
    assert rsi.iloc[-1] == pytest.approx(50.0)


# SCR-010: coverage floor refuses an empty report.
def test_coverage_floor_fails_on_zero_measured_files(monkeypatch, capsys):
    mod = _load("scripts/check_coverage_floors.py", "check_coverage_floors_t")
    monkeypatch.setattr(mod, "_coverage_json", lambda: {"files": {}})
    assert mod.main() == 1
    assert "no measured files" in capsys.readouterr().out


# OPS-021: the 5m preflight must not be satisfied by 15m artifacts.
def test_model_artifact_lookup_is_exact_per_timeframe(tmp_path):
    mod = _load("scripts/check_model_artifacts.py", "check_model_artifacts_t")
    (tmp_path / "xgb_direction_BTCUSDT_15m.joblib").write_bytes(b"x")
    assert mod._artifacts_for(tmp_path, "5m") == []
    assert len(mod._artifacts_for(tmp_path, "15m")) == 1


# OPS-020: a mutmut timeout is a failing verdict, and the cache is cleared per subsystem.
def test_mutation_timeout_scores_as_failed(monkeypatch, tmp_path, capsys):
    mod = _load("scripts/check_mutation_score.py", "check_mutation_score_t")
    monkeypatch.setattr(mod, "PROJECT_ROOT", tmp_path)
    (tmp_path / ".mutmut-cache").write_text("stale")

    def _boom(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="mutmut", timeout=1)

    monkeypatch.setattr(mod.subprocess, "run", _boom)
    result = mod.run_subsystem("risk", {"paths": ["src/risk"], "min_score": 0.8}, timeout_s=1)
    assert result.passed is False
    assert not (tmp_path / ".mutmut-cache").exists()


# DOC-018: the tool decorator must not hide coroutine functions.
def test_tool_decorator_preserves_coroutine_function():
    import inspect

    from tools.registry import tool

    @tool("phase6_low_async_probe_unique", description="probe")
    async def probe():
        return 1

    assert inspect.iscoroutinefunction(probe)
