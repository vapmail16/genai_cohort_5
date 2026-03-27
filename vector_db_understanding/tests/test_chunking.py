"""Tests for chunk_text (TDD)."""

import pytest

from qdrant_pdf_pipeline import chunk_text


def test_chunk_text_empty():
    assert chunk_text("") == []
    assert chunk_text("   ") == []


def test_chunk_text_invalid_chunk_size():
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=0)


def test_chunk_text_single_chunk():
    assert chunk_text("hello world", chunk_size=100) == ["hello world"]


def test_chunk_text_overlap_produces_multiple_chunks():
    text = "abcdefghijklmnopqrst"
    chunks = chunk_text(text, chunk_size=5, overlap=2)
    assert len(chunks) >= 2
    assert all(len(c) <= 5 for c in chunks)


def test_chunk_text_overlap_capped():
    t = "x" * 20
    chunks = chunk_text(t, chunk_size=10, overlap=9)
    assert len(chunks) >= 2
