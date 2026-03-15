#!/usr/bin/env python3
"""
Test Ollama API connection.
Verifies the local Ollama server is running and responds to a simple prompt.
"""

import os
import sys
from pathlib import Path

# -----------------------------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES (OPTIONAL)
# -----------------------------------------------------------------------------
# We look for .env in the monorepo (capstone_project/backend or project root).
# dotenv loads KEY=value pairs into os.environ so we can use os.getenv().
# This allows overriding OLLAMA_BASE_URL and OLLAMA_MODEL without changing code.
# Path(__file__).resolve().parent.parent = go up two directories from this script
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
for env_path in [ROOT / "capstone_project" / "backend" / ".env", ROOT / ".env"]:
    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
            break
        except ImportError:
            pass

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
# os.getenv(key, default): read from environment; use default if not set.
# OLLAMA_BASE_URL: where the Ollama API server listens (default localhost:11434)
# OLLAMA_MODEL: which model to use (e.g. llama3.2:3b = Llama 3.2, 3B params)
# -----------------------------------------------------------------------------
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def test_ollama_connection():
    """Test Ollama API with a simple completion."""
    # -------------------------------------------------------------------------
    # LAZY IMPORT OF REQUESTS
    # -------------------------------------------------------------------------
    # We import requests inside the function so the script can run even if
    # requests isn't installed (we'll try to install it). This keeps the
    # script self-contained for teaching/portability.
    # -------------------------------------------------------------------------
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        os.system(f"{sys.executable} -m pip install requests -q")
        import requests

    print(f"Testing Ollama at {OLLAMA_BASE_URL} (model: {DEFAULT_MODEL})...")

    try:
        # ---------------------------------------------------------------------
        # STEP 1: CHECK IF SERVER IS UP (HEALTH CHECK)
        # ---------------------------------------------------------------------
        # GET /api/tags returns a list of installed models on the server.
        # If this fails with ConnectionError, Ollama isn't running.
        # r.raise_for_status() raises an exception for 4xx/5xx HTTP errors.
        # ---------------------------------------------------------------------
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        r.raise_for_status()
        models = r.json().get("models", [])
        model_names = [m.get("name", "") for m in models]
        print(f"  Installed models: {', '.join(model_names) or 'none'}")

        # ---------------------------------------------------------------------
        # STEP 2: RESOLVE MODEL NAME
        # ---------------------------------------------------------------------
        # User may set OLLAMA_MODEL=llama3.2 but the installed model is llama3.2:3b.
        # Ollama requires the exact name. We find a match: exact or prefix match
        # (e.g. "llama3.2" matches "llama3.2:3b"). If no match, use first installed.
        # next(..., None): returns first match or None if generator is exhausted.
        # ---------------------------------------------------------------------
        model_to_use = DEFAULT_MODEL
        if DEFAULT_MODEL not in model_names:
            match = next((n for n in model_names if n == DEFAULT_MODEL or n.startswith(DEFAULT_MODEL + ":")), None)
            if match:
                model_to_use = match
            elif model_names:
                model_to_use = model_names[0]

        # ---------------------------------------------------------------------
        # STEP 3: SEND A PROMPT (INFERENCE REQUEST)
        # ---------------------------------------------------------------------
        # POST /api/generate: sends a prompt to the model and returns a completion.
        # "stream": false = return full response at once (simpler for testing).
        # "stream": true = return tokens as they're generated (for chat UIs).
        # timeout=60: LLM inference can take several seconds per request.
        # ---------------------------------------------------------------------
        r = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model_to_use,
                "prompt": "Reply with exactly: OK",
                "stream": False,
            },
            timeout=60,
        )
        r.raise_for_status()
        reply = r.json().get("response", "").strip()
        print(f"  Response: {reply}")
        print("SUCCESS: Ollama connection works.")
        return True

    # -------------------------------------------------------------------------
    # ERROR HANDLING
    # -------------------------------------------------------------------------
    # ConnectionError: Ollama server not reachable (not running, wrong port, etc.)
    # Other exceptions: e.g. 404 (model not found), JSON decode errors, etc.
    # -------------------------------------------------------------------------
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Ollama. Is it running?")
        print("  Start with: ollama serve")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


# -----------------------------------------------------------------------------
# SCRIPT ENTRY POINT
# -----------------------------------------------------------------------------
# __name__ == "__main__": only run when script is executed directly (not imported).
# sys.exit(0): success, sys.exit(1): failure (convention for shell scripts).
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    success = test_ollama_connection()
    sys.exit(0 if success else 1)
