"""Route /chat-style messages to menu, plain LLM, KB RAG, agentic MCP, or legacy RAG."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

from backend.chat_demo.plain_llm import run_plain_llm
from backend.chat_demo.tracks import resolve_effective_track

RAG_KB_PRESENTER: Dict[str, str] = {
    "file": "backend/rag/retriever.py",
    "symbol": "get_rag_context",
    "note": "Qdrant KB retrieval + grounded prompt in router._kb_rag_reply.",
}

AGENTIC_MCP_PRESENTER: Dict[str, str] = {
    "file": "backend/agents/action_agent.py",
    "symbol": "ActionAgent.execute_action",
    "note": "LLM/tool selection then MCP tool execution (stdio when USE_REAL_MCP=1).",
}

RAG_DB_PRESENTER: Dict[str, str] = {
    "file": "backend/rag/db_retriever.py",
    "symbol": "get_db_rag_context",
    "note": "Tickets + messages embedded into Qdrant collection it_support_db.",
}


def _demo_menu_markdown() -> str:
    return """### Demo tracks

Pick a track using the **buttons** in the chat (they set `demo_track` on the request), or send a message starting with `__DEMO__:<track>`.

1. **Plain LLM** — `demo_track`: `plain_llm` — model only, no knowledge base retrieval. *Open `backend/chat_demo/plain_llm.py` when presenting.*

2. **Knowledge base RAG** — `demo_track`: `rag_kb` — retrieve from the IT KB (Qdrant) then answer.

3. **DB RAG (structured)** — `demo_track`: `rag_db` (alias `rag_structured`) — retrieve from embedded **tickets and chat messages** in SQLite (collection `it_support_db`).

4. **Agentic MCP** — `demo_track`: `agentic_mcp` — the agent chooses an IT tool (VPN check, password reset, etc.) and runs it. *Open `backend/agents/action_agent.py` when presenting.*

Say **Hi** again any time with demo mode on to see this menu."""


def _db_rag_reply(llm: Any, message: str, context: str) -> str:
    prompt = f"""You are an IT support agent at Acme Corp. Use the following context from **internal tickets and chat logs** (database RAG). Be concise and professional.

Context:
{context}

User Question: {message}

If the context does not contain the answer, say so. Cite ticket or message ids when present in the context.

Answer:"""
    return llm.invoke(prompt).content


def _kb_rag_reply(
    llm: Any,
    message: str,
    context: str,
    sources: List[str],
) -> str:
    prompt = f"""You are an IT support agent at Acme Corp. Use the following context from our knowledge base to answer the user's question. Be helpful, concise, and professional.

Context from Knowledge Base:
{context}

User Question: {message}

Instructions:
- Provide a clear, step-by-step answer based on the context
- If the context doesn't contain relevant information, say so politely
- Include specific details like URLs, commands, or error codes when available
- Be friendly and professional

Answer:"""
    return llm.invoke(prompt).content


def compute_chat_reply(
    *,
    message: str,
    user_email: str,
    demo_mode: bool,
    demo_track: Optional[str],
    llm: Any,
    get_rag_context: Callable[..., Tuple[str, List[str]]],
    generate_simple_response_fn: Callable[[str], str],
    action_agent: Any,
    db_session: Any = None,
    get_db_rag_context_fn: Optional[Callable[..., Tuple[str, List[str]]]] = None,
) -> Dict[str, Any]:
    """
    Pure routing + generation. Caller persists messages and builds ChatResponse.

    Returns dict with keys: response, sources, demo_track, presenter, mcp_trace.
    """
    effective = resolve_effective_track(
        message=message,
        demo_track_field=demo_track,
        demo_mode=demo_mode,
    )

    if effective == "menu":
        return {
            "response": _demo_menu_markdown(),
            "sources": None,
            "demo_track": "menu",
            "presenter": None,
            "mcp_trace": None,
        }

    if effective == "plain_llm":
        text, presenter = run_plain_llm(llm, message)
        return {
            "response": text,
            "sources": ["plain_llm"],
            "demo_track": "plain_llm",
            "presenter": presenter,
            "mcp_trace": None,
        }

    if effective == "rag_kb":
        try:
            context, sources = get_rag_context(message, k=5)
        except Exception:
            context, sources = "", ["fallback"]
        if not context:
            return {
                "response": generate_simple_response_fn(message),
                "sources": sources or ["no_sources"],
                "demo_track": "rag_kb",
                "presenter": RAG_KB_PRESENTER,
                "mcp_trace": None,
            }
        text = _kb_rag_reply(llm, message, context, sources)
        return {
            "response": text,
            "sources": sources,
            "demo_track": "rag_kb",
            "presenter": RAG_KB_PRESENTER,
            "mcp_trace": None,
        }

    if effective == "rag_db":
        if db_session is None or get_db_rag_context_fn is None:
            return {
                "response": "Database RAG is not available (no DB session).",
                "sources": ["error"],
                "demo_track": "rag_db",
                "presenter": RAG_DB_PRESENTER,
                "mcp_trace": None,
            }
        try:
            context, sources = get_db_rag_context_fn(db_session, message, k=5)
        except Exception:
            context, sources = "", ["fallback"]
        if not context:
            return {
                "response": generate_simple_response_fn(message),
                "sources": sources or ["no_sources"],
                "demo_track": "rag_db",
                "presenter": RAG_DB_PRESENTER,
                "mcp_trace": None,
            }
        text = _db_rag_reply(llm, message, context)
        return {
            "response": text,
            "sources": sources,
            "demo_track": "rag_db",
            "presenter": RAG_DB_PRESENTER,
            "mcp_trace": None,
        }

    if effective == "agentic_mcp":
        result = action_agent.execute_action(
            request=message,
            user_email=user_email,
            classification=None,
        )
        text = result.get("message") or str(result)
        raw = result.get("result")
        summary = str(raw)[:500] if raw is not None else ""
        mcp_trace = {
            "tool": result.get("tool_used"),
            "success": result.get("success"),
            "result_summary": summary,
            "transport": result.get("mcp_transport"),
        }
        return {
            "response": text,
            "sources": ["agentic_mcp"],
            "demo_track": "agentic_mcp",
            "presenter": AGENTIC_MCP_PRESENTER,
            "mcp_trace": mcp_trace,
        }

    # Legacy: same as previous /chat behaviour
    try:
        context, sources = get_rag_context(message, k=5)
    except Exception:
        context, sources = "", ["fallback"]

    if context:
        text = _kb_rag_reply(llm, message, context, sources)
        return {
            "response": text,
            "sources": sources if sources else ["no_sources"],
            "demo_track": None,
            "presenter": None,
            "mcp_trace": None,
        }

    return {
        "response": generate_simple_response_fn(message),
        "sources": sources if sources else ["no_sources"],
        "demo_track": None,
        "presenter": None,
        "mcp_trace": None,
    }
