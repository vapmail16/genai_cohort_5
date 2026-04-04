"""
Tests for metadata-filtered retrieval — TDD RED phase.
retrieve_with_filter() must not exist yet when these are first run.
"""
from __future__ import annotations
from unittest.mock import MagicMock
import pytest
from rag_pipeline import RetrievedChunk, retrieve_with_filter


def _mock_hit(source: str, score: float = 0.85, idx: int = 0):
    h = MagicMock()
    h.id = f"id-{idx}"
    h.score = score
    h.payload = {"text_preview": f"text from {source}", "chunk_index": idx,
                 "source_file": source}
    return h


def _mock_client(hits: list):
    client = MagicMock()
    resp = MagicMock()
    resp.points = hits
    client.query_points.return_value = resp
    return client


class TestRetrieveWithFilter:
    def test_returns_list_of_retrieved_chunks(self):
        client = _mock_client([_mock_hit("policy.pdf")])
        result = retrieve_with_filter(
            client, "col", [0.1] * 384, top_k=5,
            filter_by={"source_file": "policy.pdf"},
        )
        assert isinstance(result, list)
        assert all(isinstance(c, RetrievedChunk) for c in result)

    def test_filter_is_passed_to_qdrant(self):
        """Qdrant query_points must be called with a filter when filter_by is given."""
        client = _mock_client([])
        retrieve_with_filter(
            client, "col", [0.1] * 384, top_k=5,
            filter_by={"source_file": "policy.pdf"},
        )
        call_kwargs = client.query_points.call_args
        # query_filter keyword must be present
        kwargs = call_kwargs.kwargs if call_kwargs.kwargs else {}
        assert "query_filter" in kwargs or "filter" in str(call_kwargs)

    def test_empty_filter_behaves_like_normal_retrieve(self):
        """filter_by={} should still call query_points without crashing."""
        client = _mock_client([_mock_hit("a.pdf")])
        result = retrieve_with_filter(
            client, "col", [0.1] * 384, top_k=5,
            filter_by={},
        )
        assert isinstance(result, list)

    def test_none_filter_behaves_like_normal_retrieve(self):
        client = _mock_client([_mock_hit("b.pdf")])
        result = retrieve_with_filter(
            client, "col", [0.1] * 384, top_k=5,
            filter_by=None,
        )
        assert isinstance(result, list)

    def test_returns_chunks_with_correct_source(self):
        client = _mock_client([_mock_hit("gdpr.pdf", score=0.9)])
        result = retrieve_with_filter(
            client, "col", [0.1] * 384, top_k=5,
            filter_by={"source_file": "gdpr.pdf"},
        )
        assert result[0].source_file == "gdpr.pdf"

    def test_returns_empty_when_no_hits(self):
        client = _mock_client([])
        result = retrieve_with_filter(
            client, "col", [0.1] * 384, top_k=5,
            filter_by={"source_file": "missing.pdf"},
        )
        assert result == []

    def test_multiple_filter_fields_accepted(self):
        """Should accept filter on any payload field, not just source_file."""
        client = _mock_client([_mock_hit("report.pdf")])
        result = retrieve_with_filter(
            client, "col", [0.1] * 384, top_k=5,
            filter_by={"source_file": "report.pdf", "chunk_index": 0},
        )
        assert isinstance(result, list)
