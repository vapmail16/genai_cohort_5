#!/usr/bin/env bash
#
# Download an Ollama model.
# Usage: ./download_model.sh [model_name]
# Example: ./download_model.sh llama3.2:3b
#

# -----------------------------------------------------------------------------
# PARAMETER HANDLING
# -----------------------------------------------------------------------------
# $1 = first argument passed to the script (the model name)
# ${1:-llama3.2:3b} = use $1 if provided, otherwise default to "llama3.2:3b"
# This is called "parameter expansion with default value" in bash
# -----------------------------------------------------------------------------
MODEL="${1:-llama3.2:3b}"

# -----------------------------------------------------------------------------
# DOWNLOAD THE MODEL
# -----------------------------------------------------------------------------
# ollama pull fetches the model from Ollama's registry and stores it locally.
# Models are stored in ~/.ollama/models/ (varies by OS).
# First run downloads; subsequent runs use cached layers.
# -----------------------------------------------------------------------------
echo "Downloading model: $MODEL"
ollama pull "$MODEL"
echo "✓ Done. Run with: ollama run $MODEL"
