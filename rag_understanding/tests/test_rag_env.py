"""
Tests for rag_env.py — written FIRST (TDD RED phase).
All tests here define what the env loader must do before any code is written.
"""

import os
import pytest

# ── These imports will fail until rag_env.py is implemented (RED) ─────────────
from rag_env import (
    load_rag_env,
    get_qdrant_url,
    get_qdrant_api_key,
    get_qdrant_collection,
    get_openai_api_key,
    resolve_api_key,
)


class TestLoadRagEnv:
    def test_load_is_idempotent(self):
        """Calling load_rag_env() multiple times must not raise."""
        load_rag_env()
        load_rag_env()  # second call — should be a no-op

    def test_returns_none(self):
        assert load_rag_env() is None


class TestGetQdrantUrl:
    def test_returns_string(self, monkeypatch):
        monkeypatch.setenv("QDRANT_URL", "https://example:6333")
        assert get_qdrant_url() == "https://example:6333"

    def test_returns_empty_string_when_unset(self, monkeypatch):
        monkeypatch.delenv("QDRANT_URL", raising=False)
        assert get_qdrant_url() == ""

    def test_strips_whitespace(self, monkeypatch):
        monkeypatch.setenv("QDRANT_URL", "  https://example:6333  ")
        assert get_qdrant_url() == "https://example:6333"


class TestGetQdrantApiKey:
    def test_returns_key_when_set(self, monkeypatch):
        monkeypatch.setenv("QDRANT_API_KEY", "mykey")
        assert get_qdrant_api_key() == "mykey"

    def test_returns_none_when_unset(self, monkeypatch):
        monkeypatch.delenv("QDRANT_API_KEY", raising=False)
        assert get_qdrant_api_key() is None

    def test_returns_none_for_empty_string(self, monkeypatch):
        monkeypatch.setenv("QDRANT_API_KEY", "")
        assert get_qdrant_api_key() is None


class TestGetQdrantCollection:
    def test_returns_configured_value(self, monkeypatch):
        monkeypatch.setenv("QDRANT_COLLECTION", "my_collection")
        assert get_qdrant_collection() == "my_collection"

    def test_defaults_to_cohort_pdf_demo(self, monkeypatch):
        monkeypatch.delenv("QDRANT_COLLECTION", raising=False)
        assert get_qdrant_collection() == "cohort_pdf_demo"

    def test_defaults_when_empty_string(self, monkeypatch):
        monkeypatch.setenv("QDRANT_COLLECTION", "  ")
        assert get_qdrant_collection() == "cohort_pdf_demo"


class TestGetOpenAIApiKey:
    def test_returns_key_when_set(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        assert get_openai_api_key() == "sk-test"

    def test_returns_none_when_unset(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        assert get_openai_api_key() is None


class TestResolveApiKey:
    def test_prefers_ui_input_over_env(self, monkeypatch):
        monkeypatch.setenv("QDRANT_API_KEY", "env-key")
        assert resolve_api_key("ui-key") == "ui-key"

    def test_falls_back_to_env_when_ui_empty(self, monkeypatch):
        monkeypatch.setenv("QDRANT_API_KEY", "env-key")
        assert resolve_api_key("") == "env-key"
        assert resolve_api_key(None) == "env-key"
        assert resolve_api_key("   ") == "env-key"

    def test_returns_none_when_both_missing(self, monkeypatch):
        monkeypatch.delenv("QDRANT_API_KEY", raising=False)
        assert resolve_api_key("") is None
