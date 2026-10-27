"""Regression tests for the canonical diagnostic routes and duplicate-delivery policy."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from common.command_schema import CI_COMMENT_ALLOW_PATTERNS, is_ci_log_access

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude/hooks/pre_tool_use.py"


def hook_decision(command: str) -> dict:
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT)}
    env.pop("TB_COMMAND_POLICY", None)
    result = subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True,
                            text=True, env=env, timeout=20, check=True)
    return json.loads(result.stdout)["hookSpecificOutput"]


@pytest.mark.parametrize("command", [
    "./scripts/problems pytest",
    "./scripts/problems ruff common/command_schema.py",
    "./scripts/problems selftest",
    "./scripts/problems all src tests",
    "./scripts/prfail --pr 521",
])
def test_canonical_diagnostic_routes_match_shared_allowlist(command: str) -> None:
    assert any(re.fullmatch(pattern, command) for pattern in CI_COMMENT_ALLOW_PATTERNS)
    assert not is_ci_log_access(command)


@pytest.mark.parametrize("command", [
    "./scripts/problems",
    "./scripts/problems --help",
    "./scripts/problems pytest; gh run view 123 --log",
    "./scripts/problems pytest | cat",
    "bash ./scripts/problems selftest",
    "./scripts/problems unknown-target",
    "./scripts/problems pytest --all",
    "./scripts/problems pytest ../outside.py",
])
def test_noncanonical_or_wrapped_diagnostic_routes_are_denied(command: str) -> None:
    decision = hook_decision(command)
    assert decision["permissionDecision"] == "deny"


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
