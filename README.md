# genai_cohort_5

GenAI cohort materials, demos, and the **IT Support Agent** capstone (FastAPI + React + RAG + optional MCP).

---

## Repository layout (top level)

| Folder | What it is |
| --- | --- |
| [**capstone\_project/**](capstone_project/) | **Primary cohort build:** IT Support Agent (`backend/` FastAPI + RAG + agents + teaching routes, `frontend/` Vite React, `mcp_server/` TypeScript MCP tools, `tests/`, `docs/`). |
| [**oxford\_capstone/**](oxford_capstone/) | Standalone Oxford bundle copy of capstone + MCP session materials; includes its own setup/run docs and troubleshooting log. |
| [**mcp/**](mcp/) | MCP session assets: architecture HTML, session materials, and [mcp-dungeon](mcp/mcp-dungeon/) demo. |
| [**ai\_agents/**](ai_agents/) | LangGraph/agent demos and workflow examples. |
| [**langchain\_openai/**](langchain_openai/) | Week 2 LangChain chatbot exercises (chains, memory, model switching). |
| [**prompt\_engineering/**](prompt_engineering/) | Prompt techniques, anti-injection practice, and temperature/token experiments. |
| [**vector\_db\_understanding/**](vector_db_understanding/) | Vector DB lab (Qdrant-oriented experiments and tests). |
| [**rag\_understanding/**](rag_understanding/) | RAG foundations and advanced retrieval experiments. |
| [**sdlc\_with\_llm/**](sdlc_with_llm/) | Compliance/audit copilot project (BRIDGE AI framing). |
| [**offline\_model\_setup/**](offline_model_setup/) | Ollama/local-model setup and scripts. |
| [**openai\_api\_test/**](openai_api_test/) | Minimal API connectivity/testing sandbox. |
| [**neural\_network\_example/**](neural_network_example/) | Streamlit next-word prediction demo. |
| [**project\_scaffolding/**](project_scaffolding/) | Reusable SaaS-style folder structure starter. |
| [**langsmith/**](langsmith/) | LangSmith metrics and tracing demo (`langsmith_demo.py`, Streamlit dashboard, test scenarios). |
| [**MiroFish/**](MiroFish/) | Separate multi-agent prediction project (Flask backend + Vue frontend + Docker + static assets). |
| [**Exams/**](Exams/) | Interim/advanced exam question banks (questions-only and Q&A variants). |
| `GenAI_6Week_Cohort_Syllabus_Generic.pdf` | Source curriculum document used for week/day planning in this README. |

---

## Capstone quick map

| Path | Role |
| --- | --- |
| `capstone_project/backend/main.py` | FastAPI app: `POST /chat`, tickets, health; includes **demo tracks** via `backend/chat_demo/`. |
| `capstone_project/backend/chat_demo/` | Demo routing: `plain_llm`, `rag_kb`, `rag_db` (DB → Qdrant `it_support_db`), `agentic_mcp`, welcome menu when `demo_mode` + “Hi”. |
| `capstone_project/backend/teaching/` | Isolated **teaching lab** routes (`/teaching/...`) — API basics, pipeline trace; not production chat. |
| `capstone_project/backend/rag/` | Qdrant KB retrieval; `db_retriever.py` for structured DB RAG. |
| `capstone_project/backend/agents/action_agent.py` | Tool selection + MCP call (**simulated** by default; **real stdio** when `USE_REAL_MCP=1`). |
| `capstone_project/mcp_server/` | Node MCP server (`npx tsx src/index.ts`) — run `npm install` here before real MCP. |
| `capstone_project/frontend/` | React UI; floating **Chatbot** with Oxford demo strip + presenter / MCP trace panels. |

**Run (typical):** copy-paste commands (venv, ingest, API, frontend, tests) live in [README.md](./capstone_project/docs/README.md) under **§ Command cheat sheet**. Short version: from `capstone_project/`, set `backend/.env` from `.env.example`, then `uvicorn backend.main:app --reload --port 8000`; frontend `cd frontend && npm run dev` (proxies to :8000).  

**Dependencies:** use a dedicated venv and `pip install -r capstone_project/backend/requirements.txt`. FastAPI **0.109.x** needs **Starlette 0.35.x** (pinned in requirements) — avoid upgrading Starlette to 1.x until FastAPI is upgraded.

**MCP tomorrow:** set `USE_REAL_MCP=1` in `.env` after `cd capstone_project/mcp_server && npm install`. Default path uses **in-process simulation** (no separate MCP terminal; real mode spawns the TS server per tool call over stdio).

---

## Project catalog (exhaustive at top-level)

| Area | Path | Primary focus |
| --- | --- | --- |
| Capstone (primary) | [capstone_project](capstone_project/) | End-to-end IT Support Agent (FastAPI + React + RAG + optional real MCP). |
| Capstone (bundle copy) | [oxford_capstone](oxford_capstone/) | Packaged Oxford-facing copy of capstone + MCP assets. |
| MCP materials | [mcp](mcp/) | MCP architecture/session collateral and `mcp-dungeon` teaching demo. |
| Agent systems | [ai_agents](ai_agents/) | Agent patterns, LangGraph demos, and tool-calling exercises. |
| Chatbot stack | [langchain_openai](langchain_openai/) | LangChain chatbot implementation examples. |
| Prompting track | [prompt_engineering](prompt_engineering/) | Prompt engineering, adversarial prompt patterns, token/temperature controls. |
| Retrieval track | [vector_db_understanding](vector_db_understanding/) | Qdrant/vector indexing, retrieval quality experiments, tests. |
| RAG track | [rag_understanding](rag_understanding/) | Basic/advanced RAG workflows and retrieval evaluation work. |
| SDLC/compliance | [sdlc_with_llm](sdlc_with_llm/) | Compliance-oriented copilot, regulations-focused processing. |
| Local-model track | [offline_model_setup](offline_model_setup/) | Offline inference setup and local model operations. |
| API sandbox | [openai_api_test](openai_api_test/) | OpenAI/API quick tests and connectivity checks. |
| Fundamentals demo | [neural_network_example](neural_network_example/) | Intro neural network app (next-token style toy demo). |
| Scaffolding template | [project_scaffolding](project_scaffolding/) | Reusable baseline structure for new app builds. |
| Observability demo | [langsmith](langsmith/) | LangSmith metrics logging and dashboarding examples. |
| External project | [MiroFish](MiroFish/) | Multi-agent simulation/prediction system (separate architecture stack). |
| Assessment content | [Exams](Exams/) | GenAI interim/advanced exam packs. |
| Curriculum artifact | `GenAI_6Week_Cohort_Syllabus_Generic.pdf` | 6-week syllabus reference document. |

---

## 6-Week Day-Wise Improvement Plan (based on your syllabus)

Goal: make each session outcome-driven, portfolio-ready, and tightly connected to this repository.

Note: Saturday and Sunday are teaching days for new content. Wednesday is reserved for Q&A, doubt-clearing, assignment review, and troubleshooting only (no new topics).

### Week 1 - Foundations & LLM Essentials

| Day | Current topic | What to add/improve |
| --- | --- | --- |
| Sat | SDLC with LLM, tools, scaffolding | Add one shared `project_kickoff_checklist` in `project_scaffolding/` (problem statement, success metrics, dataset source, eval criteria, risk register). Add a "Definition of Done" template for each mini-project. |
| Sun | LLM intro, architecture, use cases | Add a comparative notebook/script: same prompt across OpenAI/Claude/DeepSeek with output + latency + cost notes. Include "when to use which model" rubric in `prompt_engineering/`. |

Wed Q&A focus: setup support, troubleshooting FAQ walk-through, and implementation blocker resolution from Week 1 topics.

### Week 2 - Chatbots & Prompt Engineering

| Day | Current topic | What to add/improve |
| --- | --- | --- |
| Sat | Basic chatbot with LangChain | Introduce chatbot versioning: `v1_basic`, `v2_memory`, `v3_guardrails` inside `langchain_openai/` so students see progressive architecture evolution. |
| Sun | Prompt engineering techniques | Add structured prompt test cases (good prompt vs bad prompt vs adversarial prompt). Track outputs in a repeatable format and teach prompt regression checks. |

Wed Q&A focus: rubric-based reviews (quality, hallucination, latency, safety) and iteration support; no new concepts.

### Week 3 - Vector DBs & RAG Foundations

| Day | Current topic | What to add/improve |
| --- | --- | --- |
| Sat | Qdrant deep dive | Add chunking experiments (`small`, `medium`, `semantic`) and retrieval comparison scripts under `vector_db_understanding/` with measurable precision@k. |
| Sun | Basic + Self-RAG over docs | Add a baseline-vs-RAG benchmark task in `rag_understanding/`: same question set, compare groundedness and citation quality. |

Wed Q&A focus: student pipeline debugging using the predefined RAG troubleshooting playbook.

### Week 4 - Advanced RAG & AI Agents

| Day | Current topic | What to add/improve |
| --- | --- | --- |
| Sat | Advanced/Self-RAG continuation | Add re-ranking + query rewriting experiments in `capstone_project/backend/rag/` and compare against current retrieval chain with tracked eval prompts. |
| Sun | AI agents intro/patterns | Add one multi-tool agent mini-lab in `ai_agents/`: planner, retriever, action tool, validator. Include failure handling paths (timeouts/tool errors). |

Wed Q&A focus: architecture reviews using the checklist (boundaries, state, retries, observability).

### Week 5 - Agent Orchestration & MCP

| Day | Current topic | What to add/improve |
| --- | --- | --- |
| Sat | LangGraph orchestration | Add one canonical LangGraph flow with state diagram + trace examples in `ai_agents/` (single agent, supervisor pattern, human-in-loop variant). |
| Sun | MCP and modular AI tools | Expand `capstone_project/mcp_server/` with 2-3 production-like tools (ticket lookup, KB fetch, system status) plus strict input/output schemas and error contracts. |

Wed Q&A focus: MCP setup support, tool-call debugging, and test-failure triage only.

### Week 6 - Advanced Applications & Capstone

| Day | Current topic | What to add/improve |
| --- | --- | --- |
| Sat | Full app implementation with agents + MCP | Add "capstone release candidate" checklist: API contract freeze, smoke tests, demo script, rollback plan, and deployment readiness gates. |
| Sun | Offline model setup + capstone review | Add side-by-side online vs offline model benchmark (quality, latency, cost, privacy trade-offs) in `offline_model_setup/` and present decision guidance. |

Wed Q&A focus: final polishing support (demo rehearsal, README feedback, blocker removal).

### Cross-week improvements (high impact)

1. Add a common evaluation harness for all weeks (quality, safety, latency, cost) so progress is measurable.
2. Introduce lightweight CI checks in key modules (`tests`, lint, basic smoke endpoints) to make deliverables production-minded.
3. Add one "failure case of the week" log where students document what broke, root cause, and fix.
4. Standardize assignment templates: objective, dataset, constraints, expected output, and grading rubric.
5. Add a final "best projects showcase" page linking standout work from each week.

---

## Curriculum v2 Add-On (theme-aligned only)

Purpose: strengthen the current curriculum with missing GenAI landscape topics while staying inside each day's original theme.

Note: v2 add-ons are introduced on Saturday and Sunday only. Wednesday remains Q&A/review/support with no new topics.

### Theme-aligned day-wise enhancement plan

| Week | Day | Existing day theme | Theme-aligned add-on topic | Why it fits this day | Suggested repository integration |
| --- | --- | --- | --- | --- | --- |
| Week 1 | Sat | SDLC with LLM + scaffolding | AI project quality gates (eval criteria, risk log, acceptance checks) | SDLC day should define engineering standards before coding | Extend `project_scaffolding/` with a quality-gates checklist template |
| Week 1 | Sun | LLM intro (architecture, capabilities, use cases) | Model selection matrix (capability vs latency vs cost) | Natural extension of "LLM capabilities and use cases" | Add a comparison script in `openai_api_test/` or `prompt_engineering/` |
| Week 2 | Sat | Build basic chatbot | Guardrails in chatbot flow (input sanitization, refusal rules) | Directly improves chatbot robustness | Add `v3_guardrails` variant in `langchain_openai/` |
| Week 2 | Sun | Prompt engineering | Prompt security (injection resistance, data leakage-safe prompts) | Security is part of advanced prompting practice | Add `red_team_prompts/` and defense patterns in `prompt_engineering/` |
| Week 3 | Sat | Vector DB deep dive (Qdrant) | Hybrid retrieval and indexing strategy trade-offs | It stays inside retrieval/indexing fundamentals | Add dense-vs-hybrid experiment in `vector_db_understanding/` |
| Week 3 | Sun | RAG deep dive (basic + self RAG) | Reranking, metadata filtering, grounded citation checks | Core RAG quality improvements | Add reranker experiments in `rag_understanding/` |
| Week 4 | Sat | Advanced RAG | Query rewriting and multi-hop retrieval | Standard advanced-RAG techniques | Add query-rewrite stage in `capstone_project/backend/rag/` |
| Week 4 | Sun | AI agents intro | Agent safety/reliability patterns (timeouts, retries, tool errors) | Fits agent design patterns and real-world usage | Add failure-handling patterns in `ai_agents/` |
| Week 5 | Sat | LangGraph orchestration | State reliability and recovery (checkpointing/human-in-loop) | Directly tied to orchestration and workflow state | Add checkpoint/handoff pattern example in `ai_agents/` |
| Week 5 | Sun | MCP microservices | MCP contract testing (schema validation, fallback paths) | Fits modular tool deployment quality | Add MCP integration tests in `capstone_project/tests/` |
| Week 6 | Sat | Full advanced AI app workflow | LLMOps release readiness (SLOs, rollout, rollback) | Production workflow day should include launch mechanics | Add release checklist in `capstone_project/docs/` |
| Week 6 | Sun | Offline model setup + capstone review | Online vs offline deployment decision framework | Direct extension of offline model topic | Add benchmark template in `offline_model_setup/` |

Wed Q&A focus (all weeks, no new topics): doubt clearing, assignment reviews, code walkthroughs, bug fixes, and capstone feedback on the same week's Sat/Sun content.

### Add 4 mandatory tracks (if time is limited)

1. Evaluation harness and regression tests (quality + safety + latency + cost).
2. Security and red-team practice (prompt injection and tool safety).
3. LLMOps reliability (routing, fallback, caching, SLOs).
4. Advanced retrieval (hybrid search, reranking, query rewrite, graph option).

### Suggested rubric upgrade

- Technical correctness: 30%
- Evaluation quality and reproducibility: 20%
- Safety and risk mitigation: 20%
- Reliability and observability: 15%
- Product clarity (UX + problem framing + demo quality): 15%

## 5-10 Minute Real-Life Use Case Discussion Bank (Sat/Sun only)

Purpose: close each teaching session with one unique real-world use case that matches the day's theme and sparks practical thinking.

How to use:
- Pick one use case at the end of class (5-10 minutes).
- Cover: business problem, GenAI solution shape, risks, and success metric.
- Keep it discussion-first; no new implementation required in this segment.

| Week | Day | Day theme | Real-life use case to discuss (unique) | 3 talking points for your 5-10 min close |
| --- | --- | --- | --- | --- |
| Week 1 | Sat | SDLC with LLM + scaffolding | **Insurance Claims Triage Copilot**: intake agent that classifies incoming claim narratives and routes to adjuster queues | 1) How scope boundaries prevent over-automation, 2) what "Definition of Done" means for regulated workflows, 3) acceptance criteria before pilot launch |
| Week 1 | Sun | LLM architecture/capabilities/use cases | **Legal Intake Assistant**: first-pass case intake summarizer for law firms | 1) Which model fits confidentiality + reasoning needs, 2) hallucination risk in legal summaries, 3) where human review is mandatory |
| Week 2 | Sat | Basic chatbot building | **E-commerce Return Assistant**: chatbot that handles return eligibility and policy explanations | 1) Conversation design vs policy correctness, 2) escalation triggers to human support, 3) KPI: first-contact resolution rate |
| Week 2 | Sun | Prompt engineering | **Executive Briefing Generator**: converts long market reports into C-level one-pagers | 1) Prompt patterns for factual compression, 2) prompt guardrails against fabricated numbers, 3) quality rubric for decision-ready summaries |
| Week 3 | Sat | Vector DB deep dive | **Pharma R&D Literature Finder**: semantic retrieval for trial and molecule references | 1) Why chunk strategy changes recall, 2) metadata filtering by year/study type, 3) precision@k vs researcher trust |
| Week 3 | Sun | Basic/Self RAG over documents | **HR Policy Q&A Assistant**: answers employee policy questions with cited handbook sections | 1) Baseline LLM vs RAG behavior, 2) citation quality as trust lever, 3) failure modes when policy docs are outdated |
| Week 4 | Sat | Advanced RAG | **Procurement Contract Intelligence**: compares supplier clauses against enterprise standards | 1) Query rewriting for ambiguous legal language, 2) reranking impact on clause relevance, 3) measurable reduction in manual review time |
| Week 4 | Sun | AI agents intro/patterns | **Travel Disruption Recovery Agent**: rebooks flights/hotels during weather disruptions | 1) Planner/tool/validator role split, 2) timeout/retry strategy during API instability, 3) human approval gates for costly actions |
| Week 5 | Sat | LangGraph orchestration | **Hospital Discharge Orchestration**: multi-step workflow for discharge summaries, medication checks, and patient instructions | 1) Why stateful orchestration matters, 2) where human-in-loop checkpoints are required, 3) auditability of each node transition |
| Week 5 | Sun | MCP and modular AI tools | **Retail Store Ops Copilot**: MCP tools for stock checks, incident logs, and shift status | 1) Tool contracts/schema discipline, 2) failure fallback when a tool is offline, 3) microservice boundaries for safe scaling |
| Week 6 | Sat | Full advanced AI app workflow | **Banking Relationship Manager Copilot**: unified assistant for client notes, policy retrieval, and task automation | 1) release-readiness checklist before production, 2) observability and incident response design, 3) rollout strategy (pilot -> staged -> full) |
| Week 6 | Sun | Offline model setup + capstone review | **Factory Floor Assistant (Air-Gapped)**: local LLM for maintenance SOPs in low-connectivity environments | 1) privacy/compliance reasons for offline inference, 2) quality-latency-cost trade-offs vs cloud, 3) decision framework for hybrid deployment |

Optional rotation rule for uniqueness:
- Do not repeat an industry two weeks in a row.
- Alternate between regulated domains (finance/health/legal) and operational domains (retail/travel/manufacturing).
- End each discussion with one "what could go wrong in production?" question.

---

*Last updated: 2026-05-05 - expanded top-level inventory/catalog, added syllabus day-wise plan, curriculum v2 gap coverage, and real-life use case discussion bank.*
