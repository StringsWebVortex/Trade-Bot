"""The local patch applier cannot mutate its own trust boundary.

Decides:
  - REG-0024 — Agent diagnostic retrieval is one canonical command; local checks stay disabled
  - SEC-1022 — The CI patch validator refuses sections without a validated git header
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "apply_ci_patch.py"


def _load_patcher():
    spec = importlib.util.spec_from_file_location("apply_ci_patch_contract", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_control_plane_and_diagnostic_contract_paths_are_protected() -> None:
    patcher = _load_patcher()
    for path in (
        ".github/workflows/ci-diagnostics.yml",
        ".github/CODEOWNERS",
        ".claude/hooks/pre_tool_use.py",
        "common/command_schema.py",
        "config/command_policy.json",
        "scripts/ci_diagnostics.py",
        "scripts/prfail",
        "scripts/apply_ci_patch.py",
        "tests/test_ci_diagnostics.py",
        "src/agent_control/reliability.py",
    ):
        assert patcher.is_protected_patch_path(path)


def test_unified_diff_cannot_touch_a_protected_workflow() -> None:
    patcher = _load_patcher()
    patch = "\n".join(
        [
            "diff --git a/.github/workflows/ci-diagnostics.yml b/.github/workflows/ci-diagnostics.yml",
            "--- a/.github/workflows/ci-diagnostics.yml",
            "+++ b/.github/workflows/ci-diagnostics.yml",
            "@@ -1,1 +1,1 @@",
            "-before",
            "+after",
            "",
        ]
    )
    with pytest.raises(patcher.PatchError, match="protected control-plane path"):
        patcher._validate_patch(patch)


def test_ordinary_application_source_is_not_protected_by_path_policy() -> None:
    patcher = _load_patcher()
    assert not patcher.is_protected_patch_path("src/strategies/trend.py")
    assert not patcher.is_protected_patch_path("tests/test_strategy_trend.py")


def test_headerless_section_before_a_git_section_is_refused() -> None:
    """SCR-001: a plain ---/+++ section must not slip past path validation."""
    patcher = _load_patcher()
    patch = "\n".join(
        [
            "--- a/CLAUDE.md",
            "+++ b/CLAUDE.md",
            "@@ -1,1 +1,1 @@",
            "-a",
            "+pwned",
            "diff --git a/Makefile b/Makefile",
            "--- a/Makefile",
            "+++ b/Makefile",
            "@@ -1,1 +1,1 @@",
            "-x",
            "+y",
            "",
        ]
    )
    with pytest.raises(patcher.PatchError):
        patcher._validate_patch(patch)


def test_headerless_section_after_a_git_section_is_refused() -> None:
    patcher = _load_patcher()
    patch = "\n".join(
        [
            "diff --git a/Makefile b/Makefile",
            "--- a/Makefile",
            "+++ b/Makefile",
            "@@ -1,1 +1,1 @@",
            "-x",
            "+y",
            "--- a/CLAUDE.md",
            "+++ b/CLAUDE.md",
            "@@ -1,1 +1,1 @@",
            "-a",
            "+pwned",
            "",
        ]
    )
    with pytest.raises(patcher.PatchError, match="unvalidated"):
        patcher._validate_patch(patch)
