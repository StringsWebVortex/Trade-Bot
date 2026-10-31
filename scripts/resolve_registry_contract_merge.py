#!/usr/bin/env python3
"""Resolve legacy registry-contract test conflicts after validating their scope.

Older pull requests extend a literal list of registry ids and a literal metric
count in ``tests/regression/test_regression_registry_contract.py``. The current
test derives both expectations from the registry, so those branch-only edits
are redundant. This resolver discards them only when the branch's AST differs
from the merge base solely in those two literals; any behavioral edit is left
for a person to resolve.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

DEFAULT_PATH = "tests/regression/test_regression_registry_contract.py"


class UnsafeMerge(Exception):
    """The PR changed more than the legacy registry expectation pins."""


def _stage(number: int, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f":{number}:{path}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def _assertions(tree: ast.Module) -> tuple[list[ast.Assert], ast.Assert]:
    id_assertions: list[ast.Assert] = []
    metric_assertion = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for method in node.body:
            if not isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if method.name == "test_the_filed_defects_are_the_ones_we_know_about":
                id_assertions = [
                    item
                    for item in ast.walk(method)
                    if isinstance(item, ast.Assert)
                    and isinstance(item.test, ast.Compare)
                    and isinstance(item.test.left, ast.SetComp)
                    and item.test.comparators
                    and isinstance(item.test.comparators[0], ast.Set)
                ]
            elif method.name == "test_a_filed_defect_is_counted_against_its_layer":
                metric_assertion = next(
                    (
                        item
                        for item in ast.walk(method)
                        if isinstance(item, ast.Assert)
                        and isinstance(item.test, ast.Compare)
                        and isinstance(item.test.left, ast.Subscript)
                        and isinstance(item.test.left.value, ast.Name)
                        and item.test.left.value.id == "metric"
                        and item.test.comparators
                        and isinstance(item.test.comparators[0], ast.Dict)
                    ),
                    None,
                )
    if not id_assertions or metric_assertion is None:
        raise UnsafeMerge("expected registry id/count assertions were not found")
    return id_assertions, metric_assertion


def _normalized(text: str) -> tuple[str, set[str], dict[str, int]]:
    tree = ast.parse(text)
    id_assertions, metric_assertion = _assertions(tree)
    ids = set()
    for assertion in id_assertions:
        values = ast.literal_eval(assertion.test.comparators[0])
        if not isinstance(values, set) or not all(isinstance(item, str) for item in values):
            raise UnsafeMerge("registry id assertion is not a literal string set")
        ids.update(values)
    counts = ast.literal_eval(metric_assertion.test.comparators[0])
    if not isinstance(counts, dict) or not all(
        isinstance(key, str) and isinstance(value, int) for key, value in counts.items()
    ):
        raise UnsafeMerge("layer counts are not a literal string-to-integer mapping")

    for assertion in id_assertions:
        assertion.test.comparators[0] = ast.Constant(value="<registry-id-pin>")
    metric_assertion.test.comparators[0] = ast.Constant(value="<layer-count-pin>")
    return ast.dump(tree, include_attributes=False), ids, counts


def can_discard_legacy_pins(base: str, branch: str) -> bool:
    """Return true only when branch edits are additive expectation pins."""
    try:
        normalized_base, base_ids, base_counts = _normalized(base)
        normalized_branch, branch_ids, branch_counts = _normalized(branch)
    except (SyntaxError, ValueError, UnsafeMerge):
        return False
    return (
        normalized_base == normalized_branch
        and base_ids <= branch_ids
        and all(branch_counts.get(key, 0) >= count for key, count in base_counts.items())
    )


def main(argv: list[str]) -> int:
    path = argv[1] if len(argv) > 1 else DEFAULT_PATH
    try:
        base = _stage(1, path)
        branch = _stage(2, path)
        mainline = _stage(3, path)
    except subprocess.CalledProcessError:
        print(f"{path} is not in a conflicted merge state.", file=sys.stderr)
        return 1

    if not can_discard_legacy_pins(base, branch):
        print(
            f"{path}: branch edits include behavior beyond additive registry pins; "
            "leaving this conflict for review.",
            file=sys.stderr,
        )
        return 1

    Path(path).write_text(mainline, encoding="utf-8")
    print(f"{path}: retained main's registry-derived contract assertions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
