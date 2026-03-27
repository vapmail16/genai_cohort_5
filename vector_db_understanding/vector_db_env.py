"""Load `vector_db_understanding/.env` and read Qdrant Cloud / server settings."""

from __future__ import annotations

import os
from pathlib import Path

_ENV_LOADED = False


def load_vector_db_env() -> None:
    """Idempotent: load `.env` from this package directory (monorepo root ignores `.env`)."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        _ENV_LOADED = True
        return
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.is_file():
        load_dotenv(env_path)
    _ENV_LOADED = True


def get_qdrant_url() -> str:
    load_vector_db_env()
    return os.getenv("QDRANT_URL", "").strip()


def get_qdrant_api_key() -> str | None:
    load_vector_db_env()
    key = os.getenv("QDRANT_API_KEY", "").strip()
    return key or None


def get_qdrant_collection() -> str:
    load_vector_db_env()
    name = os.getenv("QDRANT_COLLECTION", "cohort_pdf_demo").strip()
    return name or "cohort_pdf_demo"


def resolve_api_key(user_input: str | None) -> str | None:
    """Prefer non-empty UI/CLI input; otherwise use `QDRANT_API_KEY` from `.env`."""
    u = (user_input or "").strip()
    if u:
        return u
    return get_qdrant_api_key()
