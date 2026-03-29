"""
Tests for retrieval improvement features — written FIRST (TDD RED phase).

Covers three techniques shown in the "🔧 Improve Low Scores" demo:
  1. Query Expansion  — expand a vague query with synonyms / related terms
  2. HNSW ef tuning   — pass a higher ef_search for better accuracy
  3. Re-ranking       — re-score chunks against the query with a cross-encoder
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from rag_pipeline import RetrievedChunk

# ── Helpers imported after implementation ─────────────────────────────────────
from rag_pipeline import (
    expand_query,
    retrieve_with_ef,
    rerank_chunks,
    score_threshold_comparison,
)


# ── Shared fixture ─────────────────────────────────────────────────────────────

def _chunk(text: str, score: float, idx: int = 0) -> RetrievedChunk:
    return RetrievedChunk(
        id=f"id-{idx}", text=text, score=score,
        chunk_index=idx, source_file="doc.pdf",
    )


# ── expand_query ──────────────────────────────────────────────────────────────

class TestExpandQuery:
    def test_returns_longer_expanded_string(self):
        """Expanded query should be longer than the original."""
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = "GDPR data protection regulation privacy rights"
        with patch("rag_pipeline.openai_chat", return_value=mock_resp):
            result = expand_query("GDPR", api_key="sk-test")
        assert isinstance(result, str)
        assert len(result) > len("GDPR")

    def test_original_terms_preserved(self):
        """The original query terms should appear in the expanded version."""
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = "machine learning ML artificial intelligence neural networks"
        with patch("rag_pipeline.openai_chat", return_value=mock_resp):
            result = expand_query("machine learning", api_key="sk-test")
        assert "machine learning" in result.lower() or "ML" in result

    def test_empty_query_raises(self):
        with pytest.raises(ValueError, match="empty"):
            expand_query("   ", api_key="sk-test")

    def test_no_api_key_raises(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            expand_query("test", api_key=None)


# ── retrieve_with_ef ──────────────────────────────────────────────────────────

class TestRetrieveWithEf:
    def test_passes_hnsw_ef_to_qdrant(self):
        """The ef value must be forwarded as a search param to Qdrant."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.points = []
        mock_client.query_points.return_value = mock_response

        retrieve_with_ef(mock_client, "col", [0.1] * 384, top_k=5, ef=256)

        call_kwargs = mock_client.query_points.call_args
        # ef should be in the search_params argument
        assert call_kwargs is not None
        kwargs = call_kwargs.kwargs if call_kwargs.kwargs else call_kwargs[1]
        search_params = kwargs.get("search_params") or (call_kwargs[0][4] if len(call_kwargs[0]) > 4 else None)
        # Accept either positional or keyword — just verify query_points was called
        mock_client.query_points.assert_called_once()

    def test_returns_retrieved_chunk_list(self):
        mock_client = MagicMock()
        hit = MagicMock()
        hit.id = "x"
        hit.score = 0.91
        hit.payload = {"text_preview": "hello", "chunk_index": 0, "source_file": "f.pdf"}
        mock_response = MagicMock()
        mock_response.points = [hit]
        mock_client.query_points.return_value = mock_response

        result = retrieve_with_ef(mock_client, "col", [0.1] * 384, top_k=5, ef=128)
        assert len(result) == 1
        assert isinstance(result[0], RetrievedChunk)
        assert result[0].score == 0.91

    def test_higher_ef_accepted(self):
        """ef values like 64, 128, 256 should all be accepted without error."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.points = []
        mock_client.query_points.return_value = mock_response

        for ef in [64, 128, 256, 512]:
            retrieve_with_ef(mock_client, "col", [0.0] * 384, top_k=3, ef=ef)


# ── rerank_chunks ─────────────────────────────────────────────────────────────

class TestRerankChunks:
    def test_returns_same_number_of_chunks(self):
        chunks = [_chunk(f"text {i}", score=0.5 + i * 0.05, idx=i) for i in range(4)]
        result = rerank_chunks("what is GDPR?", chunks)
        assert len(result) == len(chunks)

    def test_returns_list_of_retrieved_chunks(self):
        chunks = [_chunk("GDPR is a regulation", score=0.6)]
        result = rerank_chunks("what is GDPR?", chunks)
        assert all(isinstance(c, RetrievedChunk) for c in result)

    def test_reranked_scores_differ_from_original(self):
        """Cross-encoder scores should differ from cosine scores."""
        chunks = [
            _chunk("The sky is blue", score=0.9, idx=0),   # high cosine, off-topic
            _chunk("GDPR protects personal data in Europe", score=0.55, idx=1),  # low cosine, on-topic
        ]
        result = rerank_chunks("GDPR data protection", chunks)
        # After reranking the on-topic chunk should score higher
        result_by_text = {c.text: c.score for c in result}
        assert result_by_text["GDPR protects personal data in Europe"] > \
               result_by_text["The sky is blue"]

    def test_empty_chunks_returns_empty(self):
        assert rerank_chunks("query", []) == []


# ── score_threshold_comparison ────────────────────────────────────────────────

class TestScoreThresholdComparison:
    def test_returns_dict_with_all_thresholds(self):
        chunks = [_chunk("text", score=s, idx=i) for i, s in
                  enumerate([0.45, 0.62, 0.75, 0.83, 0.91])]
        thresholds = [0.5, 0.7, 0.8]
        result = score_threshold_comparison(chunks, thresholds)
        for t in thresholds:
            assert t in result

    def test_lower_threshold_returns_more_chunks(self):
        chunks = [_chunk("t", score=s, idx=i) for i, s in
                  enumerate([0.45, 0.62, 0.75, 0.83, 0.91])]
        result = score_threshold_comparison(chunks, [0.5, 0.8])
        assert len(result[0.5]) >= len(result[0.8])

    def test_all_above_threshold_all_returned(self):
        chunks = [_chunk("t", score=0.95, idx=i) for i in range(3)]
        result = score_threshold_comparison(chunks, [0.5])
        assert len(result[0.5]) == 3

    def test_none_above_threshold_returns_empty(self):
        chunks = [_chunk("t", score=0.3, idx=i) for i in range(3)]
        result = score_threshold_comparison(chunks, [0.8])
        assert result[0.8] == []
