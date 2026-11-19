"""Quality-registry gate: detects ID collisions across concurrent branches."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import qe_registry_refs as refs

_REPO = Path(__file__).resolve().parents[4]


@dataclass
class GateResult:
    passed: bool
    blocking: bool = False
    findings: list[str] = field(default_factory=list)
    detail: str = ""


def _read_registry_entries(registry_path: str) -> list[dict]:
    """Read entries from the working-tree registry file."""
    try:
        doc = json.loads(Path(registry_path).read_text(encoding="utf-8"))
        return doc.get("entries", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def gate_registry_id_collision(config: dict) -> GateResult:
    """
    Check for ID collisions between the working tree and live branches.

    Returns a non-blocking advisory GateResult if a collision is found
    (stale branches must not block merges).
    """
    registry_cfg = config.get("registry", {})
    registry_path = registry_cfg.get("path", "config/quality_registry.json")
    full_path = str(_REPO / registry_path)

    local_entries = {e["id"]: e for e in _read_registry_entries(full_path)}

    if not local_entries:
        return GateResult(passed=True, detail="no new ids allocated on this branch")

    # Scan remote refs for the same IDs.
    findings: list[str] = []
    try:
        repo = str(_REPO)
        ref_lines = refs._git(repo, "for-each-ref", "--format=%(refname)").splitlines()

        # Determine merge-base entries (IDs already on the base branch).
        base_ids: set[str] = set()
        try:
            base_sha = refs._git(repo, "merge-base", "HEAD", "origin/main").strip()
            base_blob = refs._git(repo, "cat-file", "blob", base_sha)
            base_doc = json.loads(base_blob)
            base_ids = {e["id"] for e in base_doc.get("entries", [])}
        except Exception:
            pass

        # Only examine IDs that are new on this branch (not on the base).
        new_ids = {eid: e for eid, e in local_entries.items() if eid not in base_ids}
        if not new_ids:
            return GateResult(passed=True, detail="no new ids on this branch vs the base")

        for ref in ref_lines:
            check = refs._git(
                repo,
                "cat-file",
                "--batch-check=%(objectname) %(objecttype)",
                stdin=ref + "\n",
            )
            parts = check.strip().split()
            if len(parts) < 2 or parts[1] != "blob":
                continue
            sha = parts[0]
            try:
                blob = refs._git(repo, "cat-file", "blob", sha)
                remote_doc = json.loads(blob)
            except Exception:
                continue

            for remote_entry in remote_doc.get("entries", []):
                eid = remote_entry["id"]
                if eid not in new_ids:
                    continue
                local_entry = new_ids[eid]
                # Same body → same requirement, not a collision.
                if remote_entry == local_entry:
                    continue
                findings.append(
                    f"ID {eid!r} exists on {ref} with a different body — "
                    "one of the two branches has a stale copy"
                )

    except refs.GitUnavailable:
        return GateResult(passed=True, detail="git unavailable — skipping ref scan")

    if findings:
        return GateResult(
            passed=False,
            blocking=False,
            findings=findings,
            detail=f"{len(findings)} advisory collision(s) found",
        )

    return GateResult(passed=True, detail="no id collisions detected")
