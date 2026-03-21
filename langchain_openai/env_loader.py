"""
Load .env from monorepo (capstone_project/backend or project root).
Ensures OPENAI_API_KEY is available without duplicating secrets.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATHS = [
    ROOT / "capstone_project" / "backend" / ".env",
    ROOT / ".env",
    ROOT / "offline_model_setup" / ".env",  # OLLAMA_BASE_URL, OLLAMA_MODEL
    Path(__file__).resolve().parent / ".env",  # local .env if present
]


def load_env():
    """Load all existing .env files (monorepo first, then local). Last file can override earlier ones."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return None
    last_loaded = None
    for p in ENV_PATHS:
        if p.exists():
            # override=True so langchain_openai/.env overrides OLLAMA_* from monorepo
            load_dotenv(p, override=True)
            last_loaded = str(p)
    return last_loaded
