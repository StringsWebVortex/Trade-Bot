"""One MongoClient per process, not one per call.

Both db modules built a fresh MongoClient every time a collection was
asked for. Each client owns a connection pool and its own monitoring
threads, and nothing closes them, so every call leaked a pool. There are
23 call sites; rag_smoke.py alone reaches this five times in one run, and
ingest_repo.py runs for the better part of an hour.

MongoClient is not constructed here -- these tests patch it. Building a real
one would open sockets, and the network guard in conftest blocks that.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

import kg.db
import rag_mongo.db


def test_kg_reuses_one_client_across_both_collections() -> None:
    with (
        patch.object(rag_mongo.db, "MongoClient", return_value=MagicMock()) as mock_client,
        patch.object(kg.db, "MONGODB_URI", "mongodb://stub"),
    ):
        kg.db.get_nodes_collection()
        kg.db.get_edges_collection()
        kg.db.get_nodes_collection()

    mock_client.assert_called_once()


def test_rag_reuses_one_client_across_calls() -> None:
    with (
        patch.object(rag_mongo.db, "MongoClient", return_value=MagicMock()) as mock_client,
        patch.object(rag_mongo.db, "MONGODB_URI", "mongodb://stub"),
    ):
        rag_mongo.db.get_collection()
        rag_mongo.db.get_collection()

    mock_client.assert_called_once()


def test_kg_and_rag_share_one_client_for_the_shared_cluster() -> None:
    """REG-1702 (DOC-015): kg/ and rag_mongo/ point at the same cluster and URI.

    They used to carry copy-pasted ``_client_for`` factories, each with its own
    lru_cache, so a process using both (review/retrieval.py, rag_smoke.py) held
    two MongoClient pools for one cluster. kg.db now reuses rag_mongo.db's.
    """
    assert kg.db._client_for is rag_mongo.db._client_for
    with (
        patch.object(rag_mongo.db, "MongoClient", return_value=MagicMock()) as mock_client,
        patch.object(rag_mongo.db, "MONGODB_URI", "mongodb://stub"),
        patch.object(kg.db, "MONGODB_URI", "mongodb://stub"),
    ):
        rag_mongo.db.get_collection()
        kg.db.get_nodes_collection()
        kg.db.get_edges_collection()

    mock_client.assert_called_once()


def test_kg_and_rag_raise_the_same_missing_uri_error() -> None:
    """One URI check, not two copies of its message that can drift apart."""
    with pytest.raises(RuntimeError) as rag_error:
        rag_mongo.db.require_uri("")
    with patch.object(kg.db, "MONGODB_URI", None), pytest.raises(RuntimeError) as kg_error:
        kg.db._require_uri()
    assert str(kg_error.value) == str(rag_error.value)


def test_missing_uri_keeps_raising_rather_than_being_cached() -> None:
    """lru_cache does not cache exceptions, and the guard sits outside it.

    A URI that is unset at import time must fail on every call, not fail once
    and then return a remembered result.
    """
    with patch.object(rag_mongo.db, "MONGODB_URI", ""):
        for _ in range(2):
            with pytest.raises(RuntimeError, match="MONGODB_URI not set"):
                rag_mongo.db.get_collection()

    with patch.object(kg.db, "MONGODB_URI", ""):
        for _ in range(2):
            with pytest.raises(RuntimeError, match="MONGODB_URI not set"):
                kg.db.get_nodes_collection()
