"""Config.validate() — LLM and Zep required at startup."""

import pytest

from app.config import Config


@pytest.fixture(autouse=True)
def restore_config():
    llm = Config.LLM_API_KEY
    zep = Config.ZEP_API_KEY
    yield
    Config.LLM_API_KEY = llm
    Config.ZEP_API_KEY = zep


def test_validate_passes_with_llm_and_zep(monkeypatch):
    monkeypatch.setattr(Config, "LLM_API_KEY", "sk-test")
    monkeypatch.setattr(Config, "ZEP_API_KEY", "zep-test")
    assert Config.validate() == []


def test_validate_fails_without_llm(monkeypatch):
    monkeypatch.setattr(Config, "LLM_API_KEY", None)
    monkeypatch.setattr(Config, "ZEP_API_KEY", "zep-test")
    errors = Config.validate()
    assert any("LLM_API_KEY" in e for e in errors)


def test_validate_fails_without_zep(monkeypatch):
    monkeypatch.setattr(Config, "LLM_API_KEY", "sk-test")
    monkeypatch.setattr(Config, "ZEP_API_KEY", None)
    errors = Config.validate()
    assert any("ZEP_API_KEY" in e for e in errors)
