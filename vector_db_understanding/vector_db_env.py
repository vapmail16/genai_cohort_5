"""
vector_db_env.py — Environment loader for Qdrant connection settings
=====================================================================
What students learn:
  - Why we keep secrets (URLs, API keys) out of code and in a .env file
  - How python-dotenv loads a specific .env path so the monorepo root .env
    (which is also gitignored) doesn't interfere
  - The "idempotent load" pattern — call this anywhere, it only runs once

Values it reads from vector_db_understanding/.env:
  QDRANT_URL        → your Qdrant Cloud HTTPS endpoint (port 6333)
  QDRANT_API_KEY    → Qdrant Cloud API key (or None for unauthenticated local)
  QDRANT_COLLECTION → default collection name (falls back to "cohort_pdf_demo")
"""

from __future__ import annotations

import os
from pathlib import Path

# ── Module-level flag so we only load the file once per process ───────────────
_ENV_LOADED = False


# ── Step 1: Load .env file ────────────────────────────────────────────────────
def load_vector_db_env() -> None:
    """Idempotent loader — safe to call multiple times from different modules."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        # python-dotenv not installed — skip silently, env vars may already be set
        _ENV_LOADED = True
        return
    # Always resolve relative to THIS file so it works regardless of cwd
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.is_file():
        load_dotenv(env_path)
    _ENV_LOADED = True


# ── Step 2: Typed accessors — one function per config value ───────────────────
# Each accessor calls load_vector_db_env() first, so callers don't have to
# remember to load the env themselves.

def get_qdrant_url() -> str:
    # Returns "" if not set — callers should warn the user in the UI
    load_vector_db_env()
    return os.getenv("QDRANT_URL", "").strip()


def get_qdrant_api_key() -> str | None:
    # Returns None (not empty string) when unset — QdrantClient accepts None
    load_vector_db_env()
    key = os.getenv("QDRANT_API_KEY", "").strip()
    return key or None


def get_qdrant_collection() -> str:
    # Falls back to a safe default so the lab always has a collection name
    load_vector_db_env()
    name = os.getenv("QDRANT_COLLECTION", "cohort_pdf_demo").strip()
    return name or "cohort_pdf_demo"


# ── Step 3: Key resolution helper ────────────────────────────────────────────
def resolve_api_key(user_input: str | None) -> str | None:
    """
    UI / CLI priority:
      1. If the user pasted a key in the text box, use that.
      2. Otherwise fall back to QDRANT_API_KEY from .env.
    This lets presenters override the key at demo time without editing .env.
    """
    u = (user_input or "").strip()
    if u:
        return u
    return get_qdrant_api_key()
