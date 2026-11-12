"""
GOV-071: registry entries are added one file each, so pull requests that each
add entries merge in any order.

Every pull request used to append its entries to the tail of the same array in
`config/quality_registry.json`. Two such pull requests conflicted however
unrelated their entries were, and each merge put every other one back into
conflict: on 2026-10-28 all 26 open pull requests conflicted with main, 22 of
them only in shared bookkeeping files. A new entry is now
`config/quality_registry.d/<ID>.json`, and the loader joins those files to the
base file.

Git is never called: the scaffolder runs with `--local-only`, and every
registry here is built under `tmp_path`.

Decides:
  - GOV-071 — Pull requests that each add registry entries merge in any order
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from required_import import require

from src.quality.registry import (
    OVERLAY_DIR,
    REGISTRY_PATH,
    RegistryError,
    load_registry,
    read_registry_document,
)

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / ".claude" / "skills" / "quality-engineering" / "scripts"
sys.path.insert(0, str(SCRIPTS))

require("jsonschema")

import qe_new_requirement as scaffold  # noqa: E402


def _entry(entry_id: str) -> dict:
    return {
        "id": entry_id,
        "kind": "requirement",
        "title": "An entry added by one branch",
        "statement": "A statement long enough to satisfy the schema minimum length.",
        "criticality": "medium",
        "subsystem": "governance",
        "status": "planned",
        "source": "QE-99",
        "planned_in": "PR-001",
        "failure_mode": "Something goes wrong in production, at length.",
    }


@pytest.fixture(scope="module")
def vocabulary() -> dict:
    """The real base file's vocabularies, with no entries of its own."""
    document = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    document["entries"] = []
    return document


@pytest.fixture
def base(tmp_path: Path, vocabulary: dict) -> Path:
    path = tmp_path / "quality_registry.json"
    path.write_text(json.dumps(vocabulary), encoding="utf-8")
    return path


def _add(base: Path, entry: dict, name: str | None = None) -> None:
    overlay = base.with_suffix(".d")
    overlay.mkdir(exist_ok=True)
    (overlay / (name or f"{entry['id']}.json")).write_text(json.dumps(entry), encoding="utf-8")


def test_the_repository_loads_its_entry_files() -> None:
    files = sorted(OVERLAY_DIR.glob("*.json"))
    assert files, "config/quality_registry.d/ holds at least GOV-071"
    registry = load_registry()
    for file in files:
        assert file.stem in registry, file.name


def test_an_entry_file_is_appended_to_the_base(base: Path) -> None:
    _add(base, _entry("GOV-901"))
    _add(base, _entry("GOV-900"))
    ids = [e["id"] for e in read_registry_document(base)["entries"]]
    assert ids == ["GOV-900", "GOV-901"]  # file-name order, whatever was added first
    assert "GOV-901" in load_registry(path=base, root=REPO)


def test_a_file_named_for_another_id_is_refused(base: Path) -> None:
    _add(base, _entry("GOV-900"), name="GOV-901.json")
    with pytest.raises(RegistryError, match="whose id is 'GOV-901'"):
        load_registry(path=base, root=REPO)


def test_an_entry_file_that_is_not_json_is_refused(base: Path) -> None:
    overlay = base.with_suffix(".d")
    overlay.mkdir()
    (overlay / "GOV-900.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(RegistryError, match="GOV-900.json is not valid JSON"):
        load_registry(path=base, root=REPO)


def test_an_entry_file_cannot_redefine_a_base_entry(base: Path) -> None:
    document = json.loads(base.read_text(encoding="utf-8"))
    document["entries"] = [_entry("GOV-900")]
    base.write_text(json.dumps(document), encoding="utf-8")
    _add(base, _entry("GOV-900"))
    with pytest.raises(RegistryError, match="duplicate entry ids: GOV-900"):
        load_registry(path=base, root=REPO)


def test_two_branches_adding_entries_change_disjoint_paths(
    base: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # The scaffolder is how an entry is added. Each "branch" below adds one;
    # the base file stays byte-identical and each entry is a file of its own,
    # so git has nothing to merge line by line and either order is clean.
    monkeypatch.setattr(scaffold, "REGISTRY_PATH", base)
    monkeypatch.setattr(scaffold, "OVERLAY_DIR", base.with_suffix(".d"))
    before = base.read_bytes()
    for entry_id in ("GOV-900", "GOV-901"):
        code = scaffold.main(
            [
                "--id",
                entry_id,
                "--title",
                "An entry added by one branch",
                "--statement",
                "A statement long enough to satisfy the schema minimum length.",
                "--criticality",
                "medium",
                "--subsystem",
                "governance",
                "--source",
                "QE-99",
                "--failure-mode",
                "Something goes wrong in production, at length.",
                "--status",
                "planned",
                "--planned-in",
                "PR-001",
                "--local-only",
            ]
        )
        assert code == 0, capsys.readouterr().out
    capsys.readouterr()
    assert base.read_bytes() == before
    written = sorted(p.name for p in base.with_suffix(".d").iterdir())
    assert written == ["GOV-900.json", "GOV-901.json"]
    loaded = load_registry(path=base, root=REPO)
    assert "GOV-900" in loaded and "GOV-901" in loaded
