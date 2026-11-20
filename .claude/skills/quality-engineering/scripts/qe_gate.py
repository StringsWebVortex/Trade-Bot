"""Quality-registry gate: detects ID collisions across concurrent branches."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import jsonschema
except ImportError:  # the project declares jsonschema; absence is a broken gate runtime
    jsonschema = None

import qe_registry_refs as refs
import qe_evidence

_REPO = Path(__file__).resolve().parents[4]
_SKILL = Path(__file__).resolve().parents[1]
_CONFIG_PATH = _SKILL / "qe.config.json"
_PLAN_SCHEMA_PATH = _SKILL / "schemas" / "change_plan.schema.json"

_GATE_REGISTRY: dict[str, GateFn] = {}


def _register(gate_id: str):
    def decorator(fn):
        _GATE_REGISTRY[gate_id] = fn
        return fn
    return decorator


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


@_register("gate-registry-evidence")
def gate_registry_evidence(config: dict) -> GateResult:
    """Validate registry structure and on-disk test/dependency references."""
    registry_cfg = config.get("registry", {})
    report = qe_evidence.audit(_REPO, registry_cfg.get("path", "config/quality_registry.json"),
                               registry_cfg.get("schema", "config/quality_registry.schema.json"))
    findings = [
        f"{item['code']}: {item.get('entry_id', '')} {item['message']}".strip()
        for item in report["findings"]
    ]
    return GateResult(
        passed=report["passed"],
        blocking=True,
        findings=findings,
        detail=f"{report['entry_count']} registry entries; {len(findings)} finding(s)",
    )


@_register("gate-registry-collision")
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


def _load_config() -> dict:
    try:
        return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"gates": [], "never": [], "registry": {}}


def _validate_plan(plan: dict) -> tuple[bool, str]:
    """Validate the complete plan contract before applying semantic policy."""
    if not isinstance(plan, dict):
        return False, "plan root must be a JSON object"
    if jsonschema is None:
        return False, "jsonschema is unavailable; refusing to accept an unvalidated plan"
    try:
        schema = json.loads(_PLAN_SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = sorted(
            jsonschema.Draft7Validator(schema).iter_errors(plan),
            key=lambda error: (list(error.path), error.message),
        )
    except (OSError, json.JSONDecodeError, jsonschema.SchemaError) as exc:
        return False, f"cannot load a valid change-plan schema: {exc}"
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "<root>"
        return False, f"plan schema violation at {location}: {first.message} ({len(errors)} error(s))"

    if plan["change_class"] == "defect_fix":
        has_new_regression = any(
            requirement["new"] and requirement["id"].startswith("REG-")
            for requirement in plan["requirements"]
        )
        if not has_new_regression:
            return False, (
                "defect_fix requires a new REG- registry entry so the fix is never silently reverted"
            )
    return True, ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qe_gate")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--list", action="store_true", help="List all gate IDs and exit 0")
    group.add_argument("--json", dest="json_output", action="store_true", help="Run all gates; output JSON")
    group.add_argument("--only", metavar="ID", help="Run one gate by ID; exit 2 if unknown")
    group.add_argument("--plan", metavar="PATH", help="Validate a change plan JSON file")
    args = parser.parse_args(argv)

    config = _load_config()

    if args.list:
        for gate in config.get("gates", []):
            print(gate["id"])
        return 0

    if args.plan:
        try:
            plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            print(f"[error] cannot read plan: {exc}", file=sys.stderr)
            return 2
        ok, reason = _validate_plan(plan)
        if not ok:
            print(f"[refused] {reason}", file=sys.stderr)
            return 1
        print("[ok] plan passes")
        return 0

    if args.only:
        gate_id = args.only
        gate_def = next((g for g in config.get("gates", []) if g["id"] == gate_id), None)
        if gate_def is None:
            print(f"[error] unknown gate {gate_id!r}", file=sys.stderr)
            return 2
        fn = _GATE_REGISTRY.get(gate_id)
        if fn is None:
            print(f"[skip] no runner for {gate_id!r}")
            return 0
        result = fn(config)
        if not result.passed:
            for finding in result.findings:
                print(f"  {finding}")
            return 1 if result.blocking else 0
        return 0

    # Default: --json (run all gates)
    results = []
    for gate_def in config.get("gates", []):
        gid = gate_def["id"]
        fn = _GATE_REGISTRY.get(gid)
        blocking = gate_def.get("blocking", False)
        if fn is None:
            results.append({
                "id": gid,
                "blocking": blocking,
                "passed": not blocking,
                "skipped": True,
                "detail": "no runner registered",
                "findings": [] if not blocking else [f"blocking gate {gid!r} has no runner"],
            })
            continue
        gr = fn(config)
        results.append({
            "id": gid,
            "blocking": blocking,
            "passed": gr.passed,
            "skipped": False,
            "detail": gr.detail,
            "findings": gr.findings,
        })

    payload = {"results": results}
    if args.json_output:
        print(json.dumps(payload, indent=2))
    return 1 if any(r["blocking"] and not r["passed"] for r in results) else 0


# Alias for type hints in _register decorator
GateFn = type(gate_registry_id_collision)

if __name__ == "__main__":
    sys.exit(main())
