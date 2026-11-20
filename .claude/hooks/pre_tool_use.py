"""Pre-tool-use hook: GitHub route enforcement and write-budget gating."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_HOOKS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_HOOKS_DIR))
sys.path.insert(0, str(ROOT))

import _gh_contract as ghc  # noqa: E402

from common.command_schema import (  # noqa: E402
    CI_COMMENT_ALLOW_PATTERNS,
    CI_LOG_REFUSAL,
    LOCAL_CHECK_REFUSAL,
    is_ci_log_access,
    is_local_check_execution,
)

# ---------------------------------------------------------------------------
# CI routing helpers
# ---------------------------------------------------------------------------

_TAIL_LOG_RE = re.compile(r"\btail\s+-[a-zA-Z]*f\b")
_CI_TOOL_METHODS = frozenset({"get_status", "get_check_runs", "list_check_runs"})

# Tools that always return CI verdict regardless of method.
_ALWAYS_CI_TOOLS = frozenset({"get_workflow_run_logs", "list_workflow_run_artifacts"})


def _get_ci_verdict(hint: int | None = None) -> str:
    """Call ci_verdict and return the verdict string, or a fallback on error."""
    try:
        import ci_verdict  # type: ignore[import-not-found]

        if not ci_verdict.has_credentials():
            return ""
        return ci_verdict.verdict(hint=hint)
    except ci_verdict.VerdictError as exc:  # type: ignore[attr-defined]
        return f"ci verdict unavailable: {exc}"
    except Exception as exc:
        return f"ci verdict unavailable: {exc}"


def _is_bash_ci_route(command: str) -> bool:
    """Return True if the Bash command is a CI diagnostic route."""
    return bool(is_ci_log_access(command) or _TAIL_LOG_RE.search(command))


# ---------------------------------------------------------------------------
# _github_route_violation — called by test_diagnostic_route_boundary.py
# ---------------------------------------------------------------------------


def _github_route_violation(event: dict) -> str:
    """Return empty string if the tool call is allowed, non-empty refusal reason otherwise."""
    tool_name = event.get("tool_name", "")
    command = event.get("tool_input", {}).get("command", "")

    if tool_name != "Bash":
        return ""

    # Explicitly allowed: exact prfail report command.
    if any(re.fullmatch(p, command) for p in CI_COMMENT_ALLOW_PATTERNS):
        return ""

    # Deny CI log access routes.
    if _is_bash_ci_route(command):
        return CI_LOG_REFUSAL

    # Deny scripts/problems wrapper (local check frontend).
    if re.search(r"\bscripts/problems\b", command):
        return LOCAL_CHECK_REFUSAL

    # Deny all other local check executions.
    if is_local_check_execution(command):
        return LOCAL_CHECK_REFUSAL

    return ""


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------


def _route_bash(tool_input: dict) -> dict:
    command = tool_input.get("command", "")

    if any(re.fullmatch(p, command) for p in CI_COMMENT_ALLOW_PATTERNS):
        return {"permissionDecision": "allow"}

    if _is_bash_ci_route(command):
        verdict = _get_ci_verdict()
        if verdict:
            return {"permissionDecision": "deny", "permissionDecisionReason": verdict}
        return {"permissionDecision": "deny", "permissionDecisionReason": CI_LOG_REFUSAL}

    if re.search(r"\bscripts/problems\b", command):
        return {"permissionDecision": "deny", "permissionDecisionReason": LOCAL_CHECK_REFUSAL}

    if is_local_check_execution(command):
        return {"permissionDecision": "deny", "permissionDecisionReason": LOCAL_CHECK_REFUSAL}

    return {"permissionDecision": "allow"}


def _extract_pr_hint(tool_input: dict) -> int | None:
    """Extract PR number from tool_input fields."""
    if "pullNumber" in tool_input:
        return int(tool_input["pullNumber"])
    url = tool_input.get("url", "")
    if url:
        return ghc._pr_number_from_url(url)
    return None


def _route_ci_tool(base_tool: str, tool_input: dict) -> dict:
    """Route a known CI data tool through the verdict."""
    hint = _extract_pr_hint(tool_input)
    verdict = _get_ci_verdict(hint=hint)
    if verdict:
        return {"permissionDecision": "deny", "permissionDecisionReason": verdict}
    # No credentials or verdict unavailable: deny with method/tool name.
    method = tool_input.get("method", base_tool)
    return {
        "permissionDecision": "deny",
        "permissionDecisionReason": f"CI data access via '{method}' is blocked.",
    }


def _route_pull_request_read(tool_input: dict) -> dict:
    method = tool_input.get("method", "")
    if method in _CI_TOOL_METHODS:
        hint = _extract_pr_hint(tool_input)
        verdict = _get_ci_verdict(hint=hint)
        if verdict:
            return {"permissionDecision": "deny", "permissionDecisionReason": verdict}
        # No credentials.
        return {
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"CI check access via method='{method}' is blocked; no CI credentials."
            ),
        }
    return {"permissionDecision": "allow"}


def _route_get_file_contents(tool_input: dict) -> dict:
    # Check for CI URL in any field.
    for val in tool_input.values():
        if isinstance(val, str) and ghc._is_ci_url(val):
            hint = ghc._pr_number_from_url(val)
            verdict = _get_ci_verdict(hint=hint)
            if verdict:
                return {"permissionDecision": "deny", "permissionDecisionReason": verdict}
            return {
                "permissionDecision": "deny",
                "permissionDecisionReason": "CI URL detected in read request.",
            }

    tb_keys = {k for k in tool_input if k.startswith("tb_")}
    if len(tb_keys) > 1:
        return {
            "permissionDecision": "deny",
            "permissionDecisionReason": "read must name its target exactly once",
        }
    if not tb_keys:
        return {
            "permissionDecision": "deny",
            "permissionDecisionReason": "read must name its target (add tb_lines or tb_anchor)",
        }

    # Strip tb_ fields from the executed call.
    updated = {k: v for k, v in tool_input.items() if not k.startswith("tb_")}
    return {"permissionDecision": "allow", "updatedInput": updated}


def _route_write(tool_input: dict) -> dict:
    content = tool_input.get("content", "")
    path = tool_input.get("path", "")
    branch = tool_input.get("branch", "")

    # Reject sha on a file we have never fetched.
    if tool_input.get("sha") and not content.startswith(ghc.DELTA_SENTINEL):
        store_dir = ROOT / ".claude" / ".hook-state" / "gh_blobs"
        store = ghc.BlobStore(store_dir)
        if store.get(path, branch) is None:
            return {
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"sha was supplied for '{path}' but it was never fetched via "
                    "get_file_contents — fetch it first."
                ),
            }

    if content.startswith(ghc.DELTA_SENTINEL):
        store_dir = ROOT / ".claude" / ".hook-state" / "gh_blobs"
        store = ghc.BlobStore(store_dir)
        blob = store.get(path, branch)
        if blob is None:
            return {
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"delta patch requires a fetched body for '{path}' on '{branch}' — "
                    "use get_file_contents first."
                ),
            }
        result = ghc.apply_delta(blob["body"], content)
        if not result.ok:
            return {"permissionDecision": "deny", "permissionDecisionReason": result.reason}
        ok, reason = ghc.write_within_budget(blob["body"], result.content)
        if not ok:
            return {"permissionDecision": "deny", "permissionDecisionReason": reason}
        updated = {**tool_input, "content": result.content, "sha": blob["sha"]}
        return {"permissionDecision": "allow", "updatedInput": updated}

    # Non-delta write: check write budget against fetched body.
    store_dir = ROOT / ".claude" / ".hook-state" / "gh_blobs"
    store = ghc.BlobStore(store_dir)
    blob = store.get(path, branch)
    if blob is not None:
        ok, reason = ghc.write_within_budget(blob["body"], content)
        if not ok:
            return {"permissionDecision": "deny", "permissionDecisionReason": reason}

    return {"permissionDecision": "allow"}


# ---------------------------------------------------------------------------
# Reliability boundary — tested by test_agent_reliability_boundary.py
# ---------------------------------------------------------------------------

PROTECTED_BOUNDARY_PATHS: frozenset[str] = frozenset(
    {
        "src/agent_control/reliability.py",
        "src/agent_control/completion.py",
        "config/command_policy.json",
        ".claude/hooks/pre_tool_use.py",
        ".claude/hooks/_gh_contract.py",
    }
)


def _enforcement(policy: dict) -> str:
    """Return the enforcement mode from the policy dict.

    The TB_COMMAND_POLICY environment variable cannot weaken enforcement;
    only the repository-committed policy dict determines the mode.
    """
    return str(policy.get("enforcement", "block"))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    payload = json.loads(sys.stdin.read())
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    # Strip mcp__github__ prefix for inventory lookup.
    base_tool = tool_name.removeprefix("mcp__github__")

    if base_tool in ghc.DENIED_TOOLS:
        output: dict = {
            "permissionDecision": "deny",
            "permissionDecisionReason": ghc.DENIED_TOOLS[base_tool],
        }
    elif tool_name == "Bash":
        output = _route_bash(tool_input)
    elif base_tool == "create_or_update_file":
        output = _route_write(tool_input)
    elif base_tool == "pull_request_read":
        output = _route_pull_request_read(tool_input)
    elif base_tool in _ALWAYS_CI_TOOLS:
        output = _route_ci_tool(base_tool, tool_input)
    elif base_tool == "get_file_contents":
        output = _route_get_file_contents(tool_input)
    else:
        output = {"permissionDecision": "allow"}

    print(json.dumps({"hookSpecificOutput": output}))
    raise SystemExit(0)


if __name__ == "__main__":
    main()
