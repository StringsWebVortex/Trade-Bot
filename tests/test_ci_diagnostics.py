"""Collector, report reader and patch-applier contracts for CI diagnostics.

Decides:
  - GOV-013 — CI diagnostics are collected autonomously and never require log polling
  - GOV-020 — One SHA-bound report carries the exact failure lines of every non-green run
  - REG-0020 — The collector extracts failure lines server-side and discards everything else
  - REG-0021 — The collector correlates the exact open PR head before publishing
  - REG-0023 — A failure line is copied exactly, so the location it names is kept
  - REG-0024 — Agent diagnostic retrieval is one canonical command; local checks stay disabled
"""

from __future__ import annotations

import hashlib
import io
import zipfile
from pathlib import Path

import yaml

from scripts import ci_diagnostics
from scripts.ci_diagnostics import (
    REPORT_PAGE_BYTES,
    DiagnosticError,
    _all_jobs_terminal,
    _canonical_invocation,
    _canonical_json,
    _decode_job_log_payload,
    _decode_report_pages,
    _external_id,
    _matches_pr_run,
    _pack_pages,
    _page_external_id,
    _redact_message,
    _token,
    failure_lines,
)

ROOT = Path(__file__).resolve().parents[1]


def test_job_log_zip_archive_is_decoded_without_extracting_files() -> None:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("1_Setup.txt", "setup completed\n")
        archive.writestr(
            "2_Tests.txt", "FAILED tests/test_orders.py::test_order - AssertionError\n"
        )
    decoded = _decode_job_log_payload(buffer.getvalue(), 42)
    assert "setup completed" in decoded
    assert "FAILED tests/test_orders.py::test_order - AssertionError" in decoded


def test_malformed_job_log_archive_fails_closed() -> None:
    try:
        _decode_job_log_payload(bytes([255, 254, 253, 0, 1]), 42)
    except DiagnosticError as exc:
        assert "unrecognized job log archive" in str(exc)
    else:
        raise AssertionError("an invalid job-log payload must not be treated as a complete log")


def test_successful_log_volume_has_no_failure_lines() -> None:
    raw = "".join(
        f"2026-10-16T10:00:{i % 60:02d}.000Z step printed normal line {i}\n" for i in range(5000)
    )
    assert failure_lines(raw) == []


def test_message_fragments_reassemble_without_truncation() -> None:
    record = {
        "repository": "owner/repo",
        "pr": 9,
        "head_sha": "a" * 40,
        "workflow_name": "CI",
        "workflow_run_id": 10,
        "job_id": 11,
        "job_name": "unit",
        "line_number": 1,
        "message": "x" * (REPORT_PAGE_BYTES * 3),
    }
    pages = _pack_pages([record])
    fragments = [entry for page in pages for entry in page]
    assert len(fragments) > 1
    assert len(pages) > 1
    assert (
        "".join(
            entry["message_fragment"] or ""
            for entry in sorted(fragments, key=lambda f: f["message_part_index"])
        )
        == record["message"]
    )
    assert all(len(_canonical_json(page).encode("utf-8")) <= REPORT_PAGE_BYTES for page in pages)


def test_report_reader_rejects_stale_page() -> None:
    record = {
        "repository": "owner/repo",
        "pr": 9,
        "head_sha": "a" * 40,
        "workflow_name": "CI",
        "workflow_run_id": 10,
        "job_id": 11,
        "job_name": "unit",
        "line_number": 1,
        "message": "##[error]Process completed with exit code 1.",
    }
    digest = hashlib.sha256(_canonical_json([record]).encode()).hexdigest()
    packed = _pack_pages([record])
    page = {
        "status": "completed",
        "conclusion": "success",
        "head_sha": "b" * 40,
        "output": {
            "summary": _canonical_json(
                {"schema_version": 2, "generation_id": digest[:24], "page": 1, "page_count": 1}
            ),
            "text": _canonical_json(packed[0]),
        },
    }
    manifest = {
        "page_count": 1,
        "generation_id": digest[:24],
        "diagnostic_count": 1,
        "digest": digest,
    }
    try:
        _decode_report_pages(9, "a" * 40, manifest, {1: page})
    except Exception as exc:
        assert "not finalized on the requested SHA" in str(exc)
    else:
        raise AssertionError("stale report page was accepted")


def test_collector_waits_for_terminal_steps_and_jobs() -> None:
    success = {"conclusion": "success"}
    assert not _all_jobs_terminal([{"status": "in_progress", "steps": []}], success)
    # A completed (failed/cancelled) job whose later steps never started is final.
    assert _all_jobs_terminal(
        [
            {
                "status": "completed",
                "conclusion": "cancelled",
                "steps": [{"status": "pending", "conclusion": None}],
            }
        ],
        {"conclusion": "cancelled"},
    )
    assert _all_jobs_terminal(
        [{"status": "completed", "steps": [{"status": "completed", "conclusion": "skipped"}]}],
        success,
    )
    assert not _all_jobs_terminal([], success)


def test_collector_does_not_wait_on_its_own_report_checks(monkeypatch) -> None:
    real_job = {
        "name": "pytest",
        "status": "completed",
        "steps": [{"status": "completed", "conclusion": "failure"}],
    }
    listed = [
        real_job,
        {"name": ci_diagnostics.MASTER_NAME, "status": "in_progress", "steps": []},
        {"name": f"{ci_diagnostics.PAGE_PREFIX}0001", "status": "in_progress", "steps": []},
    ]
    monkeypatch.setattr(ci_diagnostics, "_pages", lambda path, key: list(listed))

    jobs = ci_diagnostics._jobs_for_run("owner/repo", 7)

    assert jobs == [real_job]
    assert _all_jobs_terminal(jobs, {"conclusion": "failure"})


def test_report_identity_is_pr_and_sha_specific() -> None:
    sha_a, sha_b = "a" * 40, "b" * 40
    assert _external_id(313, sha_a) != _external_id(313, sha_b)
    assert _external_id(313, sha_a) != _external_id(314, sha_a)
    assert _page_external_id(313, sha_a, 1) != _page_external_id(313, sha_a, 2)
    assert _page_external_id(313, sha_a, 1) != _page_external_id(314, sha_a, 1)


def test_run_correlation_never_falls_back_across_another_pr_association() -> None:
    pull = {"number": 313, "head": {"ref": "feature", "sha": "a" * 40}}
    run = {
        "event": "pull_request",
        "head_branch": "feature",
        "head_sha": "synthetic-merge-sha",
        "pull_requests": [{"number": 314, "head": {"sha": "a" * 40}}],
    }
    assert not _matches_pr_run(run, pull, "a" * 40)
    run["pull_requests"] = [{"number": 313, "head": {"sha": "a" * 40}}]
    assert _matches_pr_run(run, pull, "a" * 40)
    run["pull_requests"][0]["head"]["sha"] = "b" * 40
    assert not _matches_pr_run(run, pull, "a" * 40)


def test_report_cli_grammar_is_exact_and_rejects_extra_selectors() -> None:
    assert _canonical_invocation(["--pr", "313"]) == 313
    for args in (
        [],
        ["--pr", "0"],
        ["--pr", "-1"],
        ["--pr", "0313"],
        ["--pr", "313", "--run-id", "9"],
        ["--pr", "313", "--job-id", "7"],
        ["--pr=313"],
        ["313"],
    ):
        assert _canonical_invocation(args) is None


def test_report_cli_uses_existing_gh_auth_without_extra_token(monkeypatch) -> None:
    import subprocess

    monkeypatch.setattr(
        ci_diagnostics.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0], returncode=0, stdout="existing_cli_token\n", stderr=""
        ),
    )
    monkeypatch.delenv("PRFAIL_TOKEN", raising=False)
    monkeypatch.setenv("GITHUB_TOKEN", "collector_token_must_not_be_used")
    monkeypatch.setenv("GH_TOKEN", "environment_token_must_not_be_used")
    assert _token() == "existing_cli_token"


def test_diagnostic_message_redaction_masks_tokens_and_secret_assignments(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "gho_test_secret_value_123456789")
    raw = (
        "Bearer abcdefghijklmnop token=inline_secret_value "
        "GITHUB_TOKEN=gho_test_secret_value_123456789"
    )
    masked = _redact_message(raw)
    assert "gho_test_secret_value_123456789" not in masked
    assert "abcdefghijklmnop" not in masked
    assert "inline_secret_value" not in masked
    assert "[REDACTED" in masked


def test_empty_finalized_report_returns_no_stdout(monkeypatch, capsys) -> None:
    sha = "a" * 40
    digest = hashlib.sha256(_canonical_json([]).encode()).hexdigest()
    manifest = {
        "schema_version": 2,
        "status": "finalized",
        "pr": 313,
        "head_sha": sha,
        "generation_id": digest[:24],
        "diagnostic_count": 0,
        "page_count": 0,
        "digest": digest,
        "collector_run_id": 99,
        "collector_run_attempt": 1,
    }
    master = {
        "status": "completed",
        "conclusion": "success",
        "head_sha": sha,
        "output": {"summary": _canonical_json(manifest)},
    }
    monkeypatch.setattr(ci_diagnostics, "_repo_slug", lambda: "owner/repo")
    monkeypatch.setattr(
        ci_diagnostics,
        "_load_current_pr",
        lambda slug, pr: {"number": pr, "state": "open", "head": {"sha": sha}},
    )
    monkeypatch.setattr(ci_diagnostics, "_report_runs", lambda slug, head, pr: (master, {}))
    assert ci_diagnostics._retrieve(313) == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_missing_report_answers_wait_without_attempting_raw_log_fallback(
    monkeypatch, capsys
) -> None:
    monkeypatch.setattr(ci_diagnostics, "_repo_slug", lambda: "owner/repo")
    monkeypatch.setattr(
        ci_diagnostics,
        "_load_current_pr",
        lambda slug, pr: {"number": pr, "state": "open", "head": {"sha": "a" * 40}},
    )
    monkeypatch.setattr(ci_diagnostics, "_report_runs", lambda slug, sha, pr: (None, {}))

    def forbidden_raw_log(*args, **kwargs):
        raise AssertionError("report retrieval attempted raw Actions log access")

    monkeypatch.setattr(ci_diagnostics, "_job_log", forbidden_raw_log)
    assert ci_diagnostics._retrieve(313) == ci_diagnostics.WAIT_EXIT
    captured = capsys.readouterr()
    assert captured.out == "wait\n"
    assert captured.err == ""


def test_collector_workflow_covers_every_workflow_and_nonblocking_permissions() -> None:
    workflow = yaml.safe_load((ROOT / ".github/workflows/ci-diagnostics.yml").read_text())
    triggers = workflow.get("on") or workflow.get(True)
    assert triggers["workflow_run"]["types"] == ["completed"]
    assert triggers["workflow_run"]["workflows"] == ["*"]
    assert workflow["permissions"]["actions"] == "read"
    assert workflow["permissions"]["checks"] == "write"
    assert workflow["concurrency"]["cancel-in-progress"] is False


def test_local_patch_applier_refuses_a_mismatched_checkout_head(monkeypatch) -> None:
    from scripts import apply_ci_patch
    from scripts.apply_ci_patch import PatchError

    # An ordinary, existing, unprotected file: only the HEAD check may refuse it.
    diff = (
        "diff --git a/README.md b/README.md\n"
        "index 1111111..2222222 100644\n"
        "--- a/README.md\n"
        "+++ b/README.md\n"
        "@@ -1,1 +1,1 @@\n"
        "-old_value = 1\n"
        "+new_value = 1\n"
    )
    monkeypatch.setattr(apply_ci_patch, "_current_head", lambda: "a" * 40)
    try:
        apply_ci_patch.apply_patch(457, "b" * 40, diff)
    except PatchError as exc:
        assert "does not match diagnostic PR head" in str(exc)
    else:
        raise AssertionError("a patch based on a different PR head was accepted")


def test_local_patch_applier_validates_existing_paths_and_rejects_unsafe_paths() -> None:
    from scripts.apply_ci_patch import PatchError, _validate_patch

    diff = (
        "diff --git a/src/example.py b/src/example.py\n"
        "index 1111111..2222222 100644\n"
        "--- a/src/example.py\n"
        "+++ b/src/example.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-old_value = 1\n"
        "+new_value = 1\n"
    )
    assert _validate_patch(diff.replace("src/example.py", "README.md")) == ["README.md"]

    # Path validation requires an existing target, so exercise the guards that
    # do not require a repository file independently.
    unsafe = diff.replace("src/example.py", "../outside.py")
    try:
        _validate_patch(unsafe)
    except PatchError as exc:
        assert "not repository-relative" in str(exc)
    else:
        raise AssertionError("path traversal patch was accepted")

    try:
        _validate_patch(diff.replace("src/example.py", ".git/config"))
    except PatchError as exc:
        assert "Git metadata" in str(exc)
    else:
        raise AssertionError("a Git-metadata patch was accepted")

    try:
        _validate_patch(
            diff.replace("src/example.py", "src/new_file.py").replace(
                "@@ -1,1 +1,1 @@", "@@ -1,1 +1,1 @@"
            )
        )
    except PatchError as exc:
        assert "existing regular file" in str(exc)
    else:
        raise AssertionError("a patch targeting a nonexistent path was accepted")


def _single_record_report(sha: str = "a" * 40) -> tuple[dict, dict]:
    record = {
        "repository": "owner/repo",
        "pr": 9,
        "head_sha": sha,
        "workflow_name": "CI",
        "workflow_run_id": 10,
        "job_id": 11,
        "job_name": "unit",
        "line_number": 1,
        "message": "##[error]Process completed with exit code 1.",
    }
    digest = hashlib.sha256(_canonical_json([record]).encode()).hexdigest()
    page = {
        "status": "completed",
        "conclusion": "success",
        "head_sha": sha,
        "output": {
            "summary": _canonical_json(
                {"schema_version": 2, "generation_id": digest[:24], "page": 1, "page_count": 1}
            ),
            "text": _canonical_json(_pack_pages([record])[0]),
        },
    }
    manifest = {
        "page_count": 1,
        "generation_id": digest[:24],
        "diagnostic_count": 1,
        "digest": digest,
    }
    return manifest, page


def test_report_reader_accepts_an_intact_report() -> None:
    manifest, page = _single_record_report()
    assert len(_decode_report_pages(9, "a" * 40, manifest, {1: page})) == 1


def test_report_reader_rejects_digest_mismatch() -> None:
    manifest, page = _single_record_report()
    manifest["digest"] = "0" * 64
    try:
        _decode_report_pages(9, "a" * 40, manifest, {1: page})
    except DiagnosticError as exc:
        assert "digest" in str(exc)
    else:
        raise AssertionError("a report with a mismatched digest was accepted")


def test_report_reader_rejects_incomplete_report() -> None:
    manifest, _page = _single_record_report()
    try:
        _decode_report_pages(9, "a" * 40, manifest, {})
    except DiagnosticError as exc:
        assert "incomplete" in str(exc)
    else:
        raise AssertionError("a report with a missing page was accepted")


def test_report_for_a_previous_head_sha_is_rejected(monkeypatch, capsys) -> None:
    old, new = "a" * 40, "b" * 40
    digest = hashlib.sha256(_canonical_json([]).encode()).hexdigest()
    manifest = {
        "schema_version": 2,
        "status": "finalized",
        "pr": 313,
        "head_sha": old,
        "generation_id": digest[:24],
        "diagnostic_count": 0,
        "page_count": 0,
        "digest": digest,
    }
    master = {
        "status": "completed",
        "conclusion": "success",
        "head_sha": new,
        "output": {"summary": _canonical_json(manifest)},
    }
    monkeypatch.setattr(ci_diagnostics, "_repo_slug", lambda: "owner/repo")
    monkeypatch.setattr(
        ci_diagnostics,
        "_load_current_pr",
        lambda slug, pr: {"number": pr, "state": "open", "head": {"sha": new}},
    )
    monkeypatch.setattr(ci_diagnostics, "_report_runs", lambda slug, head, pr: (master, {}))
    assert ci_diagnostics._retrieve(313) != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "stale" in captured.err
