"""
Smoke test for advanced_rag_tab.py — TDD RED phase.
Verifies the module is importable and show_advanced_rag() is callable.
"""
import pytest


class TestAdvancedRagTabImport:
    def test_module_imports(self):
        import advanced_rag_tab  # noqa: F401

    def test_show_advanced_rag_callable(self):
        import advanced_rag_tab
        assert callable(advanced_rag_tab.show_advanced_rag)

    def test_section_helpers_defined(self):
        """All internal section functions must exist."""
        import advanced_rag_tab
        for fn in [
            "_section_pipeline",
            "_section_latest_principles",
            "_section_advanced_features",
            "_section_evolution",
            "_section_enterprise",
            "_section_ragas",
            "_section_pitfalls",
            "_section_problem_statements",
        ]:
            assert hasattr(advanced_rag_tab, fn), f"Missing: {fn}"
            assert callable(getattr(advanced_rag_tab, fn))
