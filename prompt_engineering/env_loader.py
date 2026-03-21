"""
Load .env from prompt_engineering or any sibling project (capstone, langchain_openai).
Ensures OPENAI_API_KEY is available when running scripts from this folder.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Load in order: later overrides earlier. prompt_engineering/.env LAST = wins.
# This ensures 01-04 use OPENAI_API_KEY and DATABASE_URL from this folder.
ENV_PATHS = [
    ROOT / ".env",
    ROOT / "langchain_openai" / ".env",
    ROOT / "capstone_project" / "backend" / ".env",
    Path(__file__).resolve().parent / ".env",         # prompt_engineering/.env (overrides)
]


def load_env():
    """Load all existing .env files (later overrides earlier). Ensures OPENAI_API_KEY from any project."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return None
    loaded = None
    for p in ENV_PATHS:
        if p.exists():
            load_dotenv(p, override=True)
            loaded = str(p)
    return loaded
