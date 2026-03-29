"""
rag_env.py — Environment loader for RAG demo
=============================================
What students learn:
  - How a RAG system needs TWO kinds of credentials:
      1. Qdrant (vector store) — URL + API key
      2. OpenAI (generator)   — API key
  - Why we keep them in .env and never in code
  - How to point dotenv at a specific path so the monorepo root .env is ignored

Values read from rag_understanding/.env:
  QDRANT_URL        → Qdrant Cloud HTTPS endpoint
  QDRANT_API_KEY    → Qdrant Cloud API key
  QDRANT_COLLECTION → collection to query (must be ingested first via vector_db tab)
  OPENAI_API_KEY    → OpenAI API key for the generation step
"""

from __future__ import annotations

import os
from pathlib import Path

# ── One-shot load flag ────────────────────────────────────────────────────────
_ENV_LOADED = False


def load_rag_env() -> None:
    """Idempotent: load rag_understanding/.env exactly once per process."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        _ENV_LOADED = True
        return
    # Resolve relative to THIS file so cwd doesn't matter
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.is_file():
        load_dotenv(env_path)
    _ENV_LOADED = True


# ── Typed accessors ───────────────────────────────────────────────────────────

def get_qdrant_url() -> str:
    load_rag_env()
    return os.getenv("QDRANT_URL", "").strip()


def get_qdrant_api_key() -> str | None:
    load_rag_env()
    key = os.getenv("QDRANT_API_KEY", "").strip()
    return key or None


def get_qdrant_collection() -> str:
    load_rag_env()
    name = os.getenv("QDRANT_COLLECTION", "cohort_pdf_demo").strip()
    return name or "cohort_pdf_demo"


def get_openai_api_key() -> str | None:
    load_rag_env()
    key = os.getenv("OPENAI_API_KEY", "").strip()
    return key or None


def resolve_api_key(user_input: str | None) -> str | None:
    """UI/CLI input beats .env; falls back to QDRANT_API_KEY in .env."""
    u = (user_input or "").strip()
    if u:
        return u
    return get_qdrant_api_key()
