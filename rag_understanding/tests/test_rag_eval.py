"""
Tests for RAGAS-style evaluation — TDD RED phase.
evaluate_rag_answer() must not exist yet when these are first run.

We implement the 4 RAGAS metrics using direct LLM calls (not the ragas library)
so the logic is transparent and testable without heavy dependencies.
"""
from __future__ import annotations
from unittest.mock import MagicMock, patch
import pytest
from rag_pipeline import evaluate_rag_answer


def _mock_score_response(score: float, reason: str = "test reason"):
    import json
    resp = MagicMock()
    resp.choices = [MagicMock()]
    resp.choices[0].message.content = json.dumps({"score": score, "reason": reason})
    return resp


class TestEvaluateRagAnswer:
    def test_returns_dict_with_core_metrics(self):
        with patch("rag_pipeline.openai_chat", return_value=_mock_score_response(0.9)):
            result = evaluate_rag_answer(
                query="What is GDPR?",
                answer="GDPR is the General Data Protection Regulation.",
                contexts=["GDPR stands for General Data Protection Regulation."],
                openai_api_key="sk-test",
            )
        assert isinstance(result, dict)
        for key in ("faithfulness", "answer_relevancy", "context_precision"):
            assert key in result, f"Missing key: {key}"

    def test_scores_are_floats_between_0_and_1(self):
        with patch("rag_pipeline.openai_chat", return_value=_mock_score_response(0.85)):
            result = evaluate_rag_answer(
                query="What is GDPR?",
                answer="GDPR is a regulation.",
                contexts=["GDPR is a European data protection law."],
                openai_api_key="sk-test",
            )
        for key in ("faithfulness", "answer_relevancy", "context_precision"):
            assert 0.0 <= result[key] <= 1.0, f"{key} out of range: {result[key]}"

    def test_includes_reasons(self):
        with patch("rag_pipeline.openai_chat", return_value=_mock_score_response(0.8, "Good grounding")):
            result = evaluate_rag_answer(
                query="q", answer="a", contexts=["ctx"],
                openai_api_key="sk-test",
            )
        assert "reasons" in result
        assert isinstance(result["reasons"], dict)

    def test_with_ground_truth_adds_context_recall(self):
        with patch("rag_pipeline.openai_chat", return_value=_mock_score_response(0.7)):
            result = evaluate_rag_answer(
                query="What is GDPR?",
                answer="GDPR is a regulation.",
                contexts=["GDPR is a European data protection law."],
                ground_truth="GDPR stands for General Data Protection Regulation, a EU law.",
                openai_api_key="sk-test",
            )
        assert "context_recall" in result

    def test_no_api_key_raises(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            evaluate_rag_answer("q", "a", ["ctx"], openai_api_key=None)

    def test_empty_answer_returns_zero_faithfulness(self):
        with patch("rag_pipeline.openai_chat", return_value=_mock_score_response(0.0)):
            result = evaluate_rag_answer(
                query="What is GDPR?",
                answer="",
                contexts=["some context"],
                openai_api_key="sk-test",
            )
        assert result["faithfulness"] == 0.0

    def test_handles_malformed_llm_json(self):
        """If LLM returns non-JSON, score should default to 0 not crash."""
        resp = MagicMock()
        resp.choices = [MagicMock()]
        resp.choices[0].message.content = "I cannot evaluate this."
        with patch("rag_pipeline.openai_chat", return_value=resp):
            result = evaluate_rag_answer(
                query="q", answer="a", contexts=["ctx"],
                openai_api_key="sk-test",
            )
        for key in ("faithfulness", "answer_relevancy", "context_precision"):
            assert result[key] == 0.0
