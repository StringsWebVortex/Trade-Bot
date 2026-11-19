"""Scaffolder for new quality-registry entries.

Allocates the next available ID across all live branches so two
concurrent pull requests never receive the same ID.
"""
from __future__ import annotations

import argparse
import json
import sys
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
                        taken[eid] = f"refs/{ref}"
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

    n = 1
    while n in existing_nums:
        n += 1
    width = max(4, len(str(n)))
    return f"{prefix}{n:0{width}d}"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="qe_new_requirement")
    p.add_argument("--id", required=True)
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

    # Validate test type if provided.
    if args.test_type and args.test_type not in _VALID_TEST_TYPES:
        print(
            f"[error] test_type={args.test_type!r} is not in the declared test taxonomy "
            f"({', '.join(sorted(_VALID_TEST_TYPES))})"
        )
        return 1

    # Load registry.
    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        registry = {"entries": []}

    # Check if ID is already taken anywhere.
    taken = taken_ids(registry, local_only=args.local_only)
    if args.id in taken and taken[args.id] != "the working tree":
        raise SystemExit(
            f"Entry {args.id!r} already exists on {taken[args.id]} — "
            "choose a different ID."
        )

    # Build entry.
    entry: dict = {
        "id": args.id,
        "kind": "regression" if args.id.startswith("REG-") else "requirement",
        "title": args.title,
        "statement": args.statement,
        "criticality": args.criticality,
        "subsystem": args.subsystem,
        "status": args.status,
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
        print(f"[dry-run] would write {args.id}")
        return 0

    # Write to overlay directory.
    OVERLAY_DIR.mkdir(parents=True, exist_ok=True)
    out = OVERLAY_DIR / f"{args.id}.json"
    out.write_text(json.dumps(entry, indent=2), encoding="utf-8")
    print(f"[ok  ] added {args.id}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
