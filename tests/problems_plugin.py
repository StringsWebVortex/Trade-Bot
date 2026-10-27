"""GOV-070 — pytest prints only problem lines, `path:line: pytest <test> - <message>`.

tests/conftest.py imports these hooks, so every pytest run of this suite (a
terminal, a cloud shell, CI, ./scripts/problems) prints the same thing: one
line per failing test, collection error, or failed gate, and `no problems`
when there is none. Progress, tracebacks, captured output, warnings and the
coverage table are written nowhere; there is no option that shows them.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import pytest
from _pytest._io import TerminalWriter

from scripts import problems

_STATE: dict[str, Any] = {"count": 0, "out": None, "null": None, "root": Path.cwd()}


def _write(text: str) -> None:
    out = _STATE["out"] or sys.__stdout__
    prefix = problems.CI_PREFIX if os.environ.get("GITHUB_ACTIONS") == "true" else ""
    out.write(prefix + text + "\n")
    out.flush()
    _STATE["count"] += 1


def _where(report: Any, root: Path) -> tuple[str, int | None, str]:
    crash = getattr(getattr(report, "longrepr", None), "reprcrash", None)
    if crash is not None and getattr(crash, "path", None):
        return problems.relative(str(crash.path), root), crash.lineno, crash.message
    location = getattr(report, "location", None)
    text = str(getattr(report, "longrepr", "") or "failed")
    if location:
        row = location[1] + 1 if isinstance(location[1], int) else None
        return location[0], row, text
    return problems.relative(str(getattr(report, "fspath", "") or "pytest"), root), None, text


def problem_for(report: Any, root: Path) -> str | None:
    """The problem line for a failed test or collection report, else None."""
    if not report.failed:
        return None
    path, row, message = _where(report, root)
    when = getattr(report, "when", None)
    if when is None:  # a collect report
        label = f"collection error in {report.nodeid or path}"
    elif when == "call":
        label = report.nodeid
    else:
        label = f"{report.nodeid} ({when})"
    return problems.line(path, row, None, "pytest", f"{label} - {message}")


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config) -> None:
    if hasattr(config, "workerinput"):  # an xdist worker reports to the controller
        return
    _STATE["out"] = sys.__stdout__
    _STATE["root"] = config.rootpath
    reporter = config.pluginmanager.get_plugin("terminalreporter")
    if reporter is not None:
        # Everything the terminal reporter (and pytest-cov, xdist, warnings)
        # would print goes to the null device.
        # The handle lives as long as the session, so it is kept, not closed.
        _STATE["null"] = open(os.devnull, "w", encoding="utf-8")  # noqa: SIM115
        reporter._tw = TerminalWriter(_STATE["null"])


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    text = problem_for(report, _root(report))
    if text:
        _write(text)


def pytest_collectreport(report: pytest.CollectReport) -> None:
    text = problem_for(report, _root(report))
    if text:
        _write(text)


def pytest_internalerror(excrepr: Any) -> None:
    crash = getattr(excrepr, "reprcrash", None)
    message = crash.message if crash else str(excrepr)
    _write(problems.line("pytest", None, None, "pytest", f"internal error - {message}"))


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if hasattr(session.config, "workerinput"):
        return
    cov = session.config.pluginmanager.get_plugin("_cov")
    total = getattr(cov, "cov_total", None)
    floor = getattr(getattr(cov, "options", None), "cov_fail_under", None)
    if isinstance(total, int | float) and floor and total < floor:
        message = f"total coverage {total:.2f}% is below {floor}%"
        _write(problems.line("pytest", None, None, "pytest-cov", message))
    if _STATE["count"] == 0 and int(exitstatus) not in (0, 5):
        message = f"exit status {int(exitstatus)} without a failed test"
        _write(problems.line("pytest", None, None, "pytest", message))
    if _STATE["count"] == 0:
        (_STATE["out"] or sys.__stdout__).write(problems.NO_PROBLEMS + "\n")


def _root(report: Any) -> Path:
    return _STATE["root"]
