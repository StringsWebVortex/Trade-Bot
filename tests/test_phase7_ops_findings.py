"""
Audit findings OPS-011 and OPS-012: CI installs and scans what it claims to.

OPS-011: ci.yml and the Dockerfile pre-install torch from the CPU index with a
floor of 2.3 while requirements.txt requires 2.14. The pre-pass exists so that
requirements.txt finds torch already satisfied; a pre-pass that may resolve an
older wheel than requirements.txt accepts lets pip fetch torch again from PyPI,
which is the CUDA-bundling wheel GOV-015/REG-0012 keep out.

OPS-012: npm audit passes with a warning when the registry cannot be reached.
That is deliberate on pull requests, but on the weekly schedule and a manual
dispatch no pull request is blocked, so there the outage must fail the run;
otherwise the scan can be green for weeks without having run once.

Decides:
  - REG-1600 — The CPU torch pre-pass uses the same version spec as requirements.txt
  - REG-1601 — A scheduled npm audit that could not reach the registry fails
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
_CPU_PREPASS = re.compile(r'download\.pytorch\.org/whl/cpu\s+"(torch[^"]*)"')


def _requirements_torch_spec() -> str:
    for line in (PROJECT_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        stripped = line.split("#", 1)[0].strip()
        if re.match(r"torch(?![\w-])", stripped):
            return stripped.replace(" ", "")
    raise AssertionError("requirements.txt does not name torch")


@pytest.mark.parametrize("path", [".github/workflows/ci.yml", "Dockerfile"])
def test_cpu_torch_prepass_matches_requirements_spec(path: str) -> None:
    """REG-1600: every CPU-index pre-pass carries requirements.txt's torch spec."""
    text = (PROJECT_ROOT / path).read_text(encoding="utf-8")
    specs = [s.replace(" ", "") for s in _CPU_PREPASS.findall(text)]
    assert specs, f"{path} has no CPU torch pre-pass"
    assert set(specs) == {_requirements_torch_spec()}, (path, specs)


@pytest.fixture(scope="module")
def npm_audit_script() -> str:
    spec = yaml.safe_load(
        (PROJECT_ROOT / ".github/workflows/security.yml").read_text(encoding="utf-8")
    )
    steps = spec["jobs"]["npm-audit"]["steps"]
    (audit,) = [s for s in steps if s.get("name") == "Audit"]
    return audit["run"]


def test_scheduled_registry_outage_fails_the_run(npm_audit_script: str) -> None:
    """REG-1601: after the retry loop, schedule/dispatch exits 1 before the warning."""
    after_loop = npm_audit_script.rsplit("done", 1)[1]
    guard = re.search(
        r'if \[ "\$GITHUB_EVENT_NAME" = "schedule" \] \|\| '
        r'\[ "\$GITHUB_EVENT_NAME" = "workflow_dispatch" \]; then(?P<body>.*?)\n\s*fi',
        after_loop,
        re.S,
    )
    assert guard, "no schedule/dispatch guard after the retry loop"
    assert "::error::" in guard.group("body")
    assert re.search(r"^\s*exit 1\s*$", guard.group("body"), re.M)
    warning = after_loop.find("::warning::npm audit could not reach the registry")
    assert warning > guard.end(), "the warning must come after the failing guard"
