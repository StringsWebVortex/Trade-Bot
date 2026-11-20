"""REG-1603: a failed rebuild never leaves the RAG index or the KG empty (audit OPS-009).

Both ingest scripts used to ``delete_many({})`` before embedding or extracting
anything, so a run that died partway left the store empty or partial. They now
write first, tagged with the run id, and delete what the run did not write only
once it has finished; a failed RAG run removes its own partial insert.

The embedding model is replaced by a stub module, so nothing heavy is imported.

Decides: REG-1603"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from kg.assemble import assemble

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


class _Collection:
    """The insert/update/delete calls the scripts make, over a list of dicts."""

    def __init__(self, docs: list[dict[str, Any]] | None = None) -> None:
        self.docs = list(docs or [])

    def insert_many(self, docs: list[dict[str, Any]]) -> None:
        self.docs.extend(dict(d) for d in docs)

    def delete_many(self, flt: dict[str, Any]) -> SimpleNamespace:
        def matches(doc: dict[str, Any]) -> bool:
            for key, want in flt.items():
                if isinstance(want, dict):
                    if doc.get(key) == want["$ne"]:
                        return False
                elif doc.get(key) != want:
                    return False
            return True

        keep = [d for d in self.docs if not matches(d)]
        removed = len(self.docs) - len(keep)
        self.docs = keep
        return SimpleNamespace(deleted_count=removed)


def _load(name: str, monkeypatch: pytest.MonkeyPatch) -> types.ModuleType:
    stub = types.ModuleType("rag_mongo.embeddings")
    stub.embed_batch = lambda texts: [[0.0] for _ in texts]  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "rag_mongo.embeddings", stub)
    spec = importlib.util.spec_from_file_location(f"_reg1603_{name}", SCRIPTS / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def rag(monkeypatch: pytest.MonkeyPatch) -> tuple[types.ModuleType, _Collection]:
    module = _load("ingest_repo", monkeypatch)
    col = _Collection([{"text": "old", "source": "old.py"}])
    monkeypatch.setattr(module, "get_collection", lambda: col)
    monkeypatch.setattr(module, "tracked_files", lambda: ["a.py", "b.py"])
    monkeypatch.setattr(module, "chunk_text", lambda text: [text])
    monkeypatch.setattr(module, "EMBED_BATCH_SIZE", 1)
    return module, col


class _Reader:
    """Stands in for ``open(path, encoding=...)`` inside the script module."""

    def __init__(self, path: str, *args: object, **kwargs: object) -> None:
        self.path = path

    def __enter__(self) -> _Reader:
        return self

    def __exit__(self, *exc: object) -> bool:
        return False

    def read(self) -> str:
        return f"new:{self.path}"


def test_rag_rebuild_replaces_the_index_only_after_every_batch(rag) -> None:
    module, col = rag
    module.open = _Reader  # type: ignore[attr-defined]  # module global shadows the builtin
    module.main()
    assert sorted(d["text"] for d in col.docs) == ["new:a.py", "new:b.py"]
    assert len({d["run_id"] for d in col.docs}) == 1


def test_rag_rebuild_that_fails_keeps_the_previous_index(rag, monkeypatch) -> None:
    module, col = rag
    calls = {"n": 0}

    def embed(texts: list[str]) -> list[list[float]]:
        calls["n"] += 1
        if calls["n"] == 2:
            raise RuntimeError("embedding model crashed")
        return [[0.0] for _ in texts]

    monkeypatch.setattr(module, "embed_batch", embed)
    module.open = _Reader  # type: ignore[attr-defined]
    with pytest.raises(RuntimeError, match="crashed"):
        module.main()
    assert col.docs == [{"text": "old", "source": "old.py"}]


def test_kg_rebuild_deletes_only_what_this_run_did_not_write(monkeypatch) -> None:
    module = _load("ingest_kg_repo", monkeypatch)
    nodes = _Collection([{"name": "stale"}])
    edges = _Collection([{"subject": "stale"}])
    monkeypatch.setattr(module, "get_nodes_collection", lambda: nodes)
    monkeypatch.setattr(module, "get_edges_collection", lambda: edges)
    monkeypatch.setattr(module, "tracked_files", lambda: ["a.py"])

    def ingest_one(path: str, run_id: str | None = None) -> tuple[str, dict]:
        # Before the run finishes, the previous graph is still there.
        assert [n["name"] for n in nodes.docs] == ["stale"]
        nodes.docs.append({"name": "fresh", "run_id": run_id})
        edges.docs.append({"subject": "fresh", "run_id": run_id})
        return path, {"triples_extracted": 1, "nodes_upserted": 1, "edges_upserted": 1}

    monkeypatch.setattr(module, "ingest_one", ingest_one)
    module.main()
    assert [n["name"] for n in nodes.docs] == ["fresh"]
    assert [e["subject"] for e in edges.docs] == ["fresh"]


def test_assemble_stamps_the_run_id_on_nodes_and_edges() -> None:
    nodes_col, edges_col = MagicMock(), MagicMock()
    with (
        patch("kg.assemble.get_nodes_collection", return_value=nodes_col),
        patch("kg.assemble.get_edges_collection", return_value=edges_col),
        patch("kg.assemble.resolve_entities", return_value={}),
    ):
        assemble([{"subject": "X", "predicate": "p", "object": "Y"}], run_id="r1")
    for call in [*nodes_col.update_one.call_args_list, *edges_col.update_one.call_args_list]:
        assert call.args[1]["$set"] == {"run_id": "r1"}
