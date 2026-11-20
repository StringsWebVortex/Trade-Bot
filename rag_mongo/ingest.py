from .db import get_collection
from .embeddings import embed_batch


def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    chunks, i = [], 0
    while i < len(text):
        chunks.append(text[i : i + size])
        i += size - overlap
    return chunks


def ingest_text(text: str, source: str) -> int:
    chunks = chunk_text(text)
    vectors = embed_batch(chunks)
    docs = [
        {"text": c, "embedding": v, "source": source} for c, v in zip(chunks, vectors, strict=True)
    ]
    col = get_collection()
    # Re-ingesting a source replaces its chunks. Without this delete every run
    # appended duplicates, which skewed vector and hybrid retrieval. The delete
    # runs after embedding, so a failed embed leaves the previous chunks intact.
    col.delete_many({"source": source})
    if docs:
        col.insert_many(docs)
    return len(docs)
