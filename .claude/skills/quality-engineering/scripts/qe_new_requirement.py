"""Scaffolder for new quality-registry entries.

Allocates the next available ID across all live branches so two
concurrent pull requests never receive the same ID.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import qe_registry_refs as refs

# Paths can be monkeypatched by tests.
_REPO = Path(__file__).resolve().parents[4]
REGISTRY_PATH = _REPO / "config" / "quality_registry.json"
OVERLAY_DIR = REGISTRY_PATH.with_suffix(".d")

# Valid test types (must match config/quality_registry.json test_types keys).
_VALID_TEST_TYPES = frozenset(
    {
        "unit",
        "component",
        "contract",
        "integration",
        "api",
        "e2e",
        "regression",
        "verification",
        "validation",
        "property",
    }
)


def taken_ids(registry: dict, local_only: bool = False) -> dict[str, str]:
    """
    Return {id: source_description} for every ID already allocated.

    When local_only=False (the default) also scans all remote refs via git
    so two concurrent branches cannot be handed the same ID.
    """
    taken: dict[str, str] = {}

    # Always include local registry entries.
    for entry in registry.get("entries", []):
        taken[entry["id"]] = "the working tree"

    if local_only:
        return taken

    # Scan git refs for entries on other branches.
    try:
        repo = str(_REPO)
        ref_lines = refs._git(repo, "for-each-ref", "--format=%(refname)").splitlines()
        for ref in ref_lines:
            # batch-check the ref
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
                doc = json.loads(blob)
                for entry in doc.get("entries", []):
                    eid = entry["id"]
                    if eid not in taken:
                        taken[eid] = ref
            except Exception:
                continue
    except refs.GitUnavailable:
        pass

    return taken


def next_id(taken: dict[str, str], prefix: str) -> str:
    """Return the next available ID for the given prefix (e.g. "REG-")."""
    existing_nums = set()
    for eid in taken:
        if eid.startswith(prefix):
            tail = eid[len(prefix):]
            if tail.isdigit():
                existing_nums.add(int(tail))

    n = (max(existing_nums) + 1) if existing_nums else 1
    width = max(4, len(str(n)))
    return f"{prefix}{n:0{width}d}"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="qe_new_requirement")
    p.add_argument("--id")
    p.add_argument("--prefix", help="ID prefix (e.g. REG-); auto-allocates the next ID")
    p.add_argument("--title", required=True)
    p.add_argument("--statement", required=True)
    p.add_argument("--criticality", required=True)
    p.add_argument("--subsystem", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--failure-mode", required=True)
    p.add_argument("--status", default="planned")
    p.add_argument("--planned-in")
    p.add_argument("--test", action="append", default=[])
    p.add_argument("--test-type")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--local-only", action="store_true")
    return p


def main(argv: list[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not args.id and not args.prefix:
        print("[error] one of --id or --prefix is required", file=sys.stderr)
        return 1

    # Validate test type if provided.
    if args.test_type and args.test_type not in _VALID_TEST_TYPES:
        print(
            f"[error] test_type={args.test_type!r} is not in the declared test taxonomy "
            f"({', '.join(sorted(_VALID_TEST_TYPES))})"
        )
        return 1

    # Validate status transitions.
    status = args.status
    if status == "accepted_gap":
        print("[error] accepted_gap must be written by hand — a claim about evidence cannot be generated", file=sys.stderr)
        return 1
    if status == "verified" and not args.test:
        print("[error] claim about evidence: verified status requires at least one --test", file=sys.stderr)
        return 1
    if status == "planned" and args.test:
        print("[error] planned status must not name a test; add the test when you mark it verified", file=sys.stderr)
        return 1
    if status == "planned" and not args.planned_in:
        print("[error] planned status requires --planned-in naming the PR that will add the test", file=sys.stderr)
        return 1

    # Load registry.
    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        registry = {"entries": []}

    taken = taken_ids(registry, local_only=args.local_only)

    # Resolve ID.
    if args.prefix:
        entry_id = next_id(taken, args.prefix)
    else:
        entry_id = args.id
        if entry_id in taken and taken[entry_id] != "the working tree":
            raise SystemExit(
                f"Entry {entry_id!r} already exists on {taken[entry_id]} — "
                "choose a different ID."
            )

    # Derive kind from prefix.
    if entry_id.startswith("REG-"):
        kind = "regression"
    elif entry_id.startswith("INV-"):
        kind = "invariant"
    elif entry_id.startswith("SEC-"):
        kind = "security_regression"
    else:
        kind = "requirement"

    # Build entry.
    entry: dict = {
        "id": entry_id,
        "kind": kind,
        "title": args.title,
        "statement": args.statement,
        "criticality": args.criticality,
        "subsystem": args.subsystem,
        "status": status,
        "source": args.source,
        "failure_mode": args.failure_mode,
    }
    if args.planned_in:
        entry["planned_in"] = args.planned_in
    if args.test:
        entry["verification"] = [
            {"test": t, "test_type": args.test_type or "regression"} for t in args.test
        ]

    if args.dry_run:
        print(json.dumps(entry, indent=2))
        return 0

    # Write to overlay directory.
    OVERLAY_DIR.mkdir(parents=True, exist_ok=True)
    out = OVERLAY_DIR / f"{entry_id}.json"
    out.write_text(json.dumps(entry, indent=2), encoding="utf-8")
    print(f"[ok  ] added {entry_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
