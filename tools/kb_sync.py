#!/usr/bin/env python3
"""kb_sync.py: rebuild/check .kb/index.json (run from the repo root).
Usage:
  python tools/kb_sync.py            # full incremental rebuild
  python tools/kb_sync.py --file P   # fast update for one file (post-edit hook)
  python tools/kb_sync.py --check    # exit 1 if index is stale/orphaned/unindexed
"""
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

IDX = Path(".kb/index.json")
JS_SYM = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)|class\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\()", re.M)
SKIP = ("node_modules/", "dist/", "build/", ".kb/")
SKIP_EXT = (".lock", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".pyc", ".min.js")


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True, check=True).stdout


def wanted(f):
    return Path(f).is_file() and not f.startswith(SKIP) and not f.endswith(SKIP_EXT)


def tracked():
    # tracked files plus untracked-but-not-ignored, so new files are indexed too
    out = sh("git", "ls-files", "--cached", "--others", "--exclude-standard")
    return {f for f in out.splitlines() if wanted(f)}


def digest(p):
    return hashlib.sha1(Path(p).read_bytes()).hexdigest()


def symbols(p):
    p = Path(p)
    src = p.read_text(errors="ignore")
    if p.suffix == ".py":
        try:
            return [{"name": n.name, "kind": type(n).__name__, "line": n.lineno, "end": n.end_lineno}
                    for n in ast.walk(ast.parse(src))
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        except SyntaxError:
            return [{"error": "syntax"}]
    if p.suffix in (".js", ".jsx", ".ts", ".tsx"):  # regex for now; tree-sitter is more accurate
        return [{"name": next(g for g in m.groups() if g), "line": src[:m.start()].count("\n") + 1}
                for m in JS_SYM.finditer(src)]
    return []


def entry(f):
    return {"hash": digest(f), "symbols": symbols(f)}


def load():
    return json.loads(IDX.read_text()) if IDX.exists() else {"files": {}}


def build(old):
    new = {}
    for f in sorted(tracked()):
        h = digest(f)
        new[f] = old["files"][f] if f in old["files"] and old["files"][f]["hash"] == h else entry(f)
    return {"files": new}


def check(idx):
    problems = []
    live = tracked()
    for f, e in idx["files"].items():
        if f not in live:
            problems.append(f"ORPHAN {f}")
        elif digest(f) != e["hash"]:
            problems.append(f"STALE {f}")
    problems += [f"UNINDEXED {f}" for f in sorted(live - set(idx["files"]))]
    return problems


if __name__ == "__main__":
    old = load()
    if "--check" in sys.argv:
        bad = check(old)
        print("\n".join(bad) or "KB OK")
        sys.exit(1 if bad else 0)
    if "--file" in sys.argv:
        f = sys.argv[sys.argv.index("--file") + 1]
        if Path(f).is_file() and wanted(f):
            old["files"][f] = entry(f)
        else:
            old["files"].pop(f, None)
        new = old
    else:
        new = build(old)
    IDX.parent.mkdir(exist_ok=True)
    IDX.write_text(json.dumps(new, indent=1))
    print(f"indexed {len(new['files'])} files")
