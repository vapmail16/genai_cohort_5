"""TDD: compute_chat_reply routes demo tracks vs legacy RAG chat."""

from typing import List, Tuple
from unittest.mock import MagicMock

import pytest

pytestmark = pytest.mark.unit


def _legacy_simple(msg: str) -> str:
    return f"legacy:{msg}"


class TestComputeChatReply:
    def test_menu_track_returns_markdown_three_options(self):
        from backend.chat_demo.router import compute_chat_reply

        llm = MagicMock()
        get_rag = MagicMock()
        agent = MagicMock()

        out = compute_chat_reply(
            message="Hi",
            user_email="a@b.com",
            demo_mode=True,
            demo_track="menu",
            llm=llm,
            get_rag_context=get_rag,
            generate_simple_response_fn=_legacy_simple,
            action_agent=agent,
            db_session=MagicMock(),
            get_db_rag_context_fn=MagicMock(),
        )

        assert out["demo_track"] == "menu"
        assert "Plain LLM" in out["response"]
        assert "Knowledge base RAG" in out["response"] or "RAG" in out["response"]
        assert "DB RAG" in out["response"] or "rag_db" in out["response"]
        assert "Agentic MCP" in out["response"]
        assert out["presenter"] is None
        assert out["mcp_trace"] is None
        llm.invoke.assert_not_called()
        get_rag.assert_not_called()

    def test_plain_llm_does_not_call_get_rag_context(self):
        from backend.chat_demo.router import compute_chat_reply

        class _Msg:
            content = "ok"

        llm = MagicMock()
        llm.invoke.return_value = _Msg()
        get_rag = MagicMock()
        agent = MagicMock()

        out = compute_chat_reply(
            message="Say hi in one word.",
            user_email="a@b.com",
            demo_mode=True,
            demo_track="plain_llm",
            llm=llm,
            get_rag_context=get_rag,
            generate_simple_response_fn=_legacy_simple,
            action_agent=agent,
            db_session=MagicMock(),
            get_db_rag_context_fn=MagicMock(),
        )

        assert out["demo_track"] == "plain_llm"
        get_rag.assert_not_called()
        assert out["presenter"] is not None
        assert out["presenter"].get("file", "").endswith("plain_llm.py")

    def test_rag_kb_calls_get_rag_context(self):
        from backend.chat_demo.router import compute_chat_reply

        class _Msg:
            content = "answer from kb"

        llm = MagicMock()
        llm.invoke.return_value = _Msg()

        def get_rag(q: str, k: int = 5) -> Tuple[str, List[str]]:
            return ("chunk about VPN", ["vpn.md"])

        agent = MagicMock()

        out = compute_chat_reply(
            message="VPN error",
            user_email="a@b.com",
            demo_mode=True,
            demo_track="rag_kb",
            llm=llm,
            get_rag_context=get_rag,
            generate_simple_response_fn=_legacy_simple,
            action_agent=agent,
            db_session=MagicMock(),
            get_db_rag_context_fn=MagicMock(),
        )

        assert out["demo_track"] == "rag_kb"
        assert "answer from kb" in out["response"]
        assert "vpn.md" in (out.get("sources") or [])

    def test_agentic_mcp_uses_action_agent(self):
        from backend.chat_demo.router import compute_chat_reply

        llm = MagicMock()
        get_rag = MagicMock()
        agent = MagicMock()
        agent.execute_action.return_value = {
            "success": True,
            "tool_used": "check_vpn_status",
            "message": "VPN ok",
            "result": {"status": "connected"},
            "mcp_transport": "simulated",
        }

        out = compute_chat_reply(
            message="Check my VPN status",
            user_email="u@acme.com",
            demo_mode=True,
            demo_track="agentic_mcp",
            llm=llm,
            get_rag_context=get_rag,
            generate_simple_response_fn=_legacy_simple,
            action_agent=agent,
            db_session=MagicMock(),
            get_db_rag_context_fn=MagicMock(),
        )

        assert out["demo_track"] == "agentic_mcp"
        agent.execute_action.assert_called_once()
        assert out["mcp_trace"]["tool"] == "check_vpn_status"
        assert out["mcp_trace"]["success"] is True
        assert out["mcp_trace"]["transport"] == "simulated"
        get_rag.assert_not_called()

    def test_legacy_path_when_no_effective_track(self):
        from backend.chat_demo.router import compute_chat_reply

        class _Msg:
            content = "rag answer"

        llm = MagicMock()
        llm.invoke.return_value = _Msg()
        get_rag = MagicMock(
            return_value=("some context", ["doc.md"])
        )
        agent = MagicMock()

        out = compute_chat_reply(
            message="WiFi slow",
            user_email="a@b.com",
            demo_mode=False,
            demo_track=None,
            llm=llm,
            get_rag_context=get_rag,
            generate_simple_response_fn=_legacy_simple,
            action_agent=agent,
            db_session=MagicMock(),
            get_db_rag_context_fn=MagicMock(),
        )

        assert out["demo_track"] is None
        get_rag.assert_called_once()
        assert out["response"] == "rag answer"

    def test_rag_db_calls_get_db_rag_context(self):
        from backend.chat_demo.router import compute_chat_reply

        class _Msg:
            content = "from tickets"

        llm = MagicMock()
        llm.invoke.return_value = _Msg()
        get_rag = MagicMock()
        agent = MagicMock()
        db_sess = MagicMock()

        def get_db_rag(db, q: str, k: int = 5):
            return ("ticket #1 VPN outage", ["db_ticket:1"])

        out = compute_chat_reply(
            message="Any VPN tickets?",
            user_email="a@b.com",
            demo_mode=True,
            demo_track="rag_db",
            llm=llm,
            get_rag_context=get_rag,
            generate_simple_response_fn=_legacy_simple,
            action_agent=agent,
            db_session=db_sess,
            get_db_rag_context_fn=get_db_rag,
        )

        assert out["demo_track"] == "rag_db"
        assert "from tickets" in out["response"]
        get_rag.assert_not_called()
        assert out["presenter"] and "db_retriever" in out["presenter"].get("file", "")

    def test_legacy_falls_back_to_simple_when_no_context(self):
        from backend.chat_demo.router import compute_chat_reply

        llm = MagicMock()
        get_rag = MagicMock(return_value=("", []))
        agent = MagicMock()

        out = compute_chat_reply(
            message="WiFi slow",
            user_email="a@b.com",
            demo_mode=False,
            demo_track=None,
            llm=llm,
            get_rag_context=get_rag,
            generate_simple_response_fn=_legacy_simple,
            action_agent=agent,
            db_session=MagicMock(),
            get_db_rag_context_fn=MagicMock(),
        )

        assert out["response"] == "legacy:WiFi slow"
        llm.invoke.assert_not_called()
