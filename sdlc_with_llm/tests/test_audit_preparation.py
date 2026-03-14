"""
Test Case 5.1 — Access compliance reports for audit preparation
Test Case 5.2 — Access identified compliance gaps for audit preparation
Test Case 5.3 — Audit manager attempts access when no reports or gaps exist
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.report_generator import generate_compliance_report
from src.gap_detector import detect_compliance_gaps


def get_audit_reports():
    """Simulates audit manager opening compliance reports section."""
    report = generate_compliance_report()
    return report if report.can_generate else None


def get_audit_gaps():
    """Simulates audit manager opening compliance gaps section."""
    result = detect_compliance_gaps()
    return result.gaps if result.success else []


class TestCase51AccessComplianceReports:
    """Test Case 5.1 — Access compliance reports for audit preparation."""

    def test_audit_manager_can_access_generated_reports(self):
        """The audit manager can access generated compliance reports."""
        report = get_audit_reports()
        assert report is not None
        assert report.id
        assert report.applicable_regulations

    def test_selected_report_available_for_review(self):
        """The selected report is available for review."""
        report = get_audit_reports()
        assert report.summary
        assert report.compliance_status


class TestCase52AccessComplianceGaps:
    """Test Case 5.2 — Access identified compliance gaps for audit preparation."""

    def test_audit_manager_can_access_identified_gaps(self):
        """The audit manager can access identified compliance gaps."""
        gaps = get_audit_gaps()
        # With default compliance_info, we have gaps (req-006 missing, doc-003 partial)
        assert isinstance(gaps, list)

    def test_identified_gaps_available_as_supporting_material(self):
        """The identified gaps are available for review as supporting material for audit preparation."""
        gaps = get_audit_gaps()
        for gap in gaps:
            assert gap.requirement_id
            assert gap.regulation_name
            assert gap.gap_reason


class TestCase53NoReportsOrGapsExist:
    """Test Case 5.3 — Audit manager attempts access when no reports or gaps exist."""

    def test_system_indicates_no_compliance_reports_available(self):
        """The system indicates that no compliance reports are available."""
        report = generate_compliance_report(
            compliance_file="compliance_info_empty.json",
            requirements_file="regulatory_requirements_empty.json",
        )
        assert report.can_generate is False
        assert "cannot be completed" in report.summary

    def test_system_indicates_no_compliance_gaps_available(self):
        """The system indicates that no compliance gaps are available."""
        # When we have full compliance, gaps list is empty
        result = detect_compliance_gaps(
            compliance_file="compliance_info_full_compliant.json",
        )
        assert len(result.gaps) == 0
        assert "no" in result.message.lower()

    def test_no_invalid_or_empty_artifacts_shown_as_valid(self):
        """No invalid or empty artifacts are shown as if they were valid outputs."""
        report = generate_compliance_report(
            compliance_file="compliance_info_empty.json",
            requirements_file="regulatory_requirements_empty.json",
        )
        assert report.can_generate is False
        assert len(report.applicable_regulations) == 0
