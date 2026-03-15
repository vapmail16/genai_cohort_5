#!/usr/bin/env bash
#
# Ollama Offline Model Setup
# Installs Ollama and downloads a default model.
#

# -----------------------------------------------------------------------------
# FAIL-FAST MODE
# -----------------------------------------------------------------------------
# set -e: exit immediately if any command fails (non-zero exit code).
# This prevents the script from continuing after an error, which could
# make the system appear "partially configured" and harder to debug.
# -----------------------------------------------------------------------------
set -e

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
# OLLAMA_MODEL can be set by the user before running (e.g. export OLLAMA_MODEL=llama3.1:8b)
# ${OLLAMA_MODEL:-llama3.2:3b} = use env var if set, else default to "llama3.2:3b"
# -----------------------------------------------------------------------------
OLLAMA_URL="https://ollama.com"
DEFAULT_MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

echo "=============================================="
echo "  Ollama Offline Model Setup"
echo "=============================================="

# -----------------------------------------------------------------------------
# CHECK IF OLLAMA IS INSTALLED
# -----------------------------------------------------------------------------
# command -v ollama: returns the path to 'ollama' if it exists in PATH, else nothing
# &>/dev/null: redirects both stdout and stderr to /dev/null (suppress output)
# If installed, we skip to the next section; otherwise we install.
# -----------------------------------------------------------------------------
if command -v ollama &>/dev/null; then
    echo "✓ Ollama is already installed: $(ollama --version)"
else
    echo "Installing Ollama..."

    # -------------------------------------------------------------------------
    # OS-SPECIFIC INSTALLATION
    # -------------------------------------------------------------------------
    # uname -s: returns OS name (Darwin=macOS, Linux=Linux)
    # case/esac: bash switch statement for different OS handling
    # On macOS: use Homebrew if available; otherwise prompt manual download
    # On Linux: use official install script (curl | sh)
    # -------------------------------------------------------------------------
    case "$(uname -s)" in
        Darwin)
            if command -v brew &>/dev/null; then
                brew install ollama
            else
                echo "Download from: $OLLAMA_URL/download/mac"
                echo "Or install Homebrew: https://brew.sh"
                exit 1
            fi
            ;;
        Linux)
            curl -fsSL https://ollama.com/install.sh | sh
            ;;
        *)
            echo "Unsupported OS. Install manually from: $OLLAMA_URL/download"
            exit 1
            ;;
    esac
    echo "✓ Ollama installed: $(ollama --version)"
fi

# -----------------------------------------------------------------------------
# START OLLAMA SERVICE IF NOT RUNNING
# -----------------------------------------------------------------------------
# curl -s http://localhost:11434/api/tags: queries Ollama's API
# If this fails (connection refused), Ollama isn't running.
# We then start it: on macOS we run 'ollama serve' in background;
# on Linux we try systemctl first, then fall back to serve.
# (ollama serve &) runs in background; 2>/dev/null suppresses errors; || true prevents set -e from exiting
# -----------------------------------------------------------------------------
if ! curl -s http://localhost:11434/api/tags &>/dev/null; then
    echo ""
    echo "Starting Ollama service..."
    if [[ "$(uname -s)" == "Darwin" ]]; then
        # On macOS, Ollama runs as app - open it or run in background
        (ollama serve &) 2>/dev/null || true
        sleep 3
    else
        sudo systemctl start ollama 2>/dev/null || (ollama serve &)
        sleep 3
    fi
fi

# -----------------------------------------------------------------------------
# WAIT FOR OLLAMA TO BE READY (POLLING)
# -----------------------------------------------------------------------------
# Ollama may take a few seconds to start. We poll up to 10 times (2s each = 20s max).
# for i in {1..10}: bash brace expansion, loops i from 1 to 10
# break: exits the loop when we get a successful response
# -----------------------------------------------------------------------------
for i in {1..10}; do
    if curl -s http://localhost:11434/api/tags &>/dev/null; then
        echo "✓ Ollama service is running"
        break
    fi
    echo "  Waiting for Ollama... ($i/10)"
    sleep 2
done

# -----------------------------------------------------------------------------
# VERIFY OLLAMA IS RUNNING
# -----------------------------------------------------------------------------
# Final check: if we still can't connect, print manual instructions and exit.
# This ensures we don't proceed to download a model if the server isn't up.
# -----------------------------------------------------------------------------
if ! curl -s http://localhost:11434/api/tags &>/dev/null; then
    echo ""
    echo "Ollama may need to be started manually:"
    echo "  macOS: Open Ollama from Applications, or run: ollama serve"
    echo "  Linux: sudo systemctl start ollama"
    exit 1
fi

# -----------------------------------------------------------------------------
# DOWNLOAD THE DEFAULT MODEL
# -----------------------------------------------------------------------------
# ollama pull: fetches model weights from Ollama's registry.
# Models are stored locally; first run downloads (can be several GB).
# Subsequent runs use cache. The model is then ready for inference.
# -----------------------------------------------------------------------------
echo ""
echo "Downloading model: $DEFAULT_MODEL"
echo "(This may take a few minutes on first run)"
ollama pull "$DEFAULT_MODEL"
echo "✓ Model ready: $DEFAULT_MODEL"

echo ""
echo "=============================================="
echo "  Setup complete!"
echo "=============================================="
echo ""
echo "Quick start:"
echo "  ollama run $DEFAULT_MODEL    # Interactive chat"
echo "  ollama list                  # List installed models"
echo ""
echo "API: http://localhost:11434"
echo ""
