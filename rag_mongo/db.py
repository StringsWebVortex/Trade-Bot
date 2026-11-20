from functools import lru_cache

import certifi
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

from .config import EMBEDDING_DIM, MONGODB_COLLECTION, MONGODB_DB, MONGODB_URI, VECTOR_INDEX_NAME


def require_uri(uri: str | None) -> str:
    """Return *uri*, or raise the one actionable error when it is unset.

    Shared with kg.db (same cluster, same setting) so both packages fail with
    the same message instead of two copies drifting apart.
    """
    if not uri:
        raise RuntimeError(
            "MONGODB_URI not set. Locally: copy .env.example to .env and fill it in. "
            "In a Claude Code cloud session: set it in the environment's variables."
        )
    return uri


@lru_cache(maxsize=1)
def _client_for(uri: str) -> MongoClient:
    # Atlas serves a chain rooted in a CA that a bare GitHub runner's system
    # trust store does not carry, which surfaces as an SSL handshake failure
    # rather than anything that names a certificate. Pin pymongo to certifi's
    # bundle so verification does not depend on the host image. Ignored for a
    # non-TLS URI, so local mongodb:// runs are unaffected.
    return MongoClient(uri, tlsCAFile=certifi.where())


def get_collection():
    # lru_cache: one MongoClient per process, which is what PyMongo asks for.
    # Each client owns a connection pool and its own monitoring threads, and
    # nothing here closes them -- building one per call left a pool behind on
    # every call. rag_smoke.py alone calls into this five times, and
    # ingest_repo.py runs for the better part of an hour.
    #
    # The URI check stays outside the cached call: lru_cache does not cache
    # exceptions, so an unset MONGODB_URI keeps raising rather than being
    # remembered as a result.
    #
    # kg.db reuses this same cached factory, so a process that touches both
    # the RAG and the knowledge-graph collections (review/retrieval.py,
    # scripts/rag_smoke.py) holds one pool for the shared cluster, not two.
    return _client_for(require_uri(MONGODB_URI))[MONGODB_DB][MONGODB_COLLECTION]


def ensure_vector_index() -> None:
    """Idempotent Atlas Vector Search index creation (Atlas M0+ only)."""
    col = get_collection()
    existing = {ix["name"] for ix in col.list_search_indexes()}
    if VECTOR_INDEX_NAME in existing:
        return
    definition = {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": EMBEDDING_DIM,
                "similarity": "cosine",
            }
        ]
    }
    model = SearchIndexModel(definition=definition, name=VECTOR_INDEX_NAME, type="vectorSearch")
    col.create_search_index(model=model)


def ensure_fulltext_index(name: str = "fulltext_index") -> None:
    """Idempotent Atlas full-text Search index -- backs the 'full-text' and
    'hybrid' retrieval patterns in review/retrieval.py (Atlas M0+ only)."""
    col = get_collection()
    existing = {ix["name"] for ix in col.list_search_indexes()}
    if name in existing:
        return
    definition = {"mappings": {"dynamic": False, "fields": {"text": {"type": "string"}}}}
    model = SearchIndexModel(definition=definition, name=name, type="search")
    col.create_search_index(model=model)
