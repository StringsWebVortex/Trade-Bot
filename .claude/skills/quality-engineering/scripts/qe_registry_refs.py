#!/usr/bin/env python3
"""
Read the quality registry as it exists in the working tree and on *other*
git refs: `config/quality_registry.json` plus the one-entry-per-file directory
`config/quality_registry.d/` (GOV-071).

Id allocation used to scan only the working tree, which sees ids already
merged to main and nothing else. Two branches open at the same time were
therefore handed the same next id -- three times in one session, each caught
by hand. The failure mode on merge is two different requirements sharing an
id, or a renumber that silently breaks a `depends_on` pointing at the old one.

Nothing here talks to the network. It reads refs that are already in the
object store (local branches and remote-tracking branches), so it is fast and
works offline; `git fetch` first if you want it to see branches pushed since
your last fetch.

The scan is two git invocations regardless of how many refs exist: one
`--batch-check` to resolve every `<ref>:path` to a blob, then one `--batch`
for the handful of *distinct* blobs behind them. Most branches carry an
identical registry, so the second call reads two or three objects, not two
hundred. The per-entry directory adds one `ls-tree` per distinct directory and
one read per distinct entry file, shared across every ref that carries it.
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REGISTRY_REL_PATH = "config/quality_registry.json"
OVERLAY_REL_PATH = "config/quality_registry.d"

# One second-ish of work is fine; a wedged git is not worth waiting on.
GIT_TIMEOUT_S = 30


@dataclass(frozen=True)
class RefEntry:
    """One registry entry as it appears on one ref."""

    ref: str
    entry_id: str
    body: str  # canonical JSON, so "same id, same entry" is a string compare


class GitUnavailable(RuntimeError):
    """Not a git work tree, or git is not on PATH. Callers fail open."""


def _git(repo: Path, *args: str, stdin: str | None = None) -> str:
    try:
        proc = subprocess.run(  # noqa: S603 - fixed argv, no shell
            ["git", *args],
            cwd=repo,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_S,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitUnavailable(str(exc)) from exc
    if proc.returncode != 0:
        raise GitUnavailable((proc.stderr or "").strip() or f"git {args[0]} failed")
    return proc.stdout


def list_refs(repo: Path, *, filters: Sequence[str] = ()) -> list[str]:
    """
    Local branches and remote-tracking branches, newest first.

    `filters` are passed to `for-each-ref` verbatim -- `--no-merged main` for
    the live branches, `--no-contains HEAD` to drop this branch's own
    descendants. Allocation wants every ref (a merged branch's id is taken
    whether or not this working tree has caught up); collision detection
    wants only branches that are neither merged nor this one.
    """
    args = ["for-each-ref", "--sort=-committerdate", "--format=%(refname)"]
    args += list(filters)
    args += ["refs/heads", "refs/remotes"]
    refs = [line.strip() for line in _git(repo, *args).splitlines() if line.strip()]
    # A remote's symbolic HEAD duplicates whatever it points at.
    return [r for r in refs if not r.endswith("/HEAD")]


def read_document(path: Path) -> dict[str, Any]:
    """
    The working-tree registry as one document: the base file with every entry
    file from its sibling `.d` directory appended, as `src/quality/registry.py`
    reads it. Stdlib only, because the scripts here do not import the project.
    """
    document = json.loads(path.read_text(encoding="utf-8"))
    overlay = path.with_suffix(".d")
    if overlay.is_dir() and isinstance(document.get("entries"), list):
        document["entries"] = [
            *document["entries"],
            *(json.loads(f.read_text(encoding="utf-8")) for f in sorted(overlay.glob("*.json"))),
        ]
    return document


def _blobs_for(repo: Path, refs: list[str]) -> dict[str, list[str]]:
    """{blob sha: refs carrying it}, skipping refs with no registry at all."""
    if not refs:
        return {}
    stdin = "".join(f"{ref}:{REGISTRY_REL_PATH}\n" for ref in refs)
    out = _git(repo, "cat-file", "--batch-check=%(objectname) %(objecttype)", stdin=stdin)
    by_blob: dict[str, list[str]] = {}
    for ref, line in zip(refs, out.splitlines(), strict=False):
        parts = line.split()
        if len(parts) < 2 or parts[1] != "blob":
            continue  # "missing" -- that ref predates the registry
        by_blob.setdefault(parts[0], []).append(ref)
    return by_blob


def _entries_in_blob(repo: Path, sha: str) -> dict[str, str] | None:
    raw = _git(repo, "cat-file", "blob", sha)
    try:
        document = json.loads(raw)
        entries = document["entries"]
    except (ValueError, KeyError, TypeError):
        return None  # a malformed registry on some branch is that branch's problem
    out: dict[str, str] = {}
    for entry in entries:
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            out[entry["id"]] = json.dumps(entry, sort_keys=True)
    return out


def _overlay_trees_for(repo: Path, refs: list[str]) -> dict[str, list[str]]:
    """{tree sha: refs carrying it} for the per-entry directory."""
    if not refs:
        return {}
    stdin = "".join(f"{ref}:{OVERLAY_REL_PATH}\n" for ref in refs)
    out = _git(repo, "cat-file", "--batch-check=%(objectname) %(objecttype)", stdin=stdin)
    by_tree: dict[str, list[str]] = {}
    for ref, line in zip(refs, out.splitlines(), strict=False):
        parts = line.split()
        if len(parts) < 2 or parts[1] != "tree":
            continue  # that ref predates the directory
        by_tree.setdefault(parts[0], []).append(ref)
    return by_tree


def _entries_in_tree(repo: Path, sha: str, bodies: dict[str, str | None]) -> dict[str, str]:
    """
    The entries in one per-entry directory. `bodies` caches blob sha -> body
    across trees: branches share most entry files, so each is read once.
    """
    out: dict[str, str] = {}
    for line in _git(repo, "ls-tree", sha).splitlines():
        meta, _, name = line.partition("\t")
        fields = meta.split()
        if len(fields) < 3 or fields[1] != "blob" or not name.endswith(".json"):
            continue
        blob = fields[2]
        if blob not in bodies:
            try:
                entry = json.loads(_git(repo, "cat-file", "blob", blob))
            except ValueError:
                entry = None
            ok = isinstance(entry, dict) and isinstance(entry.get("id"), str)
            bodies[blob] = json.dumps(entry, sort_keys=True) if ok else None
        body = bodies[blob]
        if body is not None:
            out[json.loads(body)["id"]] = body
    return out


def _overlay_entries(repo: Path, refs: list[str]) -> list[RefEntry]:
    found: list[RefEntry] = []
    bodies: dict[str, str | None] = {}
    for sha, carriers in _overlay_trees_for(repo, refs).items():
        entries = _entries_in_tree(repo, sha, bodies)
        for ref in carriers:
            found.extend(RefEntry(ref, eid, body) for eid, body in entries.items())
    return found


def entries_on_refs(repo: Path, *, filters: Sequence[str] = ()) -> list[RefEntry]:
    """Every registry entry visible on any other ref, tagged with its ref."""
    refs = list_refs(repo, filters=filters)
    by_blob = _blobs_for(repo, refs)
    found: list[RefEntry] = []
    for sha, carriers in by_blob.items():
        entries = _entries_in_blob(repo, sha)
        if entries is None:
            continue
        for ref in carriers:
            found.extend(RefEntry(ref, eid, body) for eid, body in entries.items())
    return found + _overlay_entries(repo, refs)


def ids_on_refs(repo: Path, *, filters: Sequence[str] = ()) -> dict[str, str]:
    """{id: one ref carrying it}. The ref is for the error message."""
    out: dict[str, str] = {}
    for item in entries_on_refs(repo, filters=filters):
        out.setdefault(item.entry_id, item.ref)
    return out


def ids_at(repo: Path, commitish: str) -> set[str] | None:
    """The registry ids at one commit-ish, or None if it has no registry."""
    by_blob = _blobs_for(repo, [commitish])
    for sha in by_blob:
        entries = _entries_in_blob(repo, sha)
        if entries is None:
            return None
        return set(entries) | {item.entry_id for item in _overlay_entries(repo, [commitish])}
    return None


def merge_base(repo: Path, a: str, b: str) -> str | None:
    """The fork point, or None when the two share no history."""
    try:
        out = _git(repo, "merge-base", a, b).strip()
    except GitUnavailable:
        return None
    return out or None
