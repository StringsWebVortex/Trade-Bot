#!/usr/bin/env python3
"""Cloud-only retrieval step for PR review (Component 5).

Designed to run INSIDE a GitHub Actions runner -- never locally, per this
project's rule that review/test for this component happens exclusively in
GitHub's cloud service. Produces a bounded context.json that the
claude-review job attaches to the review prompt, so review is grounded in
the project's RAG + knowledge-graph store, not just the raw diff.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess

from review.config import REVIEW_MAX_CONTEXT_ITEMS
from review.retrieval import graph, hybrid


def _diff_text(base: str, head: str) -> str:
    for ref in (base, head):
        # A ref starting with "-" would be parsed as a git option.
        if not ref or ref.startswith("-"):
            raise ValueError(f"invalid git ref: {ref!r}")
        verified = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if verified.returncode != 0:
            raise ValueError(f"not a commit: {ref!r}")
    out = subprocess.run(
        ["git", "diff", f"{base}...{head}", "--"], capture_output=True, text=True, check=True
    )
    return out.stdout


def _candidate_terms(diff: str) -> list[str]:
    # Bounded: cap term count so a huge diff can't blow up the retrieval query.
    names = sorted(set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", diff)))
    return names[:50]


def build_context(base: str, head: str) -> dict:
    """Retrieve grounding context, degrading to an empty set on failure.

    The review this feeds is advisory and never gates a merge, so an
    unreachable Atlas cluster must not either. Returning the empty context
    means the reviewer reads the diff alone -- a worse review, not a red
    check on every open pull request.
    """
    try:
        diff = _diff_text(base, head)
    except (ValueError, subprocess.CalledProcessError, OSError) as exc:
        print(f"warning: cannot diff {base}...{head}, reviewing without context: {exc}")
        return {"related_documents": [], "related_facts": [], "retrieval_error": str(exc)}
    terms = _candidate_terms(diff)
    query_text = " ".join(terms[:20]) or "code change"

    try:
        related_docs = hybrid(query_text, top_k=REVIEW_MAX_CONTEXT_ITEMS)
        related_edges = graph(terms, limit=REVIEW_MAX_CONTEXT_ITEMS)
    except Exception as exc:  # noqa: BLE001 - any retrieval fault degrades the same way
        print(f"warning: retrieval unavailable, reviewing the diff alone: {exc}")
        return {"related_documents": [], "related_facts": [], "retrieval_error": str(exc)}

    return {
        "related_documents": [
            {"source": d.get("source"), "excerpt": d["text"][:300]} for d in related_docs
        ],
        "related_facts": [
            f"({e['subject']}) -[{e['predicate']}]-> ({e['object']})" for e in related_edges
        ],
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True)
    p.add_argument("--head", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    ctx = build_context(args.base, args.head)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(ctx, f, indent=2)
    print(
        f"Wrote {args.out}: {len(ctx['related_documents'])} docs, {len(ctx['related_facts'])} facts"
    )
