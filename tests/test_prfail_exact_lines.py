"""
prfail answers with the exact failure lines of a pull request's CI, or `wait`.

The collector finds every workflow run GitHub started for the pull request
(no fixed list), waits until all of them finish, skips everything green, and
copies the lines that name an error, failure, skip or cancellation. prfail
prints those lines, then one line per unresolved review conversation, and
nothing else; until the report exists it prints `wait`, and a second call made
while one is running prints `wait` as well.

Decides:
  - GOV-068 — prfail prints only the exact failure lines of every non-green PR run, or wait
  - REG-0020 — The collector extracts failure lines server-side and discards everything else
  - REG-0023 — A failure line is copied exactly, so the location it names is kept
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import tempfile
import urllib.parse
from pathlib import Path
from typing import Any

import pytest
import yaml

from scripts import apply_ci_patch, ci_diagnostics
from scripts.ci_diagnostics import _canonical_json, _pack_pages, failure_lines

ROOT = Path(__file__).resolve().parents[1]
SHA = "c" * 40
PR = 521
PULL = {"number": PR, "state": "open", "head": {"sha": SHA, "ref": "feature"}}


@pytest.mark.parametrize(
    "line",
    [
        "##[error]Process completed with exit code 1.",
        "FAILED tests/test_orders.py::test_rejects_bad_order - AssertionError",
        "RuntimeError: Event loop is closed",
        "1 failure, 3 passed",
        "== 2 failed, 10 skipped in 3.2s ==",
        "##[error]The operation was canceled.",
        "Job was CANCELLED by a newer push",
    ],
)
def test_a_line_naming_a_failure_word_is_copied_exactly(line: str) -> None:
    assert failure_lines(f"2026-10-26T10:00:00.0000000Z {line}\n") == [(1, line)]


def test_other_lines_are_left_out_and_order_is_kept() -> None:
    raw = (
        "2026-10-26T10:00:00.0000000Z Run ruff format --check .\n"
        "2026-10-26T10:00:01.0000000Z Would reformat: tests/conftest.py\n"
        "2026-10-26T10:00:02.0000000Z unformatted: File would be reformatted\n"
        "2026-10-26T10:00:03.0000000Z ##[error]Process completed with exit code 1.\n"
    )
    assert failure_lines(raw) == [(4, "##[error]Process completed with exit code 1.")]


def _job(job_id: int, conclusion: str) -> dict[str, Any]:
    return {"id": job_id, "name": f"job {job_id}", "status": "completed", "conclusion": conclusion}


def _run(run_id: int, name: str, conclusion: str, **extra: Any) -> dict[str, Any]:
    return {
        "id": run_id,
        "name": name,
        "workflow_id": run_id,
        "status": "completed",
        "conclusion": conclusion,
        **extra,
    }


@pytest.fixture
def logs(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    """Every job whose log the collector reads, in order."""
    read: list[int] = []

    def job_log(slug: str, job_id: int) -> str:
        read.append(job_id)
        return f"setup ok\nstep {job_id} failed\nstep {job_id} failed\nteardown ok\n"

    monkeypatch.setattr(ci_diagnostics, "_job_log", job_log)
    return read


def test_only_non_green_jobs_of_non_green_runs_are_read(monkeypatch, logs) -> None:
    runs = [_run(1, "CI", "failure"), _run(2, "Security", "success")]
    jobs = {
        1: [_job(10, "success"), _job(11, "failure"), _job(12, "skipped"), _job(13, "cancelled")],
        2: [_job(20, "success")],
    }
    published: list[list[dict[str, Any]]] = []
    monkeypatch.setattr(ci_diagnostics, "_ensure_head_unchanged", lambda *a: None)
    monkeypatch.setattr(ci_diagnostics, "_list_runs_for_pr", lambda *a: runs)
    monkeypatch.setattr(ci_diagnostics, "_jobs_for_run", lambda slug, run_id: jobs[run_id])
    monkeypatch.setattr(ci_diagnostics, "_report_runs", lambda *a: (None, {}))
    monkeypatch.setattr(ci_diagnostics, "_publish_report", lambda *a: published.append(a[-1]))

    ci_diagnostics._collect_and_publish("o/r", PULL, PR, SHA, 7, 1)

    assert logs == [11, 13]
    ((first, second),) = published
    assert [r["message"] for r in (first, second)] == ["step 11 failed", "step 13 failed"]
    assert (first["workflow_run_id"], first["job_id"], first["line_number"]) == (1, 11, 2)


def test_unfinished_runs_leave_the_report_waiting(monkeypatch, logs) -> None:
    monkeypatch.setattr(ci_diagnostics, "COLLECT_DEADLINE_SECONDS", 0)
    with pytest.raises(ci_diagnostics.RunsPending):
        ci_diagnostics._collect_and_publish("o/r", PULL, PR, SHA, 7, 1)
    assert logs == []


def test_every_pull_request_workflow_is_found_without_a_list(monkeypatch) -> None:
    pr_link = [{"number": PR, "head": {"sha": SHA}}]
    common = {"event": "pull_request", "head_branch": "feature", "pull_requests": pr_link}
    listed = [
        _run(1, "CI", "failure", run_number=4, **common),
        _run(1, "CI", "success", run_number=5, **common) | {"id": 11},
        _run(2, "A workflow added next year", "failure", **common),
        _run(3, "CI non-success diagnostics", "success", **common)
        | {"path": ci_diagnostics.SELF_WORKFLOW_PATH},
    ]
    queried: list[str] = []

    def pages(path: str, key: str) -> list[dict[str, Any]]:
        queried.append(path)
        return listed

    monkeypatch.setattr(ci_diagnostics, "_pages", pages)

    runs = ci_diagnostics._list_runs_for_pr("o/r", PULL, SHA)

    assert [(run["name"], run["id"]) for run in runs] == [
        ("A workflow added next year", 2),
        ("CI", 11),
    ]
    (path,) = queried
    assert urllib.parse.parse_qs(path.split("?", 1)[1]) == {
        "head_sha": [SHA],
        "event": ["pull_request"],
    }
    assert not hasattr(ci_diagnostics, "WORKFLOW_INVENTORY")


def test_the_collector_trigger_is_every_workflow() -> None:
    workflow = yaml.safe_load((ROOT / ".github/workflows/ci-diagnostics.yml").read_text())
    triggers = workflow.get("on") or workflow.get(True)
    assert triggers["workflow_run"]["workflows"] == ["*"]


def _master(summary: dict[str, Any], conclusion: str = "success") -> dict[str, Any]:
    return {
        "status": "completed",
        "conclusion": conclusion,
        "head_sha": SHA,
        "output": {"summary": _canonical_json(summary)},
    }


def _finished(messages: list[str]) -> tuple[dict[str, Any], dict[int, dict[str, Any]]]:
    records = [
        {
            "repository": "o/r",
            "pr": PR,
            "head_sha": SHA,
            "workflow_name": "CI",
            "workflow_run_id": 1,
            "job_id": job_id,
            "job_name": f"job {job_id}",
            "line_number": 1,
            "message": message,
        }
        for job_id, message in enumerate(messages, start=1)
    ]
    digest = hashlib.sha256(_canonical_json(records).encode()).hexdigest()
    pages = {
        number: {
            "status": "completed",
            "conclusion": "success",
            "head_sha": SHA,
            "output": {
                "summary": _canonical_json(
                    {
                        "schema_version": 2,
                        "generation_id": digest[:24],
                        "page": number,
                        "page_count": len(packed),
                    }
                ),
                "text": _canonical_json(page),
            },
        }
        for packed in [_pack_pages(records)]
        for number, page in enumerate(packed, start=1)
    }
    manifest = {
        "schema_version": 2,
        "status": "finalized",
        "pr": PR,
        "head_sha": SHA,
        "generation_id": digest[:24],
        "diagnostic_count": len(records),
        "page_count": len(pages),
        "digest": digest,
    }
    return _master(manifest), pages


@pytest.fixture
def github(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict[str, Any]:
    state: dict[str, Any] = {"report": (None, {}), "thread_pages": [[]], "graphql": []}
    # prfail's one-call-at-a-time lock lives in the temp directory.
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    monkeypatch.setattr(ci_diagnostics, "_repo_slug", lambda: "o/r")
    monkeypatch.setattr(ci_diagnostics, "_load_current_pr", lambda slug, pr: PULL)
    monkeypatch.setattr(ci_diagnostics, "_report_runs", lambda *a: state["report"])

    def graphql(path: str, *, method: str = "GET", body: Any = None, **kw: Any) -> Any:
        assert (path, method) == ("graphql", "POST")
        state["graphql"].append(body["variables"])
        index = len(state["graphql"]) - 1
        pages = state["thread_pages"]
        return {
            "data": {
                "repository": {
                    "pullRequest": {
                        "reviewThreads": {
                            "pageInfo": {
                                "hasNextPage": index + 1 < len(pages),
                                "endCursor": f"cursor-{index}",
                            },
                            "nodes": pages[index],
                        }
                    }
                }
            }
        }

    monkeypatch.setattr(ci_diagnostics, "_json", graphql)
    return state


def _thread(resolved: bool, path: str, line: int | None, body: str, **extra: Any) -> dict:
    return {
        "isResolved": resolved,
        "path": path,
        "line": line,
        "originalLine": None,
        "comments": {"nodes": [{"body": body}]},
        **extra,
    }


def test_unresolved_conversations_follow_the_failure_lines(github, capsys) -> None:
    github["report"] = _finished(["##[error]Process completed with exit code 1."])
    github["thread_pages"] = [
        [
            _thread(False, "SECURITY.md", 12, "\n**P2: CodeQL wording is wrong**\nLong detail."),
            _thread(True, "AGENTS.md", 3, "Resolved already"),
        ],
        # An outdated thread has no current line; it still blocks the merge.
        [_thread(False, "tests/conftest.py", None, "Leaks a loop", originalLine=40)],
    ]
    assert ci_diagnostics.main_prfail(["--pr", str(PR)]) == 0
    assert capsys.readouterr().out == (
        "##[error]Process completed with exit code 1.\n"
        "SECURITY.md:12: **P2: CodeQL wording is wrong**\n"
        "tests/conftest.py:40: Leaks a loop\n"
    )
    assert [page["after"] for page in github["graphql"]] == [None, "cursor-0"]
    assert {page["number"] for page in github["graphql"]} == {PR}


def test_unresolved_conversations_alone_are_printed_when_ci_is_green(github, capsys) -> None:
    github["report"] = _finished([])
    github["thread_pages"] = [[_thread(False, "README.md", 1, "Typo")]]
    assert ci_diagnostics.main_prfail(["--pr", str(PR)]) == 0
    assert capsys.readouterr().out == "README.md:1: Typo\n"


def test_conversations_are_not_read_while_the_report_waits(github, capsys) -> None:
    github["thread_pages"] = [[_thread(False, "README.md", 1, "Typo")]]
    assert ci_diagnostics.main_prfail(["--pr", str(PR)]) == ci_diagnostics.WAIT_EXIT
    assert capsys.readouterr().out == "wait\n"
    assert github["graphql"] == []


@pytest.mark.parametrize(
    "nodes",
    [[{"path": "a.py"}], None],
    ids=["no-resolved-state", "no-thread-list"],
)
def test_an_unreadable_thread_list_is_an_error_not_silence(github, capsys, nodes) -> None:
    github["report"] = _finished([])
    github["thread_pages"] = [nodes]
    assert ci_diagnostics.main_prfail(["--pr", str(PR)]) == 2
    out, err = capsys.readouterr()
    assert out == "" and "review thread" in err


def test_prfail_prints_only_the_lines(github, capsys) -> None:
    github["report"] = _finished(
        ["##[error]Process completed with exit code 1.", "FAILED tests/test_a.py::test_x"]
        + ["##[error]Process completed with exit code 1."]
    )
    assert ci_diagnostics.main_prfail(["--pr", str(PR)]) == 0
    assert capsys.readouterr().out == (
        "##[error]Process completed with exit code 1.\nFAILED tests/test_a.py::test_x\n"
    )


def test_prfail_prints_nothing_when_nothing_failed(github, capsys) -> None:
    github["report"] = _finished([])
    assert ci_diagnostics.main_prfail(["--pr", str(PR)]) == 0
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "report",
    [
        (None, {}),
        ({"status": "in_progress", "head_sha": SHA}, {}),
        (
            _master({"status": "failed", "waiting": True, "reason": "runs still going"}, "neutral"),
            {},
        ),
    ],
    ids=["no-report-yet", "collector-running", "runs-still-going"],
)
def test_prfail_says_wait_until_the_runs_are_done(github, capsys, report) -> None:
    github["report"] = report
    assert ci_diagnostics.main_prfail(["--pr", str(PR)]) == ci_diagnostics.WAIT_EXIT
    assert capsys.readouterr() == ("wait\n", "")


def test_a_broken_collection_is_an_error_not_a_wait(github, capsys) -> None:
    github["report"] = (_master({"status": "failed", "reason": "API down"}, "neutral"), {})
    assert ci_diagnostics.main_prfail(["--pr", str(PR)]) == 2
    out, err = capsys.readouterr()
    assert out == "" and "API down" in err


def test_a_second_prfail_while_one_runs_only_says_wait(github, capsys, monkeypatch) -> None:
    def must_not_read(pr: int) -> None:
        raise AssertionError("the second call read the report")

    monkeypatch.setattr(ci_diagnostics, "read_report", must_not_read)
    lock_path = Path(tempfile.gettempdir()) / f"tradebot-prfail-{PR}.lock"
    with open(lock_path, "a", encoding="utf-8") as first_call:
        fcntl.flock(first_call, fcntl.LOCK_EX)
        assert ci_diagnostics.main_prfail(["--pr", str(PR)]) == ci_diagnostics.WAIT_EXIT
    assert capsys.readouterr().out == "wait\n"


def test_the_patch_applier_refuses_while_the_report_waits(github) -> None:
    with pytest.raises(apply_ci_patch.PatchError, match="not finished yet"):
        apply_ci_patch._verify_diagnostic_report(PR, SHA)


def test_the_patch_applier_accepts_a_finished_report_for_its_head(github) -> None:
    github["report"] = _finished(["##[error]Process completed with exit code 1."])
    apply_ci_patch._verify_diagnostic_report(PR, SHA)
    with pytest.raises(apply_ci_patch.PatchError, match="does not match"):
        apply_ci_patch._verify_diagnostic_report(PR, "d" * 40)


def test_the_report_holds_lines_not_structured_fields(github) -> None:
    github["report"] = _finished(["FAILED tests/test_a.py::test_x"])
    _sha, (record,) = ci_diagnostics.read_report(PR)
    assert set(record) == {
        "repository",
        "pr",
        "head_sha",
        "workflow_name",
        "workflow_run_id",
        "job_id",
        "job_name",
        "line_number",
        "message",
    }
    assert json.dumps(record)  # serializable as delivered
