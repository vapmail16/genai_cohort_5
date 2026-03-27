"""Smoke test: theory page module imports and delegates to similarity_math."""


def test_show_similarity_math_theory_is_callable():
    from similarity_theory_page import show_similarity_math_theory

    assert callable(show_similarity_math_theory)
