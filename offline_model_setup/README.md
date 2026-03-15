# Offline Model Setup — Ollama

Run LLMs locally with **Ollama**. No API keys, no cloud — models run entirely on your machine.

## Prerequisites

- **macOS**: Sonoma (14+) or Big Sur (11+), Apple Silicon (M1/M2/M3) or Intel
- **Linux**: Most modern distros
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB+ free (varies by model)

## Quick Start

### 1. Run Setup (Install + Download Model)

```bash
cd offline_model_setup
chmod +x setup.sh
./setup.sh
```

This will:
- Install Ollama (via Homebrew on macOS, or install script on Linux)
- Start the Ollama service
- Download `llama3.2:3b` (~2GB) as the default model

### 2. Verify Connection

```bash
pip install -r requirements.txt
python test_connection.py
```

Expected output:
```
Testing Ollama at http://localhost:11434 (model: llama3.2:3b)...
  Installed models: llama3.2:3b
  Response: OK
SUCCESS: Ollama connection works.
```

### 3. Chat with the Model

```bash
ollama run llama3.2:3b
```

Press `Ctrl+D` to exit the chat.

---

## Manual Installation

### macOS

**Option A — Homebrew**
```bash
brew install ollama
```

**Option B — Direct Download**
Download from [ollama.com/download/mac](https://ollama.com/download/mac) and drag Ollama to Applications.

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `setup.sh` | Full setup: install Ollama + download default model |
| `download_model.sh [model]` | Download a specific model |
| `test_connection.py` | Verify Ollama API is reachable |

---

## Downloading Models

```bash
# Default (llama3.2:3b)
./download_model.sh

# Specific model
./download_model.sh llama3.1:8b
./download_model.sh mistral
./download_model.sh gemma2:2b
```

**Model recommendations by RAM:**
- **8GB**: `llama3.2:3b`, `gemma2:2b`
- **16GB**: `llama3.1:8b`, `qwen2.5:7b`, `mistral`
- **32GB+**: `llama3.1:70b`, `mixtral`

Browse all models: [ollama.com/library](https://ollama.com/library)

---

## API Usage

Ollama exposes a REST API at `http://localhost:11434`.

**List models:**
```bash
curl http://localhost:11434/api/tags
```

**Generate completion:**
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Hello, how are you?",
  "stream": false
}'
```

**Python (with LangChain):**
```python
from langchain_community.llms import Ollama
llm = Ollama(model="llama3.2:3b", base_url="http://localhost:11434")
print(llm.invoke("Say hello"))
```

---

## Configuration

Create `.env` (optional) to override defaults:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Connection refused` | Start Ollama: `ollama serve` or open the Ollama app (macOS) |
| `model not found` | Run `ollama pull llama3.2:3b` (or your model name) |
| Out of memory | Use a smaller model (e.g. `gemma2:2b`) |
| Slow responses | Use a smaller model or ensure no other heavy apps are running |

---

## Service Management

**macOS**: Ollama runs as an app. Open from Applications or run `ollama serve` in a terminal.

**Linux**:
```bash
sudo systemctl start ollama   # Start
sudo systemctl enable ollama # Start on boot
sudo systemctl status ollama # Check status
```
