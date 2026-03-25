# Oxford MCP Session & Cohort 5 — Implementation Plan

**Status:** Planning only — implement step by step after sign-off.  
**Audience:** Oxford session (prestigious); later reuse for private Cohort 5 when you reach MCP.  
**Related assets:** `mcp/` root (e.g. `mcp_oxford_final.pdf`, `mcp_oxford_final.pptx`, architecture HTML), `capstone_project/` (IT Support Agent).

---

## Goals (what we are building)

1. **Open with E2E** — Show upfront what the audience will see end-to-end by the end of the session.
2. **Interactive “plain APIs”** — A dedicated place (e.g. new tab in the capstone app) to exercise LLM, DB, and backend calls with visible **status, inputs, process, and outputs** (teaching tool, not just Postman).
3. **Compare with MCP (interactive)** — Same user intents shown as direct HTTP/API style vs MCP tool calls, side by side or tabbed.
4. **MCP architecture & usage (theory)** — Short, interactive-friendly explanation (expandable sections or a simple checklist UI — design TBD).
5. **MCP implementation (live)** — AI agent + MCP client + MCP server; **end-to-end works**; ability to **open the code** and walk through how calls are made under the hood.
6. **Slides (HMRC style)** — Very little text, very simple, calm visuals; government-adjacent clarity.
7. **Teaching materials** — Code explanation document in the same spirit as other cohort teaching samples (see `rag_understanding/`, `langchain_openai/`).
8. **Anchor project** — Build on the **Cohort 5 IT Support** capstone; optionally reference or import patterns from **genai_cohort_4** (separate repo/path) only where clearly labelled.

**Cross-cutting:** Verify and align **RAG** (likely working) and **agents / MCP path** (may be partially wired or documented inconsistently) before promising them in the talk.

### Session scope — main IT Support chat (Task 5)

Implemented demo tracks in the **floating chat** (`Chatbot` + `POST /chat`): **(1) plain LLM**, **(2) KB RAG** (IT KB / Qdrant), **(3) DB RAG** (`rag_db` / alias `rag_structured` — tickets + messages → Qdrant `it_support_db`), **(4) agentic MCP** (`ActionAgent`; stdio MCP when `USE_REAL_MCP=1`). For a **shorter Oxford talk**, you may skip demonstrating the DB RAG button and stick to three tracks; the API still supports `demo_track: rag_db` for advanced cohorts.

---

## What “brilliant” looks like (Oxford + large room)

- **One clear story** — Plain APIs → same flows via MCP → live agent + tools.
- **Promise in ~90 seconds** — What they will see E2E by the end.
- **Live demo as spine** — Slides support the demo; demo does not depend on slides to rescue you.
- **Honest boundaries** — What MCP is and is not (protocol for tools/resources/prompts; not a substitute for good API design or automatic security).
- **Rehearsal** — Two full dry runs on the **same machine** as Oxford; **backup**: 60s screen recording + PDF deck if live fails.

---

## Narrative arc (session blocks)

| Block | Content | Audience takeaway |
|-------|---------|-------------------|
| 1 | E2E preview | Mental model + motivation |
| 2 | Interactive APIs (LLM, DB, backend) | How requests feel **without** MCP |
| 3 | Same flows vs MCP | Same outcome, different **shape** (discovery, tool contract, host) |
| 4 | MCP architecture & usage | Transport, host, tools/resources, security mental model |
| 5 | Working stack: agents + client + server + “under the hood” | Trust: point at real code path |
| 6 | HMRC-style deck | Minimal text; one idea per slide |
| 7 | Cohort 5 pack | Reuse for private cohort: script + doc + sample project layout |

---

## Phase 0 — Truth audit (do before major UI or slide rewrites)

**Objective:** One honest paragraph: *RAG does X; chat path does Y; orchestrator/agents do Z; MCP is wired as W.*

| Step | Task | Done |
|------|------|------|
| 0.1 | Pick **one** canonical doc (e.g. `capstone_project/docs/HOW_IT_WORKS.md`) and add “Last verified: [date]” or create `mcp/SESSION_OVERVIEW.md` as single pointer into code. | ☐ |
| 0.2 | Trace **production path**: `POST /chat` (or equivalent) → orchestrator vs simple RAG; document in one place. | ☐ |
| 0.3 | Confirm **Action Agent** + **MCP** in production vs tests only; reconcile with `MCP_AND_FRONTEND_COMPLETE.md` vs `action_agent.py` comments. | ☐ |
| 0.4 | **RAG:** Confirm ingest, Qdrant, retriever on the **Oxford laptop** (same env as live demo). | ☐ |
| 0.5 | Write **one-page “system truth”** matrix: implemented / simulated / not wired (for speaker only). | ☐ |

**Risk:** Internal docs disagree (some say MCP complete, some say placeholder). This phase eliminates surprise during Q&A.

---

## Phase 1 — Session bundle folder structure

**Location:** `genai_cohort_5/mcp/` (session bundle lives alongside deck exports and HTML).

| Asset | Purpose |
|-------|---------|
| `OXFORD_MCP_SESSION_PLAN.md` | This file — roadmap and phases. |
| `mcp_oxford_final.pdf` / `mcp_oxford_final.pptx` | Exported deck + **PDF** backup. |
| `teaching_script.md` | Timing, demo clicks, what to say, fallback if demo fails. |
| `diagrams/` | 3–5 images max: (a) classic client → API → LLM/DB, (b) MCP host + client + server, (c) capstone call chain. |
| `cohort5_bridge.md` | Map session to Cohort 5 “MCP week” for private reuse. |

**genai_cohort_4:** Copy or link only assets you will actually demo; label “Cohort 4 sample” vs “Cohort 5 capstone” to avoid confusion.

---

## Phase 2 — Interactive “API playground” (capstone new tab)

**Design intent:** Teach **request → context/auth → (tokens/budget if shown) → response → status** — not to replace Postman.

| Panel (conceptual) | Notes |
|--------------------|--------|
| LLM | Structured fields or JSON; model name; temperature; **never** show full API key in UI. |
| Backend | `GET /health`, `POST /chat` with fixed example payload; status + body. |
| DB | Read-only or sanitised example tied to your stack; or mocked “DB result” if safer live. |

**Comparison view (MCP vs APIs):** Same intent (e.g. “check VPN”, “create ticket”): **Direct HTTP** vs **MCP tool name + args + result**; optional **timeline** of steps.

**Dependency:** Complete Phase 0 so the tab does not demo a path that contradicts production.

**Main IT Support chat (demo menu):** Oxford / cohort **interactive tracks** live in the floating **Chatbot** → `POST /chat` with `demo_mode` and `demo_track`: **plain LLM**, **KB RAG** (`rag_kb`, Qdrant IT KB), **DB RAG** (`rag_db`, tickets + messages → collection `it_support_db`), **agentic MCP** (`agentic_mcp`, `ActionAgent`; real stdio MCP when `USE_REAL_MCP=1`). The teaching **API basics** lab stays under `/teaching/...` and is separate from this menu.

---

## Phase 3 — MCP theory + live implementation

**Theory (interactive):** One architecture slide + one live sequence; avoid long slide decks.

**Live implementation checklist:**

| Step | Task | Done |
|------|------|------|
| 3.1 | MCP server runs; tools listed; **one** tool executes successfully. | ☐ |
| 3.2 | Show **stdio or logs** in terminal while narrating (“here is the message boundary”). | ☐ |
| 3.3 | **Under the hood:** Annotated path in teaching doc — `mcp_server` registration → Python client → agent/orchestrator → user. | ☐ |
| 3.4 | If full wiring lags, **scope honestly**: “Production chat uses RAG; MCP tool path shown in this script/branch” — still credible if documented. | ☐ |

---

## Phase 4 — HMRC-style deck

- **6–10 slides** for ~45–60 minutes (adjust for slot); rest = demo + Q&A.
- **One short title + one visual** per slide; body **≤ 2 lines** where possible.
- Neutral palette, high contrast, minimal animation.
- Mirror `teaching_script.md` sections: Hook → Problem → APIs → MCP idea → Live → Q&A.
- Always keep **PDF export** next to source.

---

## Phase 5 — Code explanation document

Mirror LangChain sample style:

- Purpose and prerequisites  
- Run order (services, env vars)  
- File map (what each file is for)  
- “What to say when opening file X”  
- Troubleshooting table  
- **Demo script:** exact click order + which file open in IDE

---

## Phase 6 — Rehearsal & Oxford polish

| Step | Task | Done |
|------|------|------|
| 6.1 | Dry run 1 — timeboxed; log every stumble. | ☐ |
| 6.2 | Dry run 2 — one external viewer; collect “what was unclear?” | ☐ |
| 6.3 | Backup: 60s screen recording of MCP tool flow + static architecture slide. | ☐ |
| 6.4 | Q&A prep: security, MCP vs REST, vs function calling, stdio vs HTTP, lock-in. | ☐ |

---

## Risk register

| Risk | Mitigation |
|------|------------|
| Docs say MCP “done” but code simulates | Phase 0 audit; align narrative to code |
| Live demo fails | Recording + PDF + smoke-test script |
| API playground too broad | Split “teaching” vs “product chat” clearly |
| Over time | Hard stops at 15 / 30 / 45 min in teaching script |

---

## Suggested implementation order (summary)

1. **Phase 0** — Truth audit; one-page system matrix.  
2. **Phase 1** — Session folder assets + teaching script skeleton + diagram list.  
3. **Phase 4** — Deck skeleton (refine after demo path is verified).  
4. **Phase 2–3** — API playground + MCP wiring per audit.  
5. **Phase 5** — Code explanation doc tied to real files.  
6. **Phase 6** — Rehearsal + backups.

---

## Changelog

| Date | Note |
|------|------|
| *(add as you implement)* | |

---

*End of plan — implement step by step; no code required in this document.*
