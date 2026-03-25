"""Single LLM call with no retrieval — for Oxford \"plain LLM\" demo track."""

from __future__ import annotations

from typing import Any, Dict, Tuple

PLAIN_LLM_PRESENTER: Dict[str, str] = {
    "file": "backend/chat_demo/plain_llm.py",
    "symbol": "run_plain_llm",
    "note": "One ChatOpenAI.invoke with a short IT support system-style prompt; no RAG.",
}


def run_plain_llm(llm: Any, user_message: str) -> Tuple[str, Dict[str, str]]:
    prompt = f"""You are a concise IT support assistant at Acme Corp.
User message: {user_message}

Reply briefly and professionally."""
    out = llm.invoke(prompt)
    text = getattr(out, "content", str(out))
    return text, PLAIN_LLM_PRESENTER
