"""
Tests for HyDE (Hypothetical Document Embeddings) — TDD RED phase.
embed_query_hyde() must not exist yet when these are first run.
"""
from __future__ import annotations
from unittest.mock import MagicMock, patch
import pytest
from rag_pipeline import embed_query_hyde


class TestEmbedQueryHyde:
    def _mock_chat(self, text: str):
        resp = MagicMock()
        resp.choices = [MagicMock()]
        resp.choices[0].message.content = text
        return resp

    def _mock_encoder(self, dim: int = 384):
        import numpy as np
        model = MagicMock()
        model.encode.return_value = np.array([[0.1] * dim])
        return model

    def test_returns_list_of_floats(self):
        with (
            patch("rag_pipeline.openai_chat", return_value=self._mock_chat("A long hypothetical answer.")),
            patch("rag_pipeline._load_encoder", return_value=(self._mock_encoder(), "mock")),
        ):
            vec, hyp = embed_query_hyde("What is GDPR?", openai_key="sk-test")
        assert isinstance(vec, list)
        assert len(vec) == 384
        assert all(isinstance(v, float) for v in vec)

    def test_also_returns_hypothetical_text(self):
        """embed_query_hyde should return (vector, hypothetical_text) tuple."""
        with (
            patch("rag_pipeline.openai_chat", return_value=self._mock_chat("GDPR is a regulation...")),
            patch("rag_pipeline._load_encoder", return_value=(self._mock_encoder(), "mock")),
        ):
            result = embed_query_hyde("What is GDPR?", openai_key="sk-test")
        # Must be a tuple: (vector: list[float], hypothesis: str)
        assert isinstance(result, tuple)
        vec, hyp = result
        assert isinstance(vec, list)
        assert isinstance(hyp, str)
        assert len(hyp) > 0

    def test_empty_query_raises(self):
        with pytest.raises(ValueError, match="empty"):
            embed_query_hyde("  ", openai_key="sk-test")

    def test_no_openai_key_raises(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            embed_query_hyde("What is RAG?", openai_key=None)

    def test_hypothetical_doc_embedded_not_query(self):
        """The encode call must receive the hypothetical doc, not the raw query."""
        mock_model = self._mock_encoder()
        with (
            patch("rag_pipeline.openai_chat",
                  return_value=self._mock_chat("Hypothetical answer about GDPR penalties.")),
            patch("rag_pipeline._load_encoder", return_value=(mock_model, "mock")),
        ):
            embed_query_hyde("short q", openai_key="sk-test")
        # The text passed to encode should NOT be the short query
        encoded_text = mock_model.encode.call_args[0][0][0]
        assert encoded_text != "short q"
        assert "Hypothetical" in encoded_text or len(encoded_text) > len("short q")
