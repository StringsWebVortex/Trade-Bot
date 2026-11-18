#!/usr/bin/env python3
"""PostToolUse hook: lint the one file Claude just edited.

Pass -> no output, exit 0. Failure -> <=20 lines on stderr, exit 2 (Claude
Code shows a PostToolUse hook's stderr to the model on exit 2). Anything
unexpected (missing tool, timeout, bad payload) -> exit 0: never block work.
Uses only the project's own lint config; never modifies files or uses network.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

TIMEOUT_S = 30
MAX_LINES = 20
SKIP_DIRS = {
    "node_modules",
    ".venv",
    "venv",
    ".venv-tmp",
    "dist",
    "build",
    ".git",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "coverage",
    "htmlcov",
    ".claude-backup",
    "site-packages",
}
GENERATED_SUFFIXES = (".min.js", ".bundle.js", "_pb2.py", "_pb2_grpc.py", ".d.ts")
PY = {".py"}
JS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
ESLINT_CONFIGS = (
    "eslint.config.js",
    "eslint.config.mjs",
    "eslint.config.cjs",
    "eslint.config.ts",
    ".eslintrc",
    ".eslintrc.js",
    ".eslintrc.cjs",
    ".eslintrc.json",
    ".eslintrc.yml",
    ".eslintrc.yaml",
)
MYPY_MARKERS = ("mypy.ini", ".mypy.ini")
PYRIGHT_MARKERS = ("pyrightconfig.json",)


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    env = {**os.environ, "NO_COLOR": "1"}
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_S,
        env=env,
        stdin=subprocess.DEVNULL,
        check=False,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def find_up(start: Path, stop: Path, names: tuple[str, ...]) -> Path | None:
    for d in (start, *start.parents):
        if any((d / n).is_file() for n in names):
            return d
        if d == stop:
            break
    return None


def tool(name: str, root: Path, node_dir: Path | None = None) -> str | None:
    for local in (
        root / ".venv" / "bin" / name,
        (node_dir or root) / "node_modules" / ".bin" / name,
    ):
        if local.is_file():
            return str(local)
    return shutil.which(name)


def pyproject_has(root: Path, section: str) -> bool:
    p = root / "pyproject.toml"
    return p.is_file() and f"[tool.{section}" in p.read_text(encoding="utf-8", errors="ignore")


def check_python(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    ruff = tool("ruff", root)
    if ruff:
        rc, out = run(
            [ruff, "check", "--force-exclude", "--output-format=concise", "--no-fix", str(path)],
            root,
        )
        if rc == 1 and out:
            errors += [ln for ln in out.splitlines() if ":" in ln and not ln.startswith("Found")]
    if pyproject_has(root, "mypy") or any((root / m).is_file() for m in MYPY_MARKERS):
        mypy = tool("mypy", root)
        if mypy:
            rc, out = run([mypy, "--follow-imports=silent", "--no-error-summary", str(path)], root)
            if rc == 1:
                errors += [ln for ln in out.splitlines() if ": error:" in ln]
    elif pyproject_has(root, "pyright") or any((root / m).is_file() for m in PYRIGHT_MARKERS):
        pyright = tool("pyright", root)
        if pyright:
            rc, out = run([pyright, str(path)], root)
            if rc == 1:
                errors += [ln.strip() for ln in out.splitlines() if " - error" in ln]
    return errors


def check_js(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    cfg_dir = find_up(path.parent, root, ESLINT_CONFIGS)
    if cfg_dir:
        eslint = tool("eslint", root, cfg_dir)
        if eslint:
            rc, out = run([eslint, "--format", "unix", "--no-warn-ignored", str(path)], cfg_dir)
            if rc == 1:
                errors += [ln for ln in out.splitlines() if ln.count(":") >= 3]
    elif path.suffix in {".js", ".mjs", ".cjs"}:
        # No ESLint config in the project: a config-free syntax check only.
        node = shutil.which("node")
        if node:
            rc, out = run([node, "--check", str(path)], path.parent)
            if rc != 0:
                errors += out.splitlines()[:6]
    # tsc: only per-file when a tsconfig exists would need the whole project; skipped
    # deliberately to keep the hook fast. Run `npx tsc --noEmit` once per batch instead.
    return errors


def main() -> int:
    payload = json.load(sys.stdin)
    raw = (payload.get("tool_input") or {}).get("file_path")
    if not raw:
        return 0
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()).resolve()
    path = Path(raw).resolve()
    try:
        rel = path.relative_to(root)
    except ValueError:
        return 0  # outside the repo
    if (
        not path.is_file()
        or SKIP_DIRS.intersection(rel.parts)
        or path.name.endswith(GENERATED_SUFFIXES)
    ):
        return 0
    if path.suffix in PY:
        errors = check_python(path, root)
    elif path.suffix in JS:
        errors = check_js(path, root)
    else:
        return 0
    if not errors:
        return 0
    shown = errors[:MAX_LINES]
    if len(errors) > MAX_LINES:
        shown.append(f"... {len(errors) - MAX_LINES} more")
    print(f"lint failed for {rel}:", *shown, sep="\n", file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # fail open: a broken hook must never block work
        sys.exit(0)
