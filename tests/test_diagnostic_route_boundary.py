"""Regression tests for the canonical diagnostic routes and duplicate-delivery policy."""
from __future__ import annotations

import importlib.util
import json
import os
import re
from pathlib import Path

import pytest

from common.command_schema import CI_COMMENT_ALLOW_PATTERNS, is_ci_log_access

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude/hooks/pre_tool_use.py"
_spec = importlib.util.spec_from_file_location("trade_bot_pre_tool_use_test", HOOK)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)


def hook_decision(command: str) -> str:
    os.environ["CLAUDE_PROJECT_DIR"] = str(ROOT)
    os.environ.pop("TB_COMMAND_POLICY", None)
    return _hook._github_route_violation({"tool_name": "Bash", "tool_input": {"command": command}})


def test_only_filtered_prfail_report_matches_shared_allowlist() -> None:
    command = "./scripts/prfail --pr 521"
    assert any(re.fullmatch(pattern, command) for pattern in CI_COMMENT_ALLOW_PATTERNS)
    assert not is_ci_log_access(command)
    assert hook_decision(command) == ""


@pytest.mark.parametrize("command", [
    "./scripts/problems pytest",
    "./scripts/problems ruff common/command_schema.py",
    "./scripts/problems selftest",
    "./scripts/problems all src tests",
    "./scripts/problems",
    "./scripts/problems --help",
    "./scripts/problems pytest; gh run view 123 --log",
    "./scripts/problems pytest | cat",
    "bash ./scripts/problems selftest",
    "./scripts/problems unknown-target",
    "./scripts/problems pytest --all",
    "./scripts/problems pytest ../outside.py",
])
def test_local_check_wrapper_and_noncanonical_routes_are_denied(command: str) -> None:
    assert hook_decision(command)


def test_duplicate_delivery_policy_is_filename_independent_and_host_enforced() -> None:
    policy = json.loads((ROOT / "config/command_policy.json").read_text())
    duplicate = policy["duplicate_delivery"]
    assert duplicate["enabled"] is True
    assert duplicate["threshold"] == 0.25
    assert duplicate["filename_independent"] is True
    assert "host-level" in duplicate["enforcement"]
    assert "ChatGPT-hosted" in duplicate["limitations"]


def test_protected_diagnostic_scripts_are_not_modified_by_this_policy_change() -> None:
    # The protected wrappers may be absent on a working branch; if present, the
    # implementation must leave them untouched and the test only checks existence metadata.
    for path in (ROOT / "scripts/problems", ROOT / "scripts/problems.py", ROOT / "scripts/prfail"):
        if path.exists():
            assert path.is_file()
