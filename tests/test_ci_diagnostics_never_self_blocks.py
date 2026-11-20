"""REG-1604: the collector never leaves its own report check ``in_progress``.

A check run the collector creates with GITHUB_TOKEN joins a source workflow
run's check suite. The collector used to open the master ``in_progress``
before waiting for every source workflow to finish, which held one of those
runs open, so the wait never ended: every ``./scripts/prfail`` call answered
"Diagnostics report is not finalized" and no report was ever published.

* nothing in the collector writes an ``in_progress`` check run;
* a master an older collector left ``in_progress`` is settled before waiting;
* a successful collection writes the master once, completed;
* a failed collection records its reason, and ``prfail`` reports it.

Decides: REG-1604"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

import pytest

from scripts import ci_diagnostics
from scripts.ci_diagnostics import DiagnosticError, _canonical_json

ROOT = Path(__file__).resolve().parents[1]
SHA = "b" * 40
PR = 509


def test_no_collector_call_writes_an_in_progress_check() -> None:
    tree = ast.parse((ROOT / "scripts/ci_diagnostics.py").read_text(encoding="utf-8"))
    offending: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for kw in node.keywords:
            if kw.arg == "status" and getattr(kw.value, "value", None) in {"in_progress", "queued"}:
                offending.append(node.lineno)
    assert offending == []


class _Checks:
    """The master check run as GitHub would hold it, plus every write."""

    def __init__(self, master: dict[str, Any] | None = None) -> None:
        self.master = master
        self.writes: list[dict[str, Any]] = []

    def report_runs(self, slug: str, sha: str, pr: int):
        return self.master, {}

    def upsert(self, slug, sha, name, external_id, existing, **kw) -> dict[str, Any]:
        write = {"name": name, "existing": existing, **kw}
        self.writes.append(write)
        result = {
            "id": 1,
            "status": kw["status"],
            "conclusion": kw.get("conclusion", "success") if kw["status"] == "completed" else None,
            "head_sha": sha,
            "output": kw["output"],
        }
        if name == ci_diagnostics.MASTER_NAME:
            self.master = result
        return result


@pytest.fixture
def checks(monkeypatch: pytest.MonkeyPatch) -> _Checks:
    store = _Checks()
    monkeypatch.setattr(ci_diagnostics, "_report_runs", store.report_runs)
    monkeypatch.setattr(ci_diagnostics, "_upsert_check_run", store.upsert)
    return store


def test_a_stale_in_progress_master_is_settled(checks: _Checks) -> None:
    checks.master = {"id": 5, "status": "in_progress", "head_sha": SHA}
    ci_diagnostics._settle_stale_master("o/r", PR, SHA, 7, 1)
    (write,) = checks.writes
    assert write["existing"]["id"] == 5
    assert write["status"] == "completed" and write["conclusion"] == "neutral"
    assert json.loads(write["output"]["summary"])["status"] == "failed"


def test_a_completed_master_is_left_alone(checks: _Checks) -> None:
    checks.master = {"id": 5, "status": "completed", "conclusion": "success"}
    ci_diagnostics._settle_stale_master("o/r", PR, SHA, 7, 1)
    assert checks.writes == []


@pytest.fixture
def collector_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    event = tmp_path / "event.json"
    trigger = {"name": "CI", "status": "completed", "event": "pull_request"}
    event.write_text(json.dumps({"workflow_run": trigger}), encoding="utf-8")
    for key, value in {
        "GITHUB_EVENT_PATH": str(event),
        "GITHUB_EVENT_NAME": "workflow_run",
        "GITHUB_ACTIONS": "true",
        "GITHUB_REPOSITORY": "o/r",
        "GITHUB_RUN_ID": "7",
        "GITHUB_RUN_ATTEMPT": "1",
    }.items():
        monkeypatch.setenv(key, value)
    pull = {"number": PR, "head": {"sha": SHA, "ref": "feature"}, "base": {"ref": "main"}}
    monkeypatch.setattr(ci_diagnostics, "_resolve_pr_from_event", lambda slug, trig: pull)
    monkeypatch.setattr(ci_diagnostics, "_matches_pr_run", lambda run, pr, sha: True)
    monkeypatch.setattr(ci_diagnostics, "_ensure_head_unchanged", lambda *a: None)
    runs = [
        {"id": i, "name": name, "status": "completed", "conclusion": "success"}
        for i, name in enumerate(("CI", "Security"))
    ]
    monkeypatch.setattr(ci_diagnostics, "_list_runs_for_pr", lambda *a: runs)
    job = {"id": 1, "name": "lint", "status": "completed", "conclusion": "success", "steps": []}
    monkeypatch.setattr(ci_diagnostics, "_jobs_for_run", lambda slug, run_id: [dict(job)])
    monkeypatch.setattr(ci_diagnostics, "_add_failure_lines", lambda *a: None)


@pytest.mark.usefixtures("collector_env")
def test_collection_writes_only_completed_checks_and_finalizes(checks: _Checks) -> None:
    assert ci_diagnostics._collect() == 0
    assert all(write["status"] == "completed" for write in checks.writes)
    assert checks.master is not None and checks.master["conclusion"] == "success"
    assert json.loads(checks.master["output"]["summary"])["status"] == "finalized"


@pytest.mark.usefixtures("collector_env")
def test_a_failed_collection_records_why(checks: _Checks, monkeypatch, capsys) -> None:
    def no_runs(*args: object) -> list[dict[str, Any]]:
        raise DiagnosticError(
            "GitHub API response is missing the expected workflow_runs collection"
        )

    monkeypatch.setattr(ci_diagnostics, "_list_runs_for_pr", no_runs)
    with pytest.raises(DiagnosticError):
        ci_diagnostics._collect()
    assert checks.master is not None and checks.master["status"] == "completed"
    assert checks.master["conclusion"] == "neutral"

    monkeypatch.setattr(ci_diagnostics, "_repo_slug", lambda: "o/r")
    monkeypatch.setattr(
        ci_diagnostics,
        "_load_current_pr",
        lambda slug, pr: {"number": pr, "state": "open", "head": {"sha": SHA}},
    )
    assert ci_diagnostics._retrieve(PR) != 0
    err = capsys.readouterr().err
    assert "Diagnostics collection failed: GitHub API response is missing" in err


@pytest.mark.usefixtures("collector_env")
def test_a_failure_never_replaces_a_finalized_report(checks: _Checks, monkeypatch) -> None:
    finalized = {"status": "finalized", "pr": PR, "head_sha": SHA}
    checks.master = {
        "id": 3,
        "status": "completed",
        "conclusion": "success",
        "output": {"summary": _canonical_json(finalized)},
    }

    def head_changed(*args: object) -> None:
        raise DiagnosticError("Pull-request head changed or closed while collecting")

    monkeypatch.setattr(ci_diagnostics, "_collect_and_publish", head_changed)
    with pytest.raises(DiagnosticError, match="head changed"):
        ci_diagnostics._collect()
    assert checks.writes == []
