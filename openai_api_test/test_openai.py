#!/usr/bin/env python3
"""
Simple OpenAI API connection test.
Loads OPENAI_API_KEY from .env in the monorepo (capstone_project/backend or project root).
"""

import os
import sys
from pathlib import Path

# -----------------------------------------------------------------------------
# CONFIGURE .ENV SEARCH PATHS
# -----------------------------------------------------------------------------
# Path(__file__).resolve().parent.parent = project root (two levels up from this script)
# We check multiple locations so the script works whether .env is in capstone or root.
# Path / operator: Path / "subdir" creates a new path (e.g. ROOT / "capstone_project")
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
ENV_PATHS = [
    ROOT / "capstone_project" / "backend" / ".env",
    ROOT / ".env",
]


def load_env():
    """Load .env from monorepo."""
    # -------------------------------------------------------------------------
    # LAZY IMPORT WITH FALLBACK
    # -------------------------------------------------------------------------
    # Try importing dotenv; if not installed, pip install and retry.
    # This keeps the script self-contained for teaching/portability.
    # sys.executable = path to the Python interpreter running this script
    # -------------------------------------------------------------------------
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("Installing python-dotenv...")
        os.system(f"{sys.executable} -m pip install python-dotenv -q")
        from dotenv import load_dotenv

    # -------------------------------------------------------------------------
    # LOAD FIRST EXISTING .ENV
    # -------------------------------------------------------------------------
    # load_dotenv(path) reads KEY=value pairs and adds them to os.environ.
    # Returns the path we loaded from (for user feedback), or None if none found.
    # -------------------------------------------------------------------------
    for path in ENV_PATHS:
        if path.exists():
            load_dotenv(path)
            return str(path)
    return None


def test_openai_connection():
    """Test OpenAI API with a simple chat completion."""
    # -------------------------------------------------------------------------
    # LAZY IMPORT OF OPENAI CLIENT
    # -------------------------------------------------------------------------
    # Same pattern as dotenv: try import, install if missing, then use.
    # The openai package provides the official Python SDK for OpenAI's API.
    # -------------------------------------------------------------------------
    try:
        from openai import OpenAI
    except ImportError:
        print("Installing openai...")
        os.system(f"{sys.executable} -m pip install openai -q")
        from openai import OpenAI

    # -------------------------------------------------------------------------
    # VALIDATE API KEY
    # -------------------------------------------------------------------------
    # OpenAI() reads OPENAI_API_KEY from os.environ automatically.
    # We check explicitly to give a clear error if key is missing or placeholder.
    # "your_openai_api_key_here" is the default in .env.example files.
    # -------------------------------------------------------------------------
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("ERROR: OPENAI_API_KEY not set or invalid.")
        print("Add your key to capstone_project/backend/.env or project root .env")
        return False

    print("Testing OpenAI API connection...")

    # -------------------------------------------------------------------------
    # CREATE CLIENT AND SEND REQUEST
    # -------------------------------------------------------------------------
    # OpenAI() uses OPENAI_API_KEY from environment by default.
    # chat.completions.create: sends a chat message and gets a model response.
    # messages: list of {role, content}; "user" = human, "assistant" = model.
    # max_tokens: limit response length (we use 10 for a quick "OK" test).
    # gpt-4o-mini: smaller, faster model; use gpt-4o for more capability.
    # -------------------------------------------------------------------------
    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply with exactly: OK"}],
            max_tokens=10,
        )
        # response.choices[0] = first (and usually only) completion
        # .message.content = the text the model generated
        reply = response.choices[0].message.content.strip()
        print(f"Response: {reply}")
        print("SUCCESS: OpenAI API connection works.")
        return True
    except Exception as e:
        # Catches: invalid key, rate limits, network errors, etc.
        print(f"ERROR: {e}")
        return False


def main():
    """Entry point: load env, run test, exit with appropriate code."""
    # -------------------------------------------------------------------------
    # LOAD ENV AND RUN TEST
    # -------------------------------------------------------------------------
    env_path = load_env()
    if env_path:
        print(f"Loaded .env from: {env_path}")
    else:
        print("No .env found. Using existing environment.")

    success = test_openai_connection()

    # -------------------------------------------------------------------------
    # EXIT CODE
    # -------------------------------------------------------------------------
    # sys.exit(0) = success, sys.exit(1) = failure.
    # Shell scripts and CI tools use this to know if the test passed.
    # -------------------------------------------------------------------------
    sys.exit(0 if success else 1)


# -----------------------------------------------------------------------------
# SCRIPT ENTRY POINT
# -----------------------------------------------------------------------------
# __name__ == "__main__": True when script is run directly (python test_openai.py)
# False when imported as a module (from test_openai import load_env)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
