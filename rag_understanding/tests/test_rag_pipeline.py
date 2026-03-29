"""
Tests for rag_pipeline.py — written FIRST (TDD RED phase).
Uses mocks throughout — no real Qdrant or OpenAI calls.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

# ── These imports fail until rag_pipeline.py exists (RED) ────────────────────
from rag_pipeline import (
    RetrievedChunk,
    RAGResult,
    embed_query,
    retrieve_chunks,
    format_context,
    generate_answer,
    run_rag,
    run_no_rag,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

def make_chunk(text: str, score: float = 0.9, idx: int = 0) -> RetrievedChunk:
    return RetrievedChunk(
        id=f"id-{idx}",
        text=text,
        score=score,
        chunk_index=idx,
        source_file="test.pdf",
    )


# ── embed_query ───────────────────────────────────────────────────────────────

class TestEmbedQuery:
    def test_returns_list_of_floats(self):
        with patch("rag_pipeline._load_encoder") as mock_enc:
            import numpy as np
            mock_model = MagicMock()
            mock_model.encode.return_value = np.array([[0.1] * 384])
            mock_enc.return_value = (mock_model, "mock-model")
            result = embed_query("hello world")
        assert isinstance(result, list)
        assert len(result) == 384
        assert all(isinstance(v, float) for v in result)

    def test_empty_query_raises(self):
        with pytest.raises(ValueError, match="empty"):
            embed_query("   ")


# ── retrieve_chunks ───────────────────────────────────────────────────────────

class TestRetrieveChunks:
    def test_returns_list_of_retrieved_chunks(self):
        mock_client = MagicMock()
        mock_hit = MagicMock()
        mock_hit.id = "abc"
        mock_hit.score = 0.85
        mock_hit.payload = {"text_preview": "some text", "chunk_index": 0, "source_file": "test.pdf"}
        mock_response = MagicMock()
        mock_response.points = [mock_hit]
        mock_client.query_points.return_value = mock_response

        result = retrieve_chunks(mock_client, "col", [0.1] * 384, top_k=3)
        assert len(result) == 1
        assert isinstance(result[0], RetrievedChunk)
        assert result[0].score == 0.85
        assert result[0].text == "some text"

    def test_filters_by_score_threshold(self):
        mock_client = MagicMock()
        low = MagicMock()
        low.id = "low"
        low.score = 0.3
        low.payload = {"text_preview": "low", "chunk_index": 0, "source_file": "f.pdf"}
        high = MagicMock()
        high.id = "high"
        high.score = 0.9
        high.payload = {"text_preview": "high", "chunk_index": 1, "source_file": "f.pdf"}
        mock_response = MagicMock()
        mock_response.points = [high, low]
        mock_client.query_points.return_value = mock_response

        result = retrieve_chunks(mock_client, "col", [0.1] * 384, top_k=5, score_threshold=0.5)
        assert len(result) == 1
        assert result[0].text == "high"

    def test_returns_empty_list_when_no_hits(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.points = []
        mock_client.query_points.return_value = mock_response
        result = retrieve_chunks(mock_client, "col", [0.1] * 384, top_k=3)
        assert result == []


# ── format_context ────────────────────────────────────────────────────────────

class TestFormatContext:
    def test_combines_chunks_with_separators(self):
        chunks = [make_chunk("First chunk.", score=0.9, idx=0),
                  make_chunk("Second chunk.", score=0.8, idx=1)]
        ctx = format_context(chunks)
        assert "First chunk." in ctx
        assert "Second chunk." in ctx
        assert "[1]" in ctx
        assert "[2]" in ctx

    def test_empty_chunks_returns_empty_string(self):
        assert format_context([]) == ""

    def test_includes_source_info(self):
        chunks = [make_chunk("Text about AI.", idx=0)]
        ctx = format_context(chunks)
        assert "test.pdf" in ctx


# ── generate_answer ───────────────────────────────────────────────────────────

class TestGenerateAnswer:
    def _make_openai_response(self, content: str):
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = content
        mock_resp.usage.prompt_tokens = 100
        mock_resp.usage.completion_tokens = 50
        return mock_resp

    def test_stuff_strategy_returns_answer(self):
        with patch("rag_pipeline.openai_chat") as mock_chat:
            mock_chat.return_value = self._make_openai_response("Answer here.")
            result = generate_answer(
                query="What is RAG?",
                context="RAG stands for Retrieval Augmented Generation.",
                strategy="stuff",
                api_key="sk-test",
            )
        assert result["answer"] == "Answer here."
        assert result["strategy"] == "stuff"
        assert result["prompt_tokens"] == 100

    def test_refine_strategy_returns_answer(self):
        with patch("rag_pipeline.openai_chat") as mock_chat:
            mock_chat.return_value = self._make_openai_response("Refined answer.")
            result = generate_answer(
                query="What is RAG?",
                context="Context chunk.",
                strategy="refine",
                api_key="sk-test",
            )
        assert result["answer"] == "Refined answer."
        assert result["strategy"] == "refine"

    def test_unknown_strategy_raises(self):
        with pytest.raises(ValueError, match="strategy"):
            generate_answer("q", "ctx", strategy="invalid_strategy")

    def test_no_api_key_raises(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            generate_answer("q", "ctx", api_key=None)


# ── run_no_rag ────────────────────────────────────────────────────────────────

class TestRunNoRag:
    def test_returns_string_answer(self):
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = "Direct LLM answer."
        with patch("rag_pipeline.openai_chat", return_value=mock_resp):
            result = run_no_rag("What is the capital of France?", api_key="sk-test")
        assert result == "Direct LLM answer."

    def test_no_api_key_raises(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            run_no_rag("q", api_key=None)


# ── run_rag (full pipeline, fully mocked) ────────────────────────────────────

class TestRunRag:
    def test_full_pipeline_returns_rag_result(self):
        import numpy as np
        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([[0.1] * 384])

        mock_hit = MagicMock()
        mock_hit.id = "abc"
        mock_hit.score = 0.88
        mock_hit.payload = {"text_preview": "RAG context text", "chunk_index": 0, "source_file": "doc.pdf"}

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.points = [mock_hit]
        mock_client.query_points.return_value = mock_response

        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = "RAG answer."
        mock_resp.usage.prompt_tokens = 80
        mock_resp.usage.completion_tokens = 30

        with (
            patch("rag_pipeline._load_encoder", return_value=(mock_model, "mock")),
            patch("rag_pipeline.QdrantClient", return_value=mock_client),
            patch("rag_pipeline.openai_chat", return_value=mock_resp),
        ):
            result = run_rag(
                query="What is RAG?",
                qdrant_url="https://example:6333",
                api_key="qdrant-key",
                openai_api_key="sk-test",
                collection="col",
                top_k=3,
            )

        assert isinstance(result, RAGResult)
        assert result.answer == "RAG answer."
        assert len(result.chunks) == 1
        assert result.chunks[0].score == 0.88
        assert result.query == "What is RAG?"

    def test_no_chunks_returns_result_with_flag(self):
        import numpy as np
        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([[0.1] * 384])
        mock_client = MagicMock()
        mock_empty_response = MagicMock()
        mock_empty_response.points = []
        mock_client.query_points.return_value = mock_empty_response

        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = "No context answer."
        mock_resp.usage.prompt_tokens = 20
        mock_resp.usage.completion_tokens = 10

        with (
            patch("rag_pipeline._load_encoder", return_value=(mock_model, "mock")),
            patch("rag_pipeline.QdrantClient", return_value=mock_client),
            patch("rag_pipeline.openai_chat", return_value=mock_resp),
        ):
            result = run_rag(
                query="Something not in docs",
                qdrant_url="https://example:6333",
                api_key=None,
                openai_api_key="sk-test",
                collection="col",
                top_k=3,
            )

        assert isinstance(result, RAGResult)
        assert result.retrieval_empty is True
