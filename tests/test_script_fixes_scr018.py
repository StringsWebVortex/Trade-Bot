"""REG-1610: four repository scripts do what they say (audit SCR-018).

* ``resolve_registry_merge.py`` reported an add/add conflict, which has no
  stage 1, as "not in a conflicted merge state". It now merges against an
  empty base.
* ``generate_signal_fixtures.py --check`` created the fixtures directory, and
  a fixture left behind by a removed case went unnoticed. ``--check`` now only
  reads and reports the orphan; a write removes it.
* ``collect_quality_metrics.py`` published coverage's combined line and
  branch total as ``branch_coverage_pct``. The metric is now named for what
  it measures.
* ``codebase_knowledge_index.py --refresh-file-index`` dropped everything
  after the file table. Content after the table is now kept.

Decides: REG-1610"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"{name}_reg1610", _SCRIPTS / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# resolve_registry_merge.py: add/add conflicts
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def resolver() -> ModuleType:
    return _load("resolve_registry_merge")


def _doc(*ids: str) -> dict:
    return {"registry_version": 1, "entries": [{"id": i, "title": "t"} for i in ids]}


def _stages(monkeypatch, resolver: ModuleType, stages: dict[int, dict]) -> None:
    def stage(n: int, _path: str) -> tuple[dict, str]:
        if n not in stages:
            raise subprocess.CalledProcessError(128, ["git", "show", f":{n}:x"])
        return stages[n], json.dumps(stages[n], indent=2)

    monkeypatch.setattr(resolver, "_stage", stage)


def test_an_add_add_conflict_merges_against_an_empty_base(resolver, monkeypatch, tmp_path) -> None:
    _stages(monkeypatch, resolver, {2: _doc("A", "OURS"), 3: _doc("A", "THEIRS")})
    path = tmp_path / "registry.json"
    assert resolver.main(["resolve_registry_merge.py", str(path)]) == 0
    merged = json.loads(path.read_text(encoding="utf-8"))
    assert [e["id"] for e in merged["entries"]] == ["A", "THEIRS", "OURS"]


def test_an_add_add_conflict_with_one_id_written_twice_is_refused(
    resolver, monkeypatch, tmp_path
) -> None:
    ours, theirs = _doc("A"), _doc("A")
    theirs["entries"][0]["title"] = "different"
    _stages(monkeypatch, resolver, {2: ours, 3: theirs})
    path = tmp_path / "registry.json"
    assert resolver.main(["resolve_registry_merge.py", str(path)]) == 1
    assert not path.exists()


def test_a_file_with_no_conflict_stages_is_still_reported(
    resolver, monkeypatch, tmp_path, capsys
) -> None:
    _stages(monkeypatch, resolver, {})
    assert resolver.main(["resolve_registry_merge.py", str(tmp_path / "r.json")]) == 1
    assert "not in a conflicted merge state" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# generate_signal_fixtures.py: --check only reads, orphans are found
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def generator() -> ModuleType:
    return _load("generate_signal_fixtures")


@pytest.fixture
def fixtures(generator, monkeypatch, tmp_path):
    cases = [SimpleNamespace(case_id="case_a"), SimpleNamespace(case_id="case_b")]
    monkeypatch.setattr(generator, "CASES", cases)
    monkeypatch.setattr(generator, "build_record", lambda case: {"case": case.case_id})
    monkeypatch.setattr(generator, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(generator, "OUTPUT_DIR", tmp_path / "signals")
    return generator


def test_check_does_not_create_the_fixtures_directory(fixtures, tmp_path) -> None:
    assert fixtures.main(["--check"]) == 1
    assert not (tmp_path / "signals").exists()


def test_check_reports_a_fixture_whose_case_was_removed(fixtures, tmp_path, capsys) -> None:
    assert fixtures.main([]) == 0
    (tmp_path / "signals" / "case_gone.json").write_text("{}\n", encoding="utf-8")
    capsys.readouterr()

    assert fixtures.main(["--check"]) == 1
    assert "case_gone.json has no case" in capsys.readouterr().out
    assert (tmp_path / "signals" / "case_gone.json").exists()


def test_a_write_removes_the_orphan_so_check_passes_again(fixtures, tmp_path) -> None:
    assert fixtures.main([]) == 0
    (tmp_path / "signals" / "case_gone.json").write_text("{}\n", encoding="utf-8")

    assert fixtures.main([]) == 0
    assert sorted(p.name for p in (tmp_path / "signals").iterdir()) == [
        "case_a.json",
        "case_b.json",
    ]
    assert fixtures.main(["--check"]) == 0


# ---------------------------------------------------------------------------
# collect_quality_metrics.py: the coverage metric's name
# ---------------------------------------------------------------------------


def test_the_coverage_metric_is_not_called_branch_coverage(monkeypatch, tmp_path) -> None:
    collector = _load("collect_quality_metrics")
    (tmp_path / ".coverage").write_bytes(b"")
    report = {"totals": {"percent_covered": 98.25}, "files": {"a.py": {}}}
    monkeypatch.setattr(collector, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(
        collector.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout=json.dumps(report)),
    )
    metrics = collector.coverage_metrics()
    assert "branch_coverage_pct" not in metrics
    assert metrics["line_and_branch_coverage_pct"]["value"] == 98.25


# ---------------------------------------------------------------------------
# codebase_knowledge_index.py: content after the file table
# ---------------------------------------------------------------------------


def test_refresh_keeps_what_follows_the_file_table(monkeypatch, tmp_path) -> None:
    indexer = _load("codebase_knowledge_index")
    source = tmp_path / "src" / "example.py"
    source.parent.mkdir()
    source.write_text("x = 1\n", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:8]
    index = (
        "# File Index\n\n"
        "## Complete tracked-file index\n"
        "| # | Priority | Path | Type | Lines | SHA8 | Notes |\n"
        "| ---: | --- | --- | --- | ---: | --- | --- |\n"
        "| 1 | P1 | src/example.py | Python | 9 | 00000000 | keep |\n"
        "\n## Appendix\n\nWritten after the table.\n"
    )
    monkeypatch.setattr(indexer, "tracked_paths", lambda root: {"src/example.py"})

    refreshed, issues = indexer.refresh_file_index(index, tmp_path)

    assert not issues
    assert f"| 1 | P1 | src/example.py | Python | 1 | {digest} | keep |" in refreshed
    assert refreshed.endswith("\n## Appendix\n\nWritten after the table.\n")
