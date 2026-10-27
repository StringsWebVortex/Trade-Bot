#!/usr/bin/env python3
"""GOV-070 — run a check and print only its problems, as `path:line:col: tool message`.

./scripts/problems <target> [paths...] runs one of the repository's checks with
its own output captured, and prints nothing but problem lines, the way an
editor's Problems panel lists them:

    src/app.py:12:5: ruff B007 Loop control variable `cmd` not used
    tests/test_x.py:88: pytest tests/test_x.py::test_y - assert 1 == 2
    frontend/src/App.jsx:41:7: vitest App renders - expected 5 to be 4

A part the tool does not report (a column, a line) is left out, never made up.
When there is no problem it prints `no problems`. Logs, tracebacks, progress
and summaries are never printed; there is no switch that shows them.

Targets:
  pytest    the Python suite; with paths, only those tests and without coverage
  ruff      ruff check
  format    ruff format --check, one line per hunk that would change
  vitest    the frontend unit tests (npm test)
  browser   the frontend browser tests (npm run test:browser)
  frontend  vitest, then browser
  build     the frontend build (npm run build)
  all       every target above
  selftest  run each target on tests/fixtures/problems and compare (CI)

Exit status: 0 no problems, 1 problems, 2 the check could not run. Under
GitHub Actions each line is prefixed with `::error::`, which annotates it and
lets ./scripts/prfail return the same line.

The pytest plugin (tests/problems_plugin.py, loaded by tests/conftest.py)
makes pytest print in this format itself, so a direct `pytest` run shows the
same lines and nothing else.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
FIXTURES = ROOT / "tests" / "fixtures" / "problems"
CI_PREFIX = "::error::"
NO_PROBLEMS = "no problems"
TIMEOUT = 45 * 60

Run = Callable[[Sequence[str], Path], tuple[int, str]]
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


class CheckError(Exception):
    """The check could not run, so it has no problems to report."""


def line(path: str, row: int | None, col: int | None, tool: str, message: str) -> str:
    """One problem line; a part the tool did not report is left out."""
    where = path
    if row:
        where += f":{row}"
        if col:
            where += f":{col}"
    first = message.strip().splitlines()[0].strip() if message.strip() else ""
    return f"{where}: {tool} {first}".rstrip()


def relative(path: str, root: Path = ROOT) -> str:
    try:
        return Path(path).resolve().relative_to(root).as_posix()
    except (ValueError, OSError):
        return path


# --- ruff ------------------------------------------------------------------


def ruff_problems(raw: str) -> list[str]:
    """ruff check --output-format=json."""
    found = []
    for item in json.loads(raw or "[]"):
        location = item.get("location") or {}
        code = item.get("code") or "syntax"
        found.append(
            line(
                relative(item["filename"]),
                location.get("row"),
                location.get("column"),
                "ruff",
                f"{code} {item.get('message', '')}",
            )
        )
    return found


HUNK = re.compile(r"^@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@")


def format_problems(raw: str) -> list[str]:
    """ruff format --check --diff: one line per hunk, at its first changed line."""
    found = []
    path = ""
    row: int | None = None  # original line of the current hunk, until its first change
    for text in raw.splitlines():
        if text.startswith("--- "):
            path, row = relative(text[4:].strip()), None
        elif match := HUNK.match(text):
            row = int(match.group(1))
        elif row is not None and text.startswith((" ", "-", "+")):
            if text.startswith(" "):
                row += 1
                continue
            found.append(line(path, row, None, "ruff-format", "would reformat"))
            row = None
    return found


# --- frontend --------------------------------------------------------------


BUILD_LOCATION = re.compile(
    r"((?:/|\.{0,2}/)?[\w@./-]+\.(?:jsx?|tsx?|mjs|cjs|css|html)):(\d+):(\d+)"
)


def build_problems(raw: str, status: int) -> list[str]:
    """vite build: the first error and the file:line:col it names."""
    if status == 0:
        return []
    lines = [t.strip() for t in raw.splitlines() if t.strip()]
    # vite opens with headings ("error during build:", "Build failed with 1
    # error:"); the error itself is the first such line that is not one.
    message = next(
        (t for t in lines if "error" in t.lower() and not t.endswith(":")),
        lines[-1] if lines else "failed",
    )
    for text in lines:
        if match := BUILD_LOCATION.search(text):
            named = Path(match.group(1))
            path = relative(str(named if named.is_absolute() else FRONTEND / named))
            return [line(path, int(match.group(2)), int(match.group(3)), "build", message)]
    return [line("frontend", None, None, "build", message)]


# --- runners ---------------------------------------------------------------


def _run(command: Sequence[str], cwd: Path) -> tuple[int, str]:
    try:
        done = subprocess.run(
            list(command),
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            timeout=TIMEOUT,
            env=_environment(),
        )
    except FileNotFoundError as exc:
        raise CheckError(f"{command[0]} is not installed") from exc
    except subprocess.TimeoutExpired as exc:
        raise CheckError(f"{command[0]} did not finish within {TIMEOUT // 60} min") from exc
    return done.returncode, ANSI.sub("", done.stdout + done.stderr)


# Variables that would add options to a check behind the command line's back.
OPTION_VARIABLES = ("PYTEST_ADDOPTS", "PYTEST_PLUGINS", "NODE_OPTIONS", "RUFF_OUTPUT_FORMAT")


def _environment() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in OPTION_VARIABLES}
    return {**env, "NO_COLOR": "1", "FORCE_COLOR": "0"}


def check_ruff(paths: Sequence[str], run: Run = _run) -> list[str]:
    status, out = run(
        [sys.executable, "-m", "ruff", "check", "--output-format=json", *(paths or ["."])], ROOT
    )
    if status not in (0, 1):
        raise CheckError(_first(out, "ruff check failed to run"))
    return ruff_problems(_json_part(out, "["))


def check_format(paths: Sequence[str], run: Run = _run) -> list[str]:
    status, out = run(
        [sys.executable, "-m", "ruff", "format", "--check", "--diff", *(paths or ["."])], ROOT
    )
    if status not in (0, 1):
        raise CheckError(_first(out, "ruff format failed to run"))
    return format_problems(out)


def check_pytest(paths: Sequence[str], run: Run = _run) -> list[str]:
    # With paths it is a focused run, which the 99% suite-wide floor would fail.
    extra = ["--no-cov", *paths] if paths else []
    status, out = run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", *extra], ROOT)
    found = [t.removeprefix(CI_PREFIX) for t in out.splitlines() if _is_problem(t)]
    if status not in (0, 1) and not found:
        # 5 is "no tests collected"; anything else without a problem line is a
        # failure outside any test, which is still a problem to report.
        found = [line("pytest", None, None, "pytest", f"exit status {status} - {_first(out, '')}")]
    return found


def _npm(script: str, paths: Sequence[str], tool: str, run: Run) -> list[str]:
    # frontend/problems-reporter.js, set in every vitest config, prints the
    # problem lines itself; anything else vitest writes is dropped here.
    command = ["npm", "run", "--silent", script, *(["--", *paths] if paths else [])]
    status, out = run(command, FRONTEND)
    found = [t.removeprefix(CI_PREFIX) for t in out.splitlines() if _is_problem(t)]
    if status != 0 and not found:
        found = [line("frontend", None, None, tool, f"exit status {status} - {_first(out, '')}")]
    return found


def check_vitest(paths: Sequence[str], run: Run = _run) -> list[str]:
    return _npm("test", paths, "vitest", run)


def check_browser(paths: Sequence[str], run: Run = _run) -> list[str]:
    return _npm("test:browser", paths, "vitest-browser", run)


def check_build(paths: Sequence[str], run: Run = _run) -> list[str]:
    status, out = run(["npm", "run", "--silent", "build", "--", *paths], FRONTEND)
    return build_problems(out, status)


CHECKS: dict[str, Callable[..., list[str]]] = {
    "pytest": check_pytest,
    "ruff": check_ruff,
    "format": check_format,
    "vitest": check_vitest,
    "browser": check_browser,
    "build": check_build,
}
GROUPS = {"frontend": ["vitest", "browser"], "all": list(CHECKS)}


def _is_problem(text: str) -> bool:
    return bool(PROBLEM.match(text.removeprefix(CI_PREFIX)))


# path[:line[:col]]: tool message -- what line() writes and the pytest plugin prints.
PROBLEM = re.compile(r"^[^\s:]+(?::\d+){0,2}: [\w.-]+ \S")


def _first(out: str, default: str) -> str:
    return next((t.strip() for t in out.splitlines() if t.strip()), default)


def _json_part(out: str, opener: str) -> str:
    start = out.find(opener)
    return out[start:] if start >= 0 else ""


# --- self-test -------------------------------------------------------------


def selftest(targets: Sequence[str], run: Run = _run) -> list[str]:
    """Run each target on its fixture and return a problem for every mismatch."""
    expected = json.loads((FIXTURES / "expected.json").read_text(encoding="utf-8"))
    mismatches = []
    for target in targets or [name for name in expected if not name.startswith("_")]:
        want = expected[target]["lines"]
        got = CHECKS[target](expected[target]["paths"], run)
        if got != want:
            mismatches.append(
                line(
                    "tests/fixtures/problems/expected.json",
                    None,
                    None,
                    "selftest",
                    f"{target} printed {got!r}, expected {want!r}",
                )
            )
    return mismatches


# --- entry -----------------------------------------------------------------


def emit(lines: Iterable[str], write: Callable[[str], object], ci: bool) -> None:
    for text in lines:
        write((CI_PREFIX + text if ci else text) + "\n")


def main(argv: Sequence[str], env: dict[str, str] | None = None, run: Run = _run) -> int:
    env = dict(os.environ if env is None else env)
    ci = env.get("GITHUB_ACTIONS") == "true"
    write = sys.stdout.write
    targets = [*CHECKS, *GROUPS, "selftest"]
    if not argv or argv[0] not in targets:
        write(f"problems: error: target must be one of {', '.join(targets)}\n")
        return 2
    target, paths = argv[0], list(argv[1:])
    options = [p for p in paths if p.startswith("-")]
    if options:
        # Paths and test ids only: an option could change what the check prints.
        write(f"problems: error: options are not accepted: {' '.join(options)}\n")
        return 2
    try:
        if target == "selftest":
            found = selftest(paths, run)
        else:
            found = []
            for name in GROUPS.get(target, [target]):
                found += CHECKS[name](paths, run)
    except (CheckError, OSError, ValueError, KeyError) as exc:
        write(f"problems: error: {exc}\n")
        return 2
    if not found:
        write(NO_PROBLEMS + "\n")
        return 0
    emit(found, write, ci)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
