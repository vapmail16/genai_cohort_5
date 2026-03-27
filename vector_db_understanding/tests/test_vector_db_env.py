"""Tests for vector_db_env / .env resolution."""

import os

import pytest

from vector_db_env import resolve_api_key


@pytest.fixture(autouse=True)
def clear_qdrant_env(monkeypatch):
    monkeypatch.delenv("QDRANT_API_KEY", raising=False)


def test_resolve_api_key_prefers_user_input(monkeypatch):
    monkeypatch.setenv("QDRANT_API_KEY", "from-env")
    assert resolve_api_key("from-ui") == "from-ui"


def test_resolve_api_key_falls_back_to_env(monkeypatch):
    monkeypatch.setenv("QDRANT_API_KEY", "secret")
    assert resolve_api_key("") == "secret"
    assert resolve_api_key("   ") == "secret"
    assert resolve_api_key(None) == "secret"


def test_resolve_api_key_none_without_env(monkeypatch):
    monkeypatch.delenv("QDRANT_API_KEY", raising=False)
    assert resolve_api_key("") is None
