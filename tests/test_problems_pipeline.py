"""
Every check reports a problem as one `path:line:col: tool message` line, the
same line wherever it runs, and nothing else reaches the agent.

The pipeline under test: a check (ruff, ruff format, pytest through
tests/problems_plugin.py, vitest through frontend/problems-reporter.js, vite
build) -> ./scripts/problems -> under GitHub Actions a `::error::` line in the
job log -> the CI diagnostics collector -> ./scripts/prfail, which must return
the line exactly as ./scripts/problems printed it. The hook admits only
`./scripts/problems <target> [paths]` and prfail for local runs.

`./scripts/problems selftest` runs the real tools on tests/fixtures/problems in
CI and compares against expected.json; this module decides the in-process
parts of the same chain.

Decides:
  - GOV-070 — Checks print only exact problem lines, everywhere, through two commands
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from scripts import ci_diagnostics, problems
from tests import problems_plugin

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "problems"


@pytest.fixture(scope="module")
def hook():
    spec = importlib.util.spec_from_file_location(
        "tb_pre_tool_use", ROOT / ".claude" / "hooks" / "pre_tool_use.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- each tool's output becomes exact problem lines -------------------------


def test_ruff_findings_carry_file_line_column_and_code() -> None:
    raw = json.dumps(
        [
            {
                "filename": str(ROOT / "src" / "x.py"),
                "location": {"row": 12, "column": 5},
                "code": "B007",
                "message": "Loop control variable `cmd` not used",
            }
        ]
    )
    assert problems.ruff_problems(raw) == [
        "src/x.py:12:5: ruff B007 Loop control variable `cmd` not used"
    ]


def test_a_format_problem_is_the_first_changed_line_of_each_hunk() -> None:
    raw = (
        "--- src/x.py\n+++ src/x.py\n"
        "@@ -10,7 +10,7 @@\n a\n b\n c\n-VALUE = {  'a':1 }\n+VALUE = {'a': 1}\n d\n"
        "@@ -40,3 +40,4 @@\n e\n+\n f\n"
    )
    assert problems.format_problems(raw) == [
        "src/x.py:13: ruff-format would reformat",
        "src/x.py:41: ruff-format would reformat",
    ]


def test_a_build_error_names_the_file_and_the_error_not_the_heading() -> None:
    raw = (
        "vite v8 building for production...\nBuild failed with 1 error:\n\n"
        "[PARSE_ERROR] Unexpected token\n"
        f"    at {ROOT}/frontend/src/App.jsx:41:7\n"
    )
    assert problems.build_problems(raw, 1) == [
        "frontend/src/App.jsx:41:7: build [PARSE_ERROR] Unexpected token"
    ]
    assert problems.build_problems(raw, 0) == []


def test_a_missing_part_is_left_out_never_made_up() -> None:
    assert problems.line("a.py", None, 3, "t", "m") == "a.py: t m"
    assert problems.line("a.py", 7, None, "t", "first\nsecond") == "a.py:7: t first"


# --- pytest prints the same lines itself ------------------------------------


def _report(**fields):
    base = {"failed": True, "when": "call", "nodeid": "tests/test_a.py::test_b", "location": None}
    return SimpleNamespace(**{**base, **fields})


def _crash(path: Path, lineno: int, message: str):
    crash = SimpleNamespace(path=str(path), lineno=lineno, message=message)
    return SimpleNamespace(reprcrash=crash)


@pytest.mark.parametrize(
    ("fields", "expected"),
    [
        (
            {"longrepr": _crash(ROOT / "tests" / "test_a.py", 9, "assert 1 == 2\n+ where")},
            "tests/test_a.py:9: pytest tests/test_a.py::test_b - assert 1 == 2",
        ),
        (
            {"when": "setup", "longrepr": _crash(ROOT / "src" / "y.py", 3, "KeyError: 'k'")},
            "src/y.py:3: pytest tests/test_a.py::test_b (setup) - KeyError: 'k'",
        ),
        (
            {"longrepr": "[XPASS(strict)] fixed", "location": ("tests/test_a.py", 4, "test_b")},
            "tests/test_a.py:5: pytest tests/test_a.py::test_b - [XPASS(strict)] fixed",
        ),
        (
            {
                "when": None,
                "nodeid": "tests/test_c.py",
                "longrepr": _crash(ROOT / "tests" / "test_c.py", 2, "ImportError: no x"),
            },
            "tests/test_c.py:2: pytest collection error in tests/test_c.py - ImportError: no x",
        ),
    ],
    ids=["assertion", "setup-error", "strict-xpass", "collection-error"],
)
def test_pytest_failures_become_problem_lines(fields, expected) -> None:
    assert problems_plugin.problem_for(_report(**fields), ROOT) == expected


def test_a_passing_report_prints_nothing() -> None:
    assert problems_plugin.problem_for(_report(failed=False), ROOT) is None


def test_the_suite_loads_the_plugin_hooks() -> None:
    import tests.conftest as conftest

    for hook_name in (
        "pytest_configure",
        "pytest_runtest_logreport",
        "pytest_collectreport",
        "pytest_sessionfinish",
        "pytest_internalerror",
    ):
        assert getattr(conftest, hook_name) is getattr(problems_plugin, hook_name)


@pytest.mark.parametrize(
    "config", ["vitest.config.js", "vitest.browser.config.js", "vitest.selftest.config.js"]
)
def test_every_vitest_config_prints_problem_lines_with_locations(config: str) -> None:
    text = (ROOT / "frontend" / config).read_text(encoding="utf-8")
    assert "reporters: ['./problems-reporter.js']" in text
    assert "includeTaskLocation: true" in text


# --- the command ------------------------------------------------------------


def _fake_run(outputs: dict[str, tuple[int, str]], seen: list | None = None):
    def run(command, cwd):
        if seen is not None:
            seen.append(list(command))
        key = next(name for name in outputs if name in " ".join(command))
        return outputs[key]

    return run


def test_no_problem_prints_no_problems(capsys) -> None:
    run = _fake_run({"ruff": (0, "[]")})
    assert problems.main(["ruff"], {}, run) == 0
    assert capsys.readouterr().out == "no problems\n"


def test_under_github_actions_each_line_is_an_error_annotation(capsys) -> None:
    finding = {"filename": "a.py", "location": {"row": 1, "column": 1}, "code": "F401"}
    raw = json.dumps([{**finding, "message": "m"}])
    assert problems.main(["ruff"], {"GITHUB_ACTIONS": "true"}, _fake_run({"ruff": (1, raw)})) == 1
    assert capsys.readouterr().out == "::error::a.py:1:1: ruff F401 m\n"


@pytest.mark.parametrize(
    "argv",
    [
        ["pytest", "--noconftest"],
        ["pytest", "tests", "-p", "no:x"],
        ["vitest", "--config", "x"],
        ["nope"],
        [],
    ],
    ids=["noconftest", "plugin-off", "config", "unknown-target", "empty"],
)
def test_options_and_unknown_targets_are_refused(argv, capsys) -> None:
    assert problems.main(argv, {}, _fake_run({"": (0, "")})) == 2
    assert capsys.readouterr().out.startswith("problems: error: ")


def test_pytest_output_keeps_only_problem_lines() -> None:
    out = (
        "::error::tests/test_a.py:9: pytest tests/test_a.py::test_b - assert 1 == 2\n"
        "error during close something: noise\n"
        "  1 failed in 0.1s\n"
    )
    seen: list = []
    found = problems.check_pytest(["tests/test_a.py"], _fake_run({"pytest": (1, out)}, seen))
    assert found == ["tests/test_a.py:9: pytest tests/test_a.py::test_b - assert 1 == 2"]
    assert "--no-cov" in seen[0]


def test_a_failure_outside_any_test_is_still_a_problem() -> None:
    found = problems.check_pytest([], _fake_run({"pytest": (3, "INTERNALERROR> boom\n")}))
    assert found == ["pytest: pytest exit status 3 - INTERNALERROR> boom"]


def test_variables_that_add_options_are_not_passed_on(monkeypatch) -> None:
    for name in problems.OPTION_VARIABLES:
        monkeypatch.setenv(name, "-s")
    env = problems._environment()
    assert not set(problems.OPTION_VARIABLES) & set(env)


def test_selftest_reports_each_mismatch(monkeypatch) -> None:
    expected = json.loads((FIXTURES / "expected.json").read_text(encoding="utf-8"))
    monkeypatch.setitem(problems.CHECKS, "ruff", lambda paths, run: expected["ruff"]["lines"])
    monkeypatch.setitem(problems.CHECKS, "format", lambda paths, run: [])
    assert problems.selftest(["ruff"]) == []
    (mismatch,) = problems.selftest(["format"])
    assert mismatch.startswith("tests/fixtures/problems/expected.json: selftest format printed []")


# --- CI log -> collector -> prfail returns the same line ---------------------


@pytest.mark.parametrize("marker", ["##[error]", "::error::"])
def test_prfail_returns_the_line_problems_printed(marker: str) -> None:
    printed = "frontend/src/App.jsx:41:7: vitest App renders - expected 5 to be 4"
    log = f"2026-10-27T01:00:00.0000000Z {marker}{printed}\n2026-10-27T01:00:00.1Z noise\n"
    ((_number, logged),) = ci_diagnostics.failure_lines(log)
    assert ci_diagnostics.problem_text(logged) == printed


def test_other_error_lines_are_returned_as_logged() -> None:
    line = "##[error]Process completed with exit code 1."
    assert ci_diagnostics.problem_text(line) == line


def test_a_failed_step_is_named_even_without_a_failure_line(monkeypatch) -> None:
    monkeypatch.setattr(ci_diagnostics, "_job_log", lambda repo, job_id: "all good\n")
    records: dict = {}
    job = {
        "id": 5,
        "name": "Python (lint + governance docs)",
        "conclusion": "failure",
        "steps": [
            {"name": "Lint", "conclusion": "success"},
            {"name": "Quality-engineering gates", "conclusion": "failure"},
        ],
    }
    ci_diagnostics._add_failure_lines(records, "o/r", 7, "a" * 40, {"id": 9, "name": "CI"}, job)
    assert [r["message"] for r in records.values()] == [
        "CI / Python (lint + governance docs) / Quality-engineering gates: failure"
    ]


def test_ci_lines_are_printed_when_review_threads_are_refused(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        ci_diagnostics,
        "read_report",
        lambda pr: ("a" * 40, [{"message": "##[error]a.py:1:1: ruff F401 m"}]),
    )
    monkeypatch.setattr(ci_diagnostics, "_repo_slug", lambda: "o/r")

    def refused(slug, pr):
        raise ci_diagnostics.DiagnosticError("GitHub API request failed (403) for /graphql")

    monkeypatch.setattr(ci_diagnostics, "_unresolved_threads", refused)
    assert ci_diagnostics._retrieve(7) == 2
    out, err = capsys.readouterr()
    assert out == "a.py:1:1: ruff F401 m\n"
    assert "review threads unavailable" in err and "403" in err


# --- CI runs every check through the command ---------------------------------


def test_ci_runs_every_check_and_the_selftest_through_problems() -> None:
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    workflow = yaml.safe_load(text)
    runs = {
        step.get("run", "").strip()
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
    }
    for command in (
        "./scripts/problems ruff",
        "./scripts/problems format",
        "./scripts/problems vitest",
        "./scripts/problems browser",
        "./scripts/problems build",
        "./scripts/problems selftest ruff format",
        "./scripts/problems selftest pytest",
        "./scripts/problems selftest vitest build",
    ):
        assert command in runs
    assert not runs & {"ruff check .", "ruff format --check .", "npm test", "npm run build"}


# --- the agent may run only these two commands -------------------------------


@pytest.mark.parametrize(
    ("command", "allowed"),
    [
        ("./scripts/problems pytest tests/test_x.py::test_y[a-b]", True),
        ("./scripts/problems all", True),
        ("./scripts/prfail --pr 12", True),
        ("./scripts/problems pytest --noconftest", False),
        ("./scripts/problems pytest -p no:cacheprovider", False),
        ("./scripts/problems ruff; cat log.txt", False),
        ("./scripts/problems ruff && npm test", False),
        ("PYTEST_ADDOPTS=-s ./scripts/problems pytest", False),
        ("python3 -m pytest -q", False),
        ("pytest tests", False),
        ("ruff check .", False),
        ("npm test", False),
        ("npx vitest run", False),
        ("python3 scripts/problems.py pytest", False),
        ("cat /tmp/pytest-of-root/log", False),
    ],
)
def test_the_hook_admits_only_the_two_commands(hook, command: str, allowed: bool) -> None:
    event = {"tool_name": "Bash", "tool_input": {"command": command}}
    denied = hook._github_route_violation(event) or hook._violations(event, hook._load_policy())
    assert (not denied) is allowed


def test_the_hook_and_the_policy_agree_on_the_command(hook) -> None:
    policy = json.loads((ROOT / "config" / "command_policy.json").read_text(encoding="utf-8"))
    pattern = policy["local_checks"]["problems_command"]
    assert pattern.strip("^$") == hook.PROBLEMS_COMMAND_RE.pattern
    assert re.fullmatch(pattern, "./scripts/problems pytest tests/a.py")


def test_the_command_and_its_plugins_cannot_be_edited_by_the_agent(hook) -> None:
    for path in (
        "scripts/problems",
        "scripts/problems.py",
        "tests/problems_plugin.py",
        "tests/test_problems_pipeline.py",
        "tests/fixtures/problems/expected.json",
        "frontend/problems-reporter.js",
    ):
        assert path in hook.PROTECTED_BOUNDARY_PATHS
