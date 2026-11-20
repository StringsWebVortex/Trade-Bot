#!/usr/bin/env python3
"""Repo-wide KG ingestion (Component 5 support).

Walks every first-party source/doc file tracked by git and runs the
extract -> resolve -> assemble pipeline (kg.ingest.ingest_document) on each,
replacing the graph's contents with the result. Every node and edge the run
writes is stamped with its run id, and the ones it did not write are deleted
only after every file has been processed (audit OPS-009): a run that dies
partway leaves the previous graph in place rather than an empty one. Unlike scripts/ingest_repo.py
(RAG, local embeddings, free), each file here costs two `claude -p`
subprocess calls (haiku extract + sonnet resolve) -- run deliberately, not
on a schedule.
"""

from __future__ import annotations

import subprocess
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# `python scripts/x.py` puts scripts/ on sys.path, not the repo root, so the
# first-party imports below are not resolvable on their own -- the RAG ingest
# workflow failed on exactly that (ModuleNotFoundError: rag_mongo). Anchoring
# on __file__ rather than the cwd keeps it correct from any directory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kg.db import get_edges_collection, get_nodes_collection  # noqa: E402
from kg.ingest import ingest_document  # noqa: E402

EXCLUDE_PATHSPECS = [":!:frontend/*", ":!:.venv/*", ":!:crypto-predictor/*"]
INCLUDE_GLOBS = ["*.py", "*.md", "*.toml", "*.yml", "*.yaml"]
MAX_WORKERS = 4


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "--", *INCLUDE_GLOBS, *EXCLUDE_PATHSPECS],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in out.stdout.splitlines() if line]


def ingest_one(path: str, run_id: str | None = None) -> tuple[str, dict]:
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except (UnicodeDecodeError, OSError) as exc:
        return path, {"error": str(exc)}
    if not text.strip():
        return path, {"skipped": "empty"}
    try:
        return path, ingest_document(text, source=path, run_id=run_id)
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort the run
        return path, {"error": str(exc)}


def main() -> None:
    files = tracked_files()
    print(f"Found {len(files)} tracked files to ingest into the KG.")

    nodes_col = get_nodes_collection()
    edges_col = get_edges_collection()
    run_id = uuid.uuid4().hex

    t0 = time.time()
    done = 0
    errors: list[str] = []
    total_triples = total_nodes = total_edges = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(ingest_one, p, run_id): p for p in files}
        for fut in as_completed(futures):
            path, result = fut.result()
            done += 1
            if "error" in result:
                errors.append(f"{path}: {result['error']}")
            elif "skipped" not in result:
                total_triples += result.get("triples_extracted", 0)
                total_nodes += result.get("nodes_upserted", 0)
                total_edges += result.get("edges_upserted", 0)
            if done % 10 == 0 or done == len(files):
                elapsed = time.time() - t0
                print(
                    f"  processed {done}/{len(files)} "
                    f"(errors so far: {len(errors)}, {elapsed:.0f}s elapsed)",
                    file=sys.stderr,
                )

    stale = {"run_id": {"$ne": run_id}}
    dn = nodes_col.delete_many(stale).deleted_count
    de = edges_col.delete_many(stale).deleted_count
    print(f"Cleared {dn} stale nodes, {de} stale edges.")

    elapsed = time.time() - t0
    print(f"Processed {done} files in {elapsed:.1f}s.")
    print(
        f"Extracted {total_triples} triples -> {total_nodes} nodes, {total_edges} edges upserted."
    )
    if errors:
        print(f"{len(errors)} files failed:")
        for e in errors[:30]:
            print(f"  {e}")


if __name__ == "__main__":
    main()
