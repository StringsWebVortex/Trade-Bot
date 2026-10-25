"""Query stage: pull a BOUNDED subgraph around entities mentioned in the
question, then reason over just those triples. Never serialize the whole
graph -- that would make context grow unboundedly as the graph scales, the
opposite of what this component exists to prevent."""

from __future__ import annotations

import re

from common.claude_cli import run_claude

from .config import KG_MAX_SUBGRAPH_TRIPLES, KG_QUERY_MODEL
from .db import get_edges_collection, get_nodes_collection


def _candidate_names(question: str) -> list[str]:
    words = {
        w for w in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", question) if w.lower() not in _STOPWORDS
    }
    if not words:
        return []
    nodes_col = get_nodes_collection()
    hits = [d["name"] for d in nodes_col.find({"name": {"$in": list(words)}}, {"name": 1})]
    if hits:
        return hits
    pattern = "|".join(re.escape(w) for w in words)
    cursor = nodes_col.find({"name": {"$regex": pattern, "$options": "i"}}, {"name": 1}).limit(10)
    return [d["name"] for d in cursor]


_STOPWORDS = frozenset(
    {"the", "and", "what", "who", "which", "where", "when", "how", "why", "are", "was",
     "were", "does", "did", "for", "with", "about", "from", "that", "this", "there",
     "their", "you", "your", "have", "has", "had", "can", "tell", "show", "list", "give"}
)


def _subgraph(names: list[str], limit: int) -> list[dict]:
    edges_col = get_edges_collection()
    if not names:
        # No matching entity means no grounding. Returning arbitrary edges
        # would present unrelated facts to the model as evidence.
        return []
    cursor = edges_col.find(
        {"$or": [{"subject": {"$in": names}}, {"object": {"$in": names}}]},
        {"_id": 0},
    ).limit(limit)
    return list(cursor)


def query(question: str) -> dict:
    names = _candidate_names(question)
    triples = _subgraph(names, KG_MAX_SUBGRAPH_TRIPLES)

    serialized = "\n".join(
        f"({t['subject']}) -[{t['predicate']}]-> ({t['object']}) "
        f"[sources: {', '.join(t.get('sources', []))}]"
        for t in triples
    )
    prompt = (
        "Answer the question using ONLY these graph triples. Cite the specific "
        "edge(s) you used.\n\n"
        f"TRIPLES:\n{serialized or '(none found)'}\n\nQUESTION: {question}"
    )
    out = run_claude(prompt, model=KG_QUERY_MODEL, max_turns=1)
    return {"answer": out["result"], "triples_used": len(triples)}
