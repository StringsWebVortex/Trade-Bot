"""Reuses the RAG component's Mongo connection settings (same Atlas
cluster/database, separate collections) -- no new infra to provision."""

from pymongo import MongoClient

# One cached client factory and one URI check for the shared cluster: kg/ and
# rag_mongo/ used to carry copy-pasted versions of both (DOC-015), which also
# meant two lru_caches and therefore two MongoClient pools per process.
from rag_mongo.config import MONGODB_DB, MONGODB_URI
from rag_mongo.db import _client_for, require_uri

from .config import KG_EDGES_COLLECTION, KG_NODES_COLLECTION


def _require_uri() -> str:
    # Reads this module's MONGODB_URI at call time, so a patch of
    # kg.db.MONGODB_URI is honoured.
    return require_uri(MONGODB_URI)


def _client() -> MongoClient:
    # lru_cache: one MongoClient per process, which is what PyMongo asks for.
    # Each client owns a connection pool and its own monitoring threads, and
    # nothing here closes them -- building one per call left a pool behind on
    # every call. rag_smoke.py alone calls into this five times, and
    # ingest_repo.py runs for the better part of an hour.
    #
    # The URI check stays outside the cached call: lru_cache does not cache
    # exceptions, so an unset MONGODB_URI keeps raising rather than being
    # remembered as a result.
    return _client_for(_require_uri())


def get_nodes_collection():
    return _client()[MONGODB_DB][KG_NODES_COLLECTION]


def get_edges_collection():
    return _client()[MONGODB_DB][KG_EDGES_COLLECTION]
