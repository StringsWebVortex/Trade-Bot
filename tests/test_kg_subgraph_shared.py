"""REG-1717: review.retrieval.graph and kg.query.subgraph are one implementation.

The bounded-subgraph edge query used to be copied into both modules (audit
DOC-015), so a fix to one (for example the empty-match behaviour) could miss
the other. These tests pin that review.retrieval.graph delegates to
kg.query.subgraph and that both give the same result and the same Mongo query.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from kg.query import subgraph
from review.retrieval import graph


def test_graph_delegates_to_kg_subgraph():
    sentinel = [{"subject": "S", "predicate": "p", "object": "O"}]
    with patch("kg.query.subgraph", return_value=sentinel) as shared:
        assert graph(["S"], limit=3) is sentinel
    shared.assert_called_once_with(["S"], 3)


@pytest.mark.parametrize("names", [[], ["Alice", "Bob"]])
def test_graph_and_subgraph_issue_the_same_query(names):
    results = []
    calls = []
    for fn in (subgraph, graph):
        edges_col = MagicMock()
        edges_col.find.return_value.limit.return_value = [{"subject": "Alice"}]
        with patch("kg.query.get_edges_collection", return_value=edges_col):
            results.append(fn(names, limit=7))
        limit_calls = edges_col.find.return_value.limit.call_args_list
        calls.append((edges_col.find.call_args_list, limit_calls))
    assert results[0] == results[1]
    assert calls[0] == calls[1]
