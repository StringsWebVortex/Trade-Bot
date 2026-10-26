"""Regression tests for atomic execution-mode persistence failures."""

from __future__ import annotations

import json

import pytest

from src.config import ExecutionMode
from src.execution import mode_persistence


def test_failed_atomic_replace_preserves_previous_mode_and_cleans_temp_file(
    tmp_path, monkeypatch
):
    target = tmp_path / "execution_mode.json"
    original = json.dumps({"version": 1, "execution_mode": ExecutionMode.PAPER.value})
    target.write_text(original, encoding="utf-8")

    def fail_replace(_source, _destination):
        raise OSError("simulated filesystem failure")

    monkeypatch.setattr(mode_persistence.os, "replace", fail_replace)

    with pytest.raises(OSError, match="simulated filesystem failure"):
        mode_persistence.save_execution_mode(ExecutionMode.MANUAL, target)

    assert target.read_text(encoding="utf-8") == original
    assert list(tmp_path.glob(".execution_mode-*")) == []


def test_failed_replace_without_an_existing_file_leaves_no_partial_state(
    tmp_path, monkeypatch
):
    target = tmp_path / "nested" / "execution_mode.json"

    def fail_replace(_source, _destination):
        raise OSError("read-only destination")

    monkeypatch.setattr(mode_persistence.os, "replace", fail_replace)

    with pytest.raises(OSError, match="read-only destination"):
        mode_persistence.save_execution_mode(ExecutionMode.MANUAL, target)

    assert not target.exists()
    assert list(target.parent.glob(".execution_mode-*")) == []
