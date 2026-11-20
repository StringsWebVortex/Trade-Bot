"""GitHub route contract — tool inventory, delta patch, write budget, blob store."""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DELTA_SENTINEL = "##CLAUDE-DELTA##"
HARD_MAX_DELTA_BLOCKS = 20
HARD_MAX_TARGET_LINES = 100

_SMALL_FILE_THRESHOLD = 10
_BULK_REWRITE_RATIO = 0.5


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass
class Result:
    ok: bool
    content: str = ""
    reason: str = ""


# ---------------------------------------------------------------------------
# Delta patch
# ---------------------------------------------------------------------------

_BLOCK_RE = re.compile(
    r"<<<<<<< OLD\n(.*?)\n======= NEW\n(.*?)\n>>>>>>> END\n",
    re.DOTALL,
)


def apply_delta(base: str, patch: str) -> Result:
    """Apply a DELTA_SENTINEL-prefixed patch to base text."""
    if not patch.startswith(DELTA_SENTINEL + "\n"):
        return Result(ok=False, reason="payload is not well-formed: missing sentinel")

    body = patch[len(DELTA_SENTINEL) + 1 :]
    blocks = _BLOCK_RE.findall(body)

    if not blocks and body.strip():
        return Result(ok=False, reason="payload is not well-formed: no recognizable blocks")

    if len(blocks) > HARD_MAX_DELTA_BLOCKS:
        return Result(
            ok=False,
            reason=(
                f"at most {HARD_MAX_DELTA_BLOCKS} delta blocks are allowed; "
                f"got {len(blocks)}"
            ),
        )

    result = base
    for old, new in blocks:
        old_with_nl = old + "\n"
        count = result.count(old_with_nl)
        if count == 0:
            return Result(ok=False, reason=f"anchor is not present in the file: {old!r}")
        if count > 1:
            return Result(ok=False, reason=f"anchor is ambiguous ({count} matches): {old!r}")
        result = result.replace(old_with_nl, new + "\n", 1)

    return Result(ok=True, content=result)


# ---------------------------------------------------------------------------
# Write budget
# ---------------------------------------------------------------------------


def write_within_budget(before: str, after: str) -> tuple[bool, str]:
    """Return (ok, reason). Refuses identical writes and bulk rewrites."""
    if before == after:
        return False, "identical content — no change detected"

    before_lines = before.splitlines()
    after_lines = after.splitlines()

    if len(before_lines) < _SMALL_FILE_THRESHOLD:
        return True, ""

    changed = sum(1 for a, b in zip(before_lines, after_lines, strict=False) if a != b)
    changed += abs(len(before_lines) - len(after_lines))
    ratio = changed / max(len(before_lines), 1)

    if ratio > _BULK_REWRITE_RATIO:
        return False, f"bulk-rewrite cap exceeded: {ratio:.0%} of lines changed"

    return True, ""


# ---------------------------------------------------------------------------
# Blob store
# ---------------------------------------------------------------------------


class BlobStore:
    """Stores fetched file bodies keyed by path + branch."""

    def __init__(self, directory: Path) -> None:
        self._dir = directory
        self._dir.mkdir(parents=True, exist_ok=True)

    def _key(self, path: str, branch: str) -> Path:
        digest = hashlib.sha256(f"{path}\x00{branch}".encode()).hexdigest()
        return self._dir / digest

    def put(self, path: str, branch: str, body: str, sha: str = "") -> None:
        self._key(path, branch).write_text(json.dumps({"body": body, "sha": sha}))

    def get(self, path: str, branch: str) -> dict | None:
        key = self._key(path, branch)
        if not key.exists():
            return None
        return json.loads(key.read_text())


# ---------------------------------------------------------------------------
# Read target slicer
# ---------------------------------------------------------------------------


def slice_to_target(body: str, target: dict) -> tuple[str, str]:
    """Slice a file body to the named target. Returns (block, problem)."""
    lines = body.splitlines()

    if "tb_lines" in target:
        spec = str(target["tb_lines"])
        if "-" in spec:
            parts = spec.split("-", 1)
            start = int(parts[0]) - 1
            end = int(parts[1])
        else:
            n = int(spec)
            start, end = n - 1, n
        start = max(0, start)
        end = min(len(lines), end, start + HARD_MAX_TARGET_LINES)
        selected = lines[start:end]
        block = "\n".join(f"{i + start + 1}| {line}" for i, line in enumerate(selected))
        return block, ""

    if "tb_anchor" in target:
        anchor = str(target["tb_anchor"])
        matches = [i for i, line in enumerate(lines) if anchor in line]
        if len(matches) > 1:
            return "", f"anchor matches {len(matches)} lines — make it unique"
        capped = lines[:HARD_MAX_TARGET_LINES]
        block = "\n".join(f"{i + 1}| {line}" for i, line in enumerate(capped))
        return block, ""

    return "", "no target specified"


# ---------------------------------------------------------------------------
# CI URL detection
# ---------------------------------------------------------------------------

_CI_URL_RE = re.compile(
    r"(?:api\.github\.com|github\.com/)[^#\s]*"
    r"(?:/actions/|/check-runs?|/check-suites?|/statuses/|/artifacts|/workflow_runs)",
    re.IGNORECASE,
)
_PR_NUMBER_RE = re.compile(r"/pulls?/(\d+)")


def _is_ci_url(url: str) -> bool:
    return bool(_CI_URL_RE.search(url))


def _pr_number_from_url(url: str) -> int | None:
    m = _PR_NUMBER_RE.search(url)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Tool inventory
# ---------------------------------------------------------------------------

# Tools allowed with specific routing contracts.
CONTRACTS: dict[str, str] = {
    "create_or_update_file": "write-budget + delta-patch route",
    "get_file_contents": "read with target narrowing; CI URLs return verdict",
    "pull_request_read": "CI check-status methods return verdict",
    "get_workflow_run_logs": "CI log — verdict only",
    "list_workflow_run_artifacts": "CI artifact listing — verdict only",
    "add_issue_comment": "issue comment write allowed",
    "add_reply_to_pull_request_comment": "PR comment reply allowed",
    "issue_read": "issue read allowed",
    "issue_write": "issue write allowed",
    "list_pull_requests": "PR list allowed",
    "list_issues": "issue list allowed",
    "list_commits": "commit list allowed",
    "get_commit": "commit read allowed",
    "list_branches": "branch list allowed",
    "create_branch": "branch create allowed",
    "get_tag": "tag read allowed",
    "list_tags": "tag list allowed",
    "list_releases": "release list allowed",
    "get_latest_release": "latest release allowed",
    "get_release_by_tag": "release by tag allowed",
    "get_me": "user info allowed",
    "list_repository_collaborators": "collaborator list allowed",
    "get_teams": "team list allowed",
    "get_team_members": "team members allowed",
    "actions_list": "actions list allowed",
    "actions_get": "action get allowed",
    "actions_run_trigger": "action run trigger allowed",
    "get_check_run": "check run read allowed",
    "get_job_logs": "job logs read allowed",
    "get_label": "label read allowed",
    "list_issue_fields": "issue fields allowed",
    "list_issue_types": "issue types allowed",
    "update_issue_comment": "issue comment update allowed",
    "update_pull_request": "PR update allowed",
    "update_pull_request_branch": "PR branch update allowed",
    "request_copilot_review": "copilot review request allowed",
    "resolve_review_thread": "review thread resolve allowed",
    "unresolve_review_thread": "review thread unresolve allowed",
    "run_secret_scanning": "secret scanning allowed",
    "sub_issue_write": "sub-issue write allowed",
    "disable_pr_auto_merge": "PR auto-merge disable allowed",
    "enable_pr_auto_merge": "PR auto-merge enable allowed",
    "add_comment_to_pending_review": "pending review comment allowed",
}

# Tools explicitly denied. All values must be non-empty reason strings.
DENIED_TOOLS: dict[str, str] = {
    "push_files": "Direct multi-file push bypasses the write-budget and delta-patch contract.",
    "delete_file": "File deletion requires a governance review outside this session.",
    "merge_pull_request": "PR merges are a human-only action; no automated merge is permitted.",
    "create_repository": "Repository creation requires explicit owner approval.",
    "fork_repository": "Repository forking requires explicit owner approval.",
    "pull_request_review_write": "Review submission is a human-only action.",
}

# Full verified inventory: every tool the connected server exposes.
# Must equal the union of CONTRACTS and DENIED_TOOLS keys.
VERIFIED_SERVER_TOOLS: frozenset[str] = frozenset(CONTRACTS) | frozenset(DENIED_TOOLS)


def unresolved_tools() -> frozenset[str]:
    """Return tools in VERIFIED_SERVER_TOOLS not covered by any contract or denial."""
    return VERIFIED_SERVER_TOOLS - frozenset(CONTRACTS) - frozenset(DENIED_TOOLS)
