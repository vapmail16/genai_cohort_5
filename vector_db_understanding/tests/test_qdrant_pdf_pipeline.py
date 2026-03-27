"""Tests for PDF extraction and Qdrant ingest (mocked)."""

from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest

from qdrant_pdf_pipeline import (
    delete_qdrant_collection,
    embed_texts,
    extract_text_from_pdf,
    ingest_pdf_to_qdrant,
    summarize_vector,
)


def test_summarize_vector():
    s = summarize_vector([3.0, 4.0], head=2)
    assert s["head"] == [3.0, 4.0]
    assert abs(s["l2_norm"] - 5.0) < 1e-9
    assert s["length"] == 2


def test_extract_text_from_pdf_mocked():
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Hello cohort"
    mock_reader = MagicMock()
    mock_reader.pages = [mock_page]

    with patch("qdrant_pdf_pipeline.PdfReader", return_value=mock_reader):
        out = extract_text_from_pdf(BytesIO(b"%PDF"))
    assert "Hello cohort" in out


@pytest.mark.slow
def test_embed_texts_returns_consistent_dim():
    """Loads sentence-transformers; run with: pytest -m slow."""
    vecs, dim, name = embed_texts(["hello world", "vector databases"])
    assert len(vecs) == 2
    assert len(vecs[0]) == dim
    assert dim > 0
    assert "MiniLM" in name or "sentence" in name.lower()


def test_ingest_pdf_to_qdrant_mocked():
    fake_vectors = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    mock_client = MagicMock()
    mock_client.get_collections.return_value = MagicMock(collections=[])

    with (
        patch("qdrant_pdf_pipeline.extract_text_from_pdf", return_value="dummy"),
        patch("qdrant_pdf_pipeline.chunk_text", return_value=["chunk one", "chunk two"]),
        patch("qdrant_pdf_pipeline.embed_texts", return_value=(fake_vectors, 3, "mock-model")),
        patch("qdrant_pdf_pipeline.QdrantClient", return_value=mock_client),
    ):
        result = ingest_pdf_to_qdrant(
            BytesIO(b"x"),
            qdrant_url="http://localhost:6333",
            collection_name="test_coll",
            chunk_size=100,
            overlap=10,
        )

    assert result.points_upserted == 2
    assert result.vector_dim == 3
    assert len(result.points_preview) == 2
    assert "vector_first_k" in result.points_preview[0]
    mock_client.upsert.assert_called_once()


def test_delete_qdrant_collection_removes_when_exists():
    coll = MagicMock()
    coll.name = "demo"
    mock_client = MagicMock()
    mock_client.get_collections.return_value = MagicMock(collections=[coll])

    with patch("qdrant_pdf_pipeline.QdrantClient", return_value=mock_client):
        msg = delete_qdrant_collection(
            qdrant_url="https://example:6333",
            api_key="k",
            collection_name="demo",
        )

    assert "Deleted" in msg
    mock_client.delete_collection.assert_called_once_with(collection_name="demo")


def test_delete_qdrant_collection_noop_when_missing():
    mock_client = MagicMock()
    mock_client.get_collections.return_value = MagicMock(collections=[])

    with patch("qdrant_pdf_pipeline.QdrantClient", return_value=mock_client):
        msg = delete_qdrant_collection(
            qdrant_url="https://example:6333",
            api_key=None,
            collection_name="demo",
        )

    assert "does not exist" in msg
    mock_client.delete_collection.assert_not_called()
