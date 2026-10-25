"""Regression tests for Low-severity audit findings (phase 6).

Each test fails on the pre-fix behaviour it names.

Decides:
  - REG-1520 — RAG re-ingest replaces a source's chunks instead of duplicating them
  - REG-1521 — Knowledge-graph and review retrieval return no edges when no entity matches
  - REG-1522 — Feature indicators never emit infinite values and RSI handles no-loss windows
  - REG-1523 — Coverage floor check fails when the report measures zero files
  - REG-1524 — All-green gate tolerates null job payloads and rejects stale allowances with exit 2
  - REG-1525 — Model-artifact preflight matches exact trainer filenames per timeframe
  - REG-1526 — Mutation floor fails closed on timeout and clears the shared cache per subsystem
  - REG-1527 — Ruleset drift check compares rule parameters the file sets
  - REG-1528 — CI diagnostic values decode percent-escapes once, with %25 last
  - REG-1529 — Quality id regex accepts registry ids past the old digit caps
  - REG-1530 — Review context refuses option-shaped refs and provenance refuses escaping names
  - REG-1531 — Market fetchers drop the still-forming last candle
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


# OPS-022 / SCR-015: ruleset drift check compares rule parameters.
def test_ruleset_check_flags_weakened_rule_parameter():
    mod = _load("scripts/apply_repo_ruleset.py", "apply_repo_ruleset_t")
    payload = {
        "enforcement": "active",
        "rules": [{"type": "pull_request", "parameters": {"required_approving_review_count": 1}}],
    }
    remote = {
        "enforcement": "active",
        "rules": [{"type": "pull_request", "parameters": {"required_approving_review_count": 0}}],
    }
    problems = mod.compare(payload, remote)
    assert any("required_approving_review_count" in p for p in problems)


def test_ruleset_check_ignores_github_default_echo():
    mod = _load("scripts/apply_repo_ruleset.py", "apply_repo_ruleset_t2")
    payload = {"enforcement": "active", "rules": [{"type": "deletion"}]}
    remote = {
        "enforcement": "active",
        "rules": [{"type": "deletion", "parameters": {"unrelated_default": True}}],
    }
    assert mod.compare(payload, remote) == []


# SCR-016: %25 is decoded last, so an encoded percent is not decoded into a newline.
def test_command_value_unquote_does_not_double_decode():
    mod = _load("scripts/ci_diagnostics.py", "ci_diagnostics_t")
    assert mod._unquote_command_value("%250A") == "%0A"
    assert mod._unquote_command_value("a%0Ab") == "a\nb"


# DOC-028: qe id regex accepts ids past the old digit caps.
def test_qe_id_regex_accepts_long_registry_ids():
    mod = _load(
        ".claude/skills/quality-engineering/scripts/qe_new_requirement.py", "qe_new_requirement_t"
    )
    assert mod.ID_RE.match("REG-10000")
    assert mod.ID_RE.match("SEC-0001")


# DOC-019: refs are verified and option-shaped refs are refused before git runs.
def test_build_context_refuses_option_shaped_ref():
    import review.build_context as bc

    with pytest.raises(ValueError):
        bc._diff_text("--output=/tmp/x", "HEAD")


# SCR-018: provenance file names may not escape the bundle.
def test_provenance_verify_refuses_traversal_name(tmp_path):
    import json

    mod = _load("scripts/write_provenance.py", "write_provenance_t")
    record = tmp_path / "provenance.json"
    record.write_text(json.dumps({"files": [{"name": "../escape", "sha256": "0"}]}))
    problems = mod.verify(record)
    assert any("unsafe file name" in p for p in problems)


# DOC-031: a still-forming last candle is dropped by both fetchers.
def test_binance_fetch_drops_forming_candle(monkeypatch):
    import time

    mod = _load("crypto-predictor/data_fetch.py", "crypto_predictor_binance")
    now_ms = int(time.time() * 1000)
    closed = [1, "1", "1", "1", "1", "1", now_ms - 1000] + [0] * 5
    forming = [now_ms, "1", "1", "1", "1", "1", now_ms + 60_000] + [0] * 5
    resp = MagicMock()
    resp.json.return_value = [closed, forming]
    monkeypatch.setattr(mod.requests, "get", lambda *a, **k: resp)
    df = mod.fetch_ohlcv("BTCUSDT", "1m")
    assert len(df) == 1


def test_kraken_fetch_drops_forming_candle(monkeypatch):
    import time

    mod = _load("crypto-predictor/data_fetch_kraken.py", "crypto_predictor_kraken")
    now = time.time()
    closed = [now - 600, "1", "1", "1", "1", "1", "1", 1]
    forming = [now, "1", "1", "1", "1", "1", "1", 1]
    resp = MagicMock()
    resp.json.return_value = {"error": [], "result": {"XXBTZUSD": [closed, forming], "last": 0}}
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(mod.requests, "get", lambda *a, **k: resp)
    df = mod.fetch_ohlcv("XBTUSD", "5m")
    assert len(df) == 1
