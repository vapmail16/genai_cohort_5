"""TDD: plain LLM path (no retrieval) for demo track."""

from unittest.mock import Mock

import pytest

pytestmark = pytest.mark.unit


class TestRunPlainLlm:
    def test_invokes_llm_and_returns_presenter_metadata(self):
        from backend.chat_demo.plain_llm import run_plain_llm, PLAIN_LLM_PRESENTER

        class _Msg:
            def __init__(self, content: str):
                self.content = content

        llm = Mock()
        llm.invoke.return_value = _Msg("Short IT tip: use a password manager.")

        text, presenter = run_plain_llm(llm, "Give one password tip.")

        assert text == "Short IT tip: use a password manager."
        assert presenter == PLAIN_LLM_PRESENTER
        llm.invoke.assert_called_once()
        call_kw = llm.invoke.call_args[0][0]
        assert "password tip" in call_kw.lower() or "Give one password" in call_kw
