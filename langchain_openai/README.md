# Week 2 Day 2 — LangChain Chatbot Session

## Setup (do this first)

```bash
# 1. Install dependencies
cd langchain_openai
pip install -r requirements.txt

# 2. API keys (loaded from monorepo or langchain_openai/.env)
#    - OPENAI_API_KEY: from capstone_project/backend/.env or project root .env
#    - ANTHROPIC_API_KEY: (optional) for 03_model_switch — add to langchain_openai/.env
```

---

## Step-by-Step: Run All Scripts

### Step 0: Offline model (optional — for local demo in 03)

```bash
cd offline_model_setup
chmod +x setup.sh
./setup.sh
```

This installs Ollama, starts the service, and downloads `llama3.2:3b`. Verify:

```bash
curl -s http://localhost:11434/api/tags
python test_connection.py
```

### Step 1: Basic chain

```bash
cd langchain_openai
python 01_basic_chain.py
```

### Step 2: Memory & conversations

```bash
python 02_memory_conversations.py
```

### Step 3: Model switch (OpenAI + Anthropic + Ollama)

```bash
python 03_model_switch.py
```

Runs the same prompt through: OpenAI GPT-4o, Anthropic Claude, and Ollama (local). For Ollama to work, run `offline_model_setup/setup.sh` first.

### Step 4: Interactive chatbot

```bash
python 04_interactive_chatbot.py
```

Type `quit` or `exit` to end. Commands: `history`, `clear`.

### Step 5: Sequential chain (bonus)

```bash
python 05_sequential_chain.py
```

---

## Demo Order

| File | What it teaches | Time |
|------|----------------|------|
| `01_basic_chain.py` | LCEL, pipe syntax, system prompts | 15 min |
| `02_memory_conversations.py` | Stateless LLMs, buffer + window memory | 20 min |
| `03_model_switch.py` | One-line model swap (OpenAI / Claude / Ollama) | 10 min |
| `04_interactive_chatbot.py` | Full interactive terminal chatbot | Live demo |
| `05_sequential_chain.py` | BONUS: chaining multiple LLM calls | If time |

---

## Key Teaching Moments

**In Demo 1** — show what `prompt.format_messages()` produces before running the chain. Students need to see the actual messages array the LLM receives.

**In Demo 2** — run `demo_no_memory()` first so students feel the pain. Then show buffer memory fixing it. The `[Messages currently in memory: N]` counter in the window demo makes the concept tangible.

**In Demo 3** — this is the big reveal. The chain code is literally identical. Only the `llm = ...` line changes. Let it land.

**In Demo 4** — hand this to students. Task: "Add a system prompt that makes the bot reflect your capstone project, not Acme Corp."

---

## Student Task (end of session)

> Build a LangChain chatbot for your capstone project using `04_interactive_chatbot.py` as a base. Customise the system prompt for your use case. Test it with at least 5 multi-turn messages. Optional: swap in Ollama if you have it running.

---

## What's Next

- **Week 2 Day 1 (22 Mar):** Prompt Engineering — refine the system prompts built today
- **Week 3 (28 Mar):** Vector DB — give the chatbot real documents to search
- **Week 4 (29 Mar):** RAG — wire retrieval into the chain built here
- **Week 5:** LangChain LCEL deep dive — refactor using `retriever | prompt | llm`
