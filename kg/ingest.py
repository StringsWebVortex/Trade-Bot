from .assemble import assemble
from .extract import extract_triples


def ingest_document(text: str, source: str, run_id: str | None = None) -> dict:
    triples = extract_triples(text, source)
    stats = assemble(triples, run_id=run_id)
    stats["triples_extracted"] = len(triples)
    return stats
