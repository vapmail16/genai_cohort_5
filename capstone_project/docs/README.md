# IT Support Agent - GenAI Cohort 5 Capstone Project

## 🎯 Project Overview

An intelligent IT Support Agent built using **Test-Driven Development (TDD)** principles. This application helps employees diagnose issues, search the knowledge base, create tickets, and execute fixes—all powered by RAG (Retrieval-Augmented Generation), LangGraph agents, and MCP tools.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  React Frontend                      │
│         (Chat UI + Ticket Dashboard)                 │
└────────────────────┬────────────────────────────────┘
                     │ HTTP / SSE streaming
┌────────────────────▼────────────────────────────────┐
│              FastAPI Backend                         │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │           LangGraph Orchestrator             │   │
│  │                                              │   │
│  │  ┌──────────┐ ┌──────────┐ ┌─────────────┐  │   │
│  │  │ Triage   │ │   RAG    │ │  Ticket     │  │   │
│  │  │  Agent   │→│  Agent   │ │  Agent      │  │   │
│  │  └──────────┘ └──────────┘ └─────────────┘  │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────┐  ┌──────────────────────────┐ │
│  │  Chroma Vector   │  │    MCP Tool Server       │ │
│  │  Store (RAG)     │  │  (tickets, sys-check,    │ │
│  │                  │  │   password-reset, logs)  │ │
│  └──────────────────┘  └──────────────────────────┘ │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │        SQLite  (tickets + chat history)      │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🧪 **Built with Test-Driven Development (TDD)**

This project follows **gold standard TDD** practices:

### **Red → Green → Refactor**

1. **🔴 RED**: Write a failing test first
2. **🟢 GREEN**: Write minimal code to pass the test
3. **🔵 REFACTOR**: Improve code while keeping tests green

**Current Status**: 🔴 **RED PHASE**
- ✅ 22 database model tests written
- ❌ 0 tests passing (expected - no implementation yet!)
- 📋 Ready to implement code to make tests green

### **Why TDD?**

- **Confidence**: Every feature has tests before deployment
- **Quality**: Bugs caught early in development
- **Documentation**: Tests describe how the system works
- **Refactoring**: Safe to improve code with test coverage
- **Design**: Forces thinking about interfaces before implementation

---

## 📁 Project Structure

```
it-support-agent/
├── backend/
│   ├── database/          # (To be implemented - TDD Green phase)
│   │   ├── __init__.py
│   │   ├── models.py      # Ticket, Message, Enums
│   │   └── crud.py        # Database operations
│   ├── rag/               # (To be implemented)
│   │   ├── __init__.py
│   │   ├── ingest.py      # Document ingestion
│   │   ├── retriever.py   # RAG retrieval & generation
│   │   └── docs/          # Knowledge base documents
│   │       ├── wifi_troubleshooting.md
│   │       ├── vpn_setup_guide.md
│   │       ├── password_reset_sop.md
│   │       ├── laptop_setup_checklist.md
│   │       ├── common_error_codes.md
│   │       └── software_install_policies.md
│   ├── agents/            # (To be implemented)
│   │   ├── __init__.py
│   │   ├── orchestrator.py    # LangGraph orchestrator
│   │   ├── triage_agent.py    # Issue classification
│   │   ├── rag_agent.py       # Knowledge base search
│   │   ├── ticket_agent.py    # Ticket creation
│   │   └── response_agent.py  # Response formatting
│   ├── mcp_server/        # (To be implemented)
│   │   ├── server.ts
│   │   └── tools/
│   ├── main.py            # FastAPI app (To be implemented)
│   ├── requirements.txt   # ✅ Created
│   └── .env.example       # ✅ Created
├── frontend/              # (Week 8)
│   ├── src/
│   │   ├── components/
│   │   └── App.jsx
│   └── package.json
├── tests/                 # ✅ Test infrastructure created
│   ├── conftest.py        # ✅ Shared fixtures
│   ├── unit/              # ✅ Unit tests
│   │   ├── test_database_models.py  # ✅ 22 tests written (Red phase)
│   │   ├── test_database_crud.py    # (Next)
│   │   ├── test_rag_ingest.py
│   │   ├── test_rag_retriever.py
│   │   ├── test_agent_triage.py
│   │   ├── test_agent_rag.py
│   │   ├── test_agent_ticket.py
│   │   └── test_agent_response.py
│   ├── integration/       # Integration tests
│   │   ├── test_rag_pipeline.py
│   │   ├── test_agent_orchestrator.py
│   │   └── test_api_endpoints.py
│   ├── e2e/               # End-to-end tests
│   │   └── test_chat_workflows.py
│   └── ai_quality/        # AI quality tests
│       ├── test_ragas_metrics.py
│       └── test_hallucination_detection.py
├── IT_SUPPORT_TDD_SPEC.md      # ✅ TDD specification
├── TDD_PROGRESS.md             # ✅ Progress tracker
├── it_support_capstone_plan.md # ✅ Original plan
├── pytest.ini                  # ✅ Pytest configuration
├── .gitignore                  # ✅ Created
├── docker-compose.yml          # (Week 10)
└── README.md                   # ✅ This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+ (for MCP server)
- OpenAI API key (or Ollama for local models)

### Installation

```bash
# 1. Clone the repository
cd /Users/user/Desktop/AI/projects/genai_cohort_5/capstone_project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENAI_API_KEY

# 5. Run tests (currently in RED phase - expect failures!)
pytest tests/unit/test_database_models.py -v
```

**Expected Output (Red Phase)**:
```
tests/unit/test_database_models.py::TestTicketModel::test_create_ticket_with_all_required_fields FAILED
tests/unit/test_database_models.py::TestTicketModel::test_create_ticket_without_user_email_raises_error FAILED
...
===================== 22 failed in 0.15s =====================
```

This is **perfect**! It means tests are written and failing because we haven't implemented the code yet.

### Next Step: Make Tests Pass (Green Phase)

```bash
# Implement backend/database/models.py
# Then run tests again
pytest tests/unit/test_database_models.py -v

# Expected: All tests should pass ✅
```

---

## 📖 Documentation

- **[IT_SUPPORT_TDD_SPEC.md](IT_SUPPORT_TDD_SPEC.md)**: Comprehensive TDD specification
- **[TDD_PROGRESS.md](TDD_PROGRESS.md)**: Current progress and next steps
- **[it_support_capstone_plan.md](it_support_capstone_plan.md)**: Original project plan

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Priority P0 (critical) tests
pytest -m priority_p0

# Database tests
pytest -m database

# AI quality tests (slower)
pytest tests/ai_quality/ --slow
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=backend --cov-report=html

# Open coverage report
open htmlcov/index.html
```

### Current Test Statistics

- **Total Tests**: 22
- **Tests Passing**: 0 (Red phase - expected!)
- **Tests Failing**: 22 (Red phase - expected!)
- **Coverage**: 0% (No implementation yet)

**Priority Breakdown:**
- P0 (Critical): 13 tests
- P1 (High): 8 tests
- P2 (Medium): 1 test

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + Tailwind CSS |
| API | FastAPI + SSE streaming |
| Orchestration | LangGraph (multi-agent) |
| RAG | LangChain LCEL + Chroma |
| Embeddings | OpenAI / nomic-embed-text |
| LLM | OpenAI GPT-4o / Ollama |
| MCP | TypeScript MCP SDK |
| Database | SQLite + SQLAlchemy |
| Testing | pytest + pytest-cov + RAGAS |
| Deployment | Docker + Railway |

---

## 📝 Development Workflow (TDD)

### For Each New Feature:

1. **Write Test First (Red)** 🔴
   ```bash
   # Create test file
   touch tests/unit/test_new_feature.py

   # Write failing test
   # Run and verify it fails
   pytest tests/unit/test_new_feature.py -v
   ```

2. **Implement Code (Green)** 🟢
   ```bash
   # Write minimal code to pass test
   # Run test again
   pytest tests/unit/test_new_feature.py -v

   # Expected: Test passes ✅
   ```

3. **Refactor (Blue)** 🔵
   ```bash
   # Improve code quality
   # Run tests to ensure nothing broke
   pytest tests/unit/test_new_feature.py -v
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: Add new feature (TDD)"
   ```

---

## 🎯 Current Status & Next Steps

### ✅ Completed

1. TDD specification document created
2. Test infrastructure set up (pytest, fixtures, mocks)
3. 22 database model tests written (Red phase)
4. Golden datasets created for RAG and triage testing
5. Project structure defined

### 🔴 Current Phase: RED (Database Models)

**22 tests written, 0 passing** - Ready for implementation!

### 📋 Next Actions

1. **Implement `backend/database/models.py`** (Green phase)
   - Define Ticket, Message, Enums
   - Run tests: `pytest tests/unit/test_database_models.py`
   - Expected: All 22 tests pass ✅

2. **Write CRUD tests** (Red phase)
   - Create `tests/unit/test_database_crud.py`
   - Write ~15 tests for CRUD operations
   - Run tests: expect failures

3. **Implement `backend/database/crud.py`** (Green phase)
   - Implement all CRUD functions
   - Make tests pass

4. **Continue TDD cycle** for RAG, Agents, API, MCP

---

## 📊 Project Milestones

- [x] **Week 0**: TDD setup and infrastructure
- [ ] **Week 1**: Database layer (TDD)
- [ ] **Week 2-3**: RAG system (TDD)
- [ ] **Week 4-5**: Multi-agent system (TDD)
- [ ] **Week 6**: API endpoints (TDD)
- [ ] **Week 7**: MCP server (TDD)
- [ ] **Week 8**: Frontend + E2E tests
- [ ] **Week 9**: AI quality tests (RAGAS)
- [ ] **Week 10**: Deployment + Documentation

**Target**: 500+ tests, >90% coverage

---

## 🤝 Contributing

This project follows strict TDD practices:

1. **Never write production code without a failing test**
2. **Write the simplest code to pass the test**
3. **Refactor only when tests are green**
4. **All commits must have passing tests**
5. **Code coverage must be >= 90%**

---

## 📄 License

MIT License - GenAI Cohort 5 Capstone Project

---

## 🙏 Acknowledgments

- GenAI Cohort 5 curriculum
- Test-Driven Development principles from Kent Beck
- RAG and LangChain community
- pytest and testing best practices

---

## 🐛 Known Issues

### Issue log (operational)

| Date | What went wrong | How to avoid next time |
|------|-----------------|-------------------------|
| 2026-03-24 | `fastapi.testclient.TestClient` failed with httpx 0.28 (`unexpected keyword argument 'app'` / ASGITransport sync context). | For teaching API tests, call the FastAPI handler directly with injected `db` + mock LLM instead of relying on Starlette TestClient + httpx edge cases. |
| 2026-03-24 | `main.py` used `from database import` while pytest imports `backend.main`, causing `ModuleNotFoundError: database`. | Use `from backend.database import` (and `from backend.rag`) so `uvicorn backend.main:app` and pytest share the same import path from repo root. |
| 2026-03-25 | Teaching UI used a separate dark theme instead of the capstone landing/chat look. | Reuse `LandingPage.css` patterns (`hero`, `agents-section`, `agent-card`, `cta-button`) and add only small overrides in `TeachingPipeline.css`. |
| 2026-03-25 | DELETE success could not return `flow_steps` with HTTP 204 (no body). | Teaching DELETE returns **200 + JSON** with `flow_steps` and a note that RFC often uses 204 without a body. |
| 2026-03-24 | API basics lab looked “washed out”: descriptions, deterministic path, and buttons used slate/grey text. | In `TeachingPipeline.css`, set readable body copy to `#111827` (hero, cards, flow summary/detail, arch controls, method badges); keep gradient primary buttons with white labels. |
| 2026-03-25 | Main-chat demo plan included a fourth track (“RAG structured” over DB). | Superseded: **`rag_db`** is implemented (`backend/rag/db_retriever.py`, Qdrant `it_support_db`). Oxford may still **skip** that button live for a shorter story (`mcp/OXFORD_MCP_SESSION_PLAN.md`). |
| 2026-03-25 | (log) | Main `/chat` demo shipped: `backend/chat_demo/` (`tracks`, `plain_llm`, `router`), `ChatRequest.demo_mode` / `demo_track`, `ChatResponse.presenter` / `mcp_trace`, `Chatbot.tsx` demo strip. |
| 2026-03-25 | `TypeError: Router.__init__() got an unexpected keyword argument 'on_startup'` when starting uvicorn; pip also reported Starlette 1.x vs FastAPI 0.109. | **Pin `starlette>=0.35.0,<0.36.0`** next to `fastapi==0.109.0` in `requirements.txt`. After installing `mcp` or other packages, run `pip install -r backend/requirements.txt` to reconcile. The `_captured_signals` / partial import trace is a **secondary** uvicorn reload crash while imports fail. |
| 2026-03-25 | Root `README.md` and `mcp/OXFORD_MCP_SESSION_PLAN.md` still referenced `mcp/sample documents/` after that folder was removed. | List actual `mcp/` files (PDF/PPTX/DOCX/HTML) in docs; grep for `sample documents` when pruning folders. |
| 2026-03-25 | `ai_agents/langgraph_training_guide.md` used a fixed cohort3 path and `ai_agents_demo` (folder no longer in repo). | Use a generic lab directory (e.g. `~/langgraph_lab`) in setup steps so the guide works for any machine. |

---

## 📞 Support

For questions about TDD approach or project setup:
1. Review `IT_SUPPORT_TDD_SPEC.md`
2. Check `TDD_PROGRESS.md` for current status
3. Read test files for behavior documentation

---

**Last Updated**: 2026-03-11
**Project Status**: 🔴 RED PHASE - Tests written, implementation pending
**Next Milestone**: 🟢 GREEN PHASE - Make database tests pass
