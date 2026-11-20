"""Tests for the non-executing quality-registry traceability audit."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / ".claude/skills/quality-engineering/scripts/qe_evidence.py"
sys.path.insert(0, str(SCRIPT.parent))
import qe_evidence  # noqa: E402


def _fixture(tmp_path: Path, entries: list[dict]) -> Path:
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests/example.py").write_text("# fixture\n", encoding="utf-8")
    (tmp_path / "config").mkdir()
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["entries"],
        "properties": {"entries": {"type": "array"}},
    }
    (tmp_path / "config/registry.schema.json").write_text(json.dumps(schema), encoding="utf-8")
    (tmp_path / "config/registry.json").write_text(json.dumps({"entries": entries}), encoding="utf-8")
    return tmp_path


def _entry(entry_id: str = "RISK-001", test: str = "tests/example.py", deps=None) -> dict:
    return {
        "id": entry_id,
        "verification": [{"test": test, "test_type": "unit"}],
        "depends_on": deps or [],
    }


def test_valid_registry_has_deterministic_clean_report(tmp_path):
    root = _fixture(tmp_path, [_entry()])
    first = qe_evidence.audit(root, "config/registry.json", "config/registry.schema.json")
    second = qe_evidence.audit(root, "config/registry.json", "config/registry.schema.json")
    assert first["passed"] is True
    assert first == second
    assert first["entry_count"] == 1


def test_duplicate_ids_are_reported(tmp_path):
    root = _fixture(tmp_path, [_entry(), _entry()])
    report = qe_evidence.audit(root, "config/registry.json", "config/registry.schema.json")
    assert "DUPLICATE_ID" in {item["code"] for item in report["findings"]}


def test_missing_test_is_reported(tmp_path):
    root = _fixture(tmp_path, [_entry(test="tests/missing.py")])
    report = qe_evidence.audit(root, "config/registry.json", "config/registry.schema.json")
    assert "TEST_MISSING" in {item["code"] for item in report["findings"]}


def test_parent_traversal_is_rejected(tmp_path):
    root = _fixture(tmp_path, [_entry(test="tests/../outside.py")])
    report = qe_evidence.audit(root, "config/registry.json", "config/registry.schema.json")
    assert "TEST_PATH_INVALID" in {item["code"] for item in report["findings"]}


def test_symlink_escape_is_rejected(tmp_path):
    root = _fixture(tmp_path, [_entry(test="tests/escape.py")])
    outside = tmp_path.parent / "outside.py"
    outside.write_text("# outside\n", encoding="utf-8")
    (root / "tests/escape.py").symlink_to(outside)
    report = qe_evidence.audit(root, "config/registry.json", "config/registry.schema.json")
    assert "TEST_MISSING" in {item["code"] for item in report["findings"]}


def test_missing_dependency_is_reported(tmp_path):
    root = _fixture(tmp_path, [_entry(deps=["RISK-999"])])
    report = qe_evidence.audit(root, "config/registry.json", "config/registry.schema.json")
    assert "DEPENDENCY_MISSING" in {item["code"] for item in report["findings"]}


def test_dependency_cycle_is_reported(tmp_path):
    root = _fixture(tmp_path, [_entry("RISK-001", deps=["RISK-002"]), _entry("RISK-002", deps=["RISK-001"])])
    report = qe_evidence.audit(root, "config/registry.json", "config/registry.schema.json")
    assert "DEPENDENCY_CYCLE" in {item["code"] for item in report["findings"]}


def test_schema_invalid_registry_fails(tmp_path):
    root = _fixture(tmp_path, [_entry()])
    (root / "config/registry.json").write_text('{"not_entries": []}', encoding="utf-8")
    report = qe_evidence.audit(root, "config/registry.json", "config/registry.schema.json")
    assert report["passed"] is False
    assert "SCHEMA_INVALID" in {item["code"] for item in report["findings"]}
