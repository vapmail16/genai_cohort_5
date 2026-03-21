# Prompt Engineering & LLM Architecture

Session 2 materials for GenAI Cohort 5. Demonstrates prompt techniques, injection defence, temperature effects, and token counting using the Acme Corp IT Support scenario.

## Prerequisites

- Python 3.10+
- `OPENAI_API_KEY` (uses GPT-4o)

## Setup

```bash
cd prompt_engineering
pip install -r requirements.txt
```

### Environment

Scripts look for `OPENAI_API_KEY` in `.env` from this folder or any sibling project (`capstone_project/backend`, `langchain_openai`). Create a local `.env` if needed:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Run All Scripts

```bash
# Run individually (recommended for learning)
python 03_temperature_and_tokens.py   # Run first — Part 1 (temperature & tokens)
python 01_prompt_techniques.py        # Part 2 — Zero-shot, Few-shot, CoT, TAG, PIC
python 02_prompt_injection.py         # Part 3 — Injection attacks & defences
python 04_student_task.py             # Part 4 — Student exercise (fill in TODOs)
```

### Run All in Sequence

```bash
python 03_temperature_and_tokens.py && \
python 01_prompt_techniques.py && \
python 02_prompt_injection.py && \
python 04_student_task.py
```

## Script Overview

| Script | Purpose |
|--------|---------|
| `03_temperature_and_tokens.py` | **Run first.** Temperature, max_tokens, token counting, roles, context window |
| `01_prompt_techniques.py` | Zero-shot → PIC + Technique 6: structured JSON (optional PostgreSQL) |
| `02_prompt_injection.py` | Injection attacks, input + output validation |
| `04_student_task.py` | Student task — customize TAG/PIC for your capstone |

## Expected Duration

- **03**: ~45 seconds (temperature, max_tokens, roles, token demos)
- **01**: ~20 seconds (6 techniques; Technique 6 = JSON + optional DB)
- **02**: ~20 seconds (injection + input/output validation)
- **04**: ~5 seconds (3 test messages)

## Local PostgreSQL (Technique 6)

Technique 6 in `01_prompt_techniques.py` stores classified tickets in local PostgreSQL.
The project uses `prompt_engineering/.env` with `OPENAI_API_KEY` and `DATABASE_URL`.

```bash
# 1. Start local PostgreSQL (macOS Homebrew)
brew services start postgresql@16

# 2. Create database
cd prompt_engineering
chmod +x setup_local_db.sh
./setup_local_db.sh

# 3. .env already has DATABASE_URL=postgresql://USER@localhost:5432/prompt_demo
```

If PostgreSQL is not running, 01 will print the parsed JSON and skip the DB write.

## Files

```
prompt_engineering/
├── 01_prompt_techniques.py    # 6 techniques: zero-shot → PIC → structured JSON
├── 02_prompt_injection.py     # Injection + input/output validation
├── 03_temperature_and_tokens.py  # Temperature, max_tokens, roles, tokens
├── env_loader.py              # Loads .env from this folder or siblings
├── requirements.txt
├── .env.example
└── README.md
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `OpenAIError: api_key must be set` | Create `.env` with `OPENAI_API_KEY=sk-...` or ensure a sibling project has it |
| Script hangs | Check network; API calls need internet |
| Rate limit | Wait a few seconds between runs or use a lower tier model |
