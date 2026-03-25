# genai_cohort_5

GenAI cohort materials, demos, and the **IT Support Agent** capstone (FastAPI + React + RAG + optional MCP).

---

## Repository layout (top level)

| Folder | What it is |
|--------|------------|
| [**capstone_project/**](capstone_project/) | **Main product:** IT Support Agent — `backend/` (FastAPI, agents, RAG, teaching routes, chat demo tracks), `frontend/` (Vite + React), `mcp_server/` (TypeScript MCP tools for stdio), `tests/`, `docs/`. See [capstone_project/docs/README.md](capstone_project/docs/README.md). |
| [**mcp/**](mcp/) | **Oxford / cohort MCP session:** plan ([OXFORD_MCP_SESSION_PLAN.md](mcp/OXFORD_MCP_SESSION_PLAN.md)), architecture HTML ([MCPArchitecture.html](mcp/MCPArchitecture.html), [ITSupportArchitecture.html](mcp/ITSupportArchitecture.html)), deck exports (`mcp_oxford_final.pdf` / `.pptx`), talking points (`mcp_talking_points_v2.docx`). |
| [**ai_agents/**](ai_agents/) | LangGraph / agent demos and training notes. |
| [**langchain_openai/**](langchain_openai/) | Week 2 — LangChain chatbot exercises (chains, memory, model switch). |
| [**neural_network_example/**](neural_network_example/) | Streamlit demo: next-word prediction with a small neural net. |
| [**offline_model_setup/**](offline_model_setup/) | Ollama — run LLMs locally (no API keys). |
| [**openai_api_test/**](openai_api_test/) | Minimal OpenAI API connectivity test. |
| [**project_scaffolding/**](project_scaffolding/) | Reusable SaaS-style folder template. |
| [**prompt_engineering/**](prompt_engineering/) | Prompt techniques, injection defence, temperature & tokens (Acme Corp IT theme). |
| [**rag_understanding/**](rag_understanding/) | RAG concepts and Streamlit exploration. |
| [**sdlc_with_llm/**](sdlc_with_llm/) | Compliance & Audit Copilot (BRIDGE AI framework). |
| [**vector_db_understanding/**](vector_db_understanding/) | Vector DB deep dive and helpers. |

---

## Capstone quick map

| Path | Role |
|------|------|
| `capstone_project/backend/main.py` | FastAPI app: `POST /chat`, tickets, health; includes **demo tracks** via `backend/chat_demo/`. |
| `capstone_project/backend/chat_demo/` | Demo routing: `plain_llm`, `rag_kb`, `rag_db` (DB → Qdrant `it_support_db`), `agentic_mcp`, welcome menu when `demo_mode` + “Hi”. |
| `capstone_project/backend/teaching/` | Isolated **teaching lab** routes (`/teaching/...`) — API basics, pipeline trace; not production chat. |
| `capstone_project/backend/rag/` | Qdrant KB retrieval; `db_retriever.py` for structured DB RAG. |
| `capstone_project/backend/agents/action_agent.py` | Tool selection + MCP call (**simulated** by default; **real stdio** when `USE_REAL_MCP=1`). |
| `capstone_project/mcp_server/` | Node MCP server (`npx tsx src/index.ts`) — run `npm install` here before real MCP. |
| `capstone_project/frontend/` | React UI; floating **Chatbot** with Oxford demo strip + presenter / MCP trace panels. |

**Run (typical):** copy-paste commands (venv, ingest, API, frontend, tests) live in [capstone_project/docs/README.md](capstone_project/docs/README.md) under **§ Command cheat sheet**. Short version: from `capstone_project/`, set `backend/.env` from `.env.example`, then `uvicorn backend.main:app --reload --port 8000`; frontend `cd frontend && npm run dev` (proxies to :8000).  

**Dependencies:** use a dedicated venv and `pip install -r capstone_project/backend/requirements.txt`. FastAPI **0.109.x** needs **Starlette 0.35.x** (pinned in requirements) — avoid upgrading Starlette to 1.x until FastAPI is upgraded.

**MCP tomorrow:** set `USE_REAL_MCP=1` in `.env` after `cd capstone_project/mcp_server && npm install`. Default path uses **in-process simulation** (no separate MCP terminal; real mode spawns the TS server per tool call over stdio).

---

## Projects (legacy table)

| Project | Description |
|---------|-------------|
| [neural_network_example](neural_network_example/) | Interactive Streamlit demo: how neural networks predict the next word in a sequence |
| [offline_model_setup](offline_model_setup/) | Ollama setup — run LLMs locally (no API keys) |
| [openai_api_test](openai_api_test/) | Simple OpenAI API connection test |
| [prompt_engineering](prompt_engineering/) | Session 2 — prompt techniques, injection defence, temperature & tokens (Acme Corp IT) |
| [langchain_openai](langchain_openai/) | Week 2 Day 2 — LangChain chatbot: chains, memory, model switch, interactive demo |
| [sdlc_with_llm](sdlc_with_llm/) | Compliance & Audit Copilot (BRIDGE AI Framework) |
| [capstone_project](capstone_project/) | IT Support Agent (RAG, chat demo tracks, teaching API lab, optional MCP) |
| [project_scaffolding](project_scaffolding/) | Standard SaaS folder structure template |

---

*Last updated: 2026-03-25 — root README lists actual `mcp/` files (no `sample documents/` folder); capstone chat demo and dependency notes unchanged.*
