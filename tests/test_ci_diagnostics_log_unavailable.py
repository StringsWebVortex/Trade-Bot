"""REG-1609: one unavailable job log no longer fails the whole diagnostics report.

The signed URL GitHub redirects a job-log request to can briefly fail just
after the job completes. The collector made one attempt and raised, so the
whole report was published as "collection failed" and ./scripts/prfail had
nothing to show for any job (PR #512, "Redirected job log download failed").

* the signed download is retried, and its final error names the cause;
* a green job whose log cannot be fetched adds nothing, since its log could
  only add warnings;
* a failed job whose log cannot be fetched gets a ``log_unavailable`` record,
  so the report says its failure lines are missing instead of looking whole.

Decides: REG-1609"""

from __future__ import annotations

import io
import urllib.error

import pytest

from scripts import ci_diagnostics
from scripts.ci_diagnostics import JobLogUnavailable

RUN = {"id": 7, "run_attempt": 1, "conclusion": "failure"}


class _Body(io.BytesIO):
    def __enter__(self) -> _Body:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


@pytest.fixture
def waits(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    recorded: list[float] = []
    monkeypatch.setattr(ci_diagnostics.time, "sleep", recorded.append)
    return recorded


def _http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("https://logs.example/x", code, "fail", {}, None)


def test_a_transient_signed_download_failure_is_retried(monkeypatch, waits) -> None:
    outcomes = [_http_error(404), urllib.error.URLError("reset"), b"log body"]

    def urlopen(request, timeout):
        assert "Authorization" not in request.headers
        outcome = outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return _Body(outcome)

    monkeypatch.setattr(ci_diagnostics.urllib.request, "urlopen", urlopen)
    assert ci_diagnostics._download_signed_log("https://logs.example/x", 9) == b"log body"
    assert waits == [1, 2]


def test_a_persistent_failure_names_its_cause(monkeypatch, waits) -> None:
    def urlopen(request, timeout):
        raise _http_error(404)

    monkeypatch.setattr(ci_diagnostics.urllib.request, "urlopen", urlopen)
    with pytest.raises(JobLogUnavailable, match=r"job 9 \(HTTP 404\)"):
        ci_diagnostics._download_signed_log("https://logs.example/x", 9)
    assert len(waits) == ci_diagnostics.LOG_DOWNLOAD_ATTEMPTS - 1


def _job(conclusion: str) -> dict:
    return {
        "id": 11,
        "name": "Python (lint + governance docs)",
        "status": "completed",
        "conclusion": conclusion,
        "steps": [{"name": "Lint", "status": "completed", "conclusion": conclusion}],
    }


@pytest.fixture
def no_log(monkeypatch: pytest.MonkeyPatch) -> None:
    def unavailable(repository: str, job_id: int) -> str:
        raise JobLogUnavailable(f"Redirected job log download failed for job {job_id} (HTTP 404)")

    monkeypatch.setattr(ci_diagnostics, "_job_log", unavailable)


@pytest.mark.usefixtures("no_log")
@pytest.mark.parametrize("conclusion", ["success", "skipped"])
def test_a_green_job_without_its_log_adds_nothing(conclusion: str) -> None:
    records: dict = {}
    ci_diagnostics._add_log_diagnostics(records, "o/r", 512, "a" * 40, "CI", RUN, _job(conclusion))
    assert records == {}


@pytest.mark.usefixtures("no_log")
def test_a_failed_job_without_its_log_says_its_lines_are_missing() -> None:
    records: dict = {}
    ci_diagnostics._add_log_diagnostics(records, "o/r", 512, "a" * 40, "CI", RUN, _job("failure"))
    (record,) = records.values()
    assert record["category"] == "log_unavailable"
    assert record["conclusion"] == "failure"
    assert record["job_id"] == 11
    assert "HTTP 404" in record["message"] and "missing from the report" in record["message"]


def test_a_server_error_on_the_log_request_is_unavailable_not_fatal(monkeypatch) -> None:
    class _Opener:
        def open(self, request, timeout):
            raise _http_error(503)

    monkeypatch.setattr(ci_diagnostics, "_token", lambda: "t")
    monkeypatch.setattr(ci_diagnostics.urllib.request, "build_opener", lambda *a: _Opener())
    with pytest.raises(JobLogUnavailable, match="503"):
        ci_diagnostics._job_log("o/r", 9)
