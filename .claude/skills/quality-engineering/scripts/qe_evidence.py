"""Audit quality-registry traceability without executing repository commands.

The report verifies structural references and on-disk test targets only. It does
not claim that a test ran or passed; execution evidence belongs to CI.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:  # A missing validator must never produce a green audit.
    jsonschema = None

DEFAULT_REGISTRY = "config/quality_registry.json"
DEFAULT_SCHEMA = "config/quality_registry.schema.json"
_TEST_PATH = re.compile(
    r"^(tests/[A-Za-z0-9_/]+\\.py(::[A-Za-z0-9_:]+)?|"
    r"frontend/src/[A-Za-z0-9_./-]+\\.test\\.jsx?)$"
)


def _finding(code: str, message: str, entry_id: str = "") -> dict[str, str]:
    item = {"code": code, "message": message}
    if entry_id:
        item["entry_id"] = entry_id
    return item


def audit(root: Path, registry_rel: str = DEFAULT_REGISTRY,
          schema_rel: str = DEFAULT_SCHEMA) -> dict[str, Any]:
    """Return a deterministic audit report for the registry at *root*."""
    findings: list[dict[str, str]] = []
    root = root.resolve()

    try:
        registry_path = (root / registry_rel).resolve(strict=True)
        schema_path = (root / schema_rel).resolve(strict=True)
        registry_path.relative_to(root)
        schema_path.relative_to(root)
        raw = json.loads(registry_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {
            "schema_version": 1,
            "registry": registry_rel,
            "entry_count": 0,
            "findings": [_finding("INPUT_ERROR", str(exc))],
            "passed": False,
        }

    if jsonschema is None:
        findings.append(_finding(
            "VALIDATOR_UNAVAILABLE",
            "jsonschema is unavailable; refusing to accept an unvalidated registry",
        ))
    else:
        try:
            validator = jsonschema.Draft7Validator(schema)
            errors = sorted(
                validator.iter_errors(raw),
                key=lambda error: (list(error.path), error.message),
            )
            for error in errors:
                location = "/".join(str(part) for part in error.path) or "<root>"
                findings.append(_finding(
                    "SCHEMA_INVALID", f"{location}: {error.message}"
                ))
        except (jsonschema.SchemaError, TypeError) as exc:
            findings.append(_finding("SCHEMA_INVALID", str(exc)))

    entries = raw.get("entries", []) if isinstance(raw, dict) else []
    if not isinstance(entries, list):
        entries = []
        findings.append(_finding("REGISTRY_INVALID", "'entries' must be an array"))

    by_id: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            findings.append(_finding("ENTRY_INVALID", "entry must be an object"))
            continue
        entry_id = entry.get("id", "")
        if not isinstance(entry_id, str) or not entry_id:
            findings.append(_finding("ENTRY_INVALID", "entry has no valid id"))
            continue
        if entry_id in by_id:
            findings.append(_finding("DUPLICATE_ID", "duplicate registry identifier", entry_id))
        else:
            by_id[entry_id] = entry

        for verification in entry.get("verification", []) or []:
            if not isinstance(verification, dict):
                findings.append(_finding("VERIFICATION_INVALID", "verification must be an object", entry_id))
                continue
            test = verification.get("test", "")
            if not isinstance(test, str) or not _TEST_PATH.fullmatch(test):
                findings.append(_finding("TEST_PATH_INVALID", f"unsafe or unsupported test path: {test!r}", entry_id))
                continue
            file_part = test.split("::", 1)[0]
            try:
                target = (root / file_part).resolve(strict=True)
                target.relative_to(root)
                if not target.is_file():
                    raise FileNotFoundError(file_part)
            except (OSError, ValueError):
                findings.append(_finding("TEST_MISSING", f"test target is missing or escapes the repository: {file_part}", entry_id))

    for entry_id, entry in by_id.items():
        for dependency in entry.get("depends_on", []) or []:
            if dependency not in by_id:
                findings.append(_finding("DEPENDENCY_MISSING", f"unknown dependency {dependency!r}", entry_id))

    # DFS with three colours; emit one stable finding per back-edge.
    colour: dict[str, int] = {}
    cycle_edges: set[tuple[str, str]] = set()

    def visit(entry_id: str) -> None:
        colour[entry_id] = 1
        for dependency in sorted(by_id[entry_id].get("depends_on", []) or []):
            if dependency not in by_id:
                continue
            if colour.get(dependency, 0) == 1:
                cycle_edges.add((entry_id, dependency))
            elif colour.get(dependency, 0) == 0:
                visit(dependency)
        colour[entry_id] = 2

    for entry_id in sorted(by_id):
        if colour.get(entry_id, 0) == 0:
            visit(entry_id)
    for source, target in sorted(cycle_edges):
        findings.append(_finding("DEPENDENCY_CYCLE", f"dependency cycle edge {source} -> {target}", source))

    findings.sort(key=lambda item: (
        item.get("entry_id", ""), item["code"], item["message"]
    ))
    return {
        "schema_version": 1,
        "registry": registry_rel,
        "entry_count": len(entries),
        "findings": findings,
        "passed": not findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--registry", default=DEFAULT_REGISTRY)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)
    report = audit(args.root, args.registry, args.schema)
    if args.json_output:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif report["passed"]:
        print(f"[ok] {report['entry_count']} registry entries; all test references resolve")
    else:
        for item in report["findings"]:
            where = f" [{item['entry_id']}]" if "entry_id" in item else ""
            print(f"[{item['code']}]{where} {item['message']}", file=sys.stderr)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
