"""
Test Case 3.1 — Successful compliance report generation
Test Case 3.2 — Generate report with limited compliance information
Test Case 3.3 — Attempt report generation with no available data
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.report_generator import generate_compliance_report


class TestCase31SuccessfulReportGeneration:
    """Test Case 3.1 — Successful compliance report generation."""

    def test_system_generates_structured_report(self):
        """The system generates a structured compliance report."""
        report = generate_compliance_report()
        assert report.can_generate is True
        assert report.id
        assert report.generated_at
        assert report.applicable_regulations
        assert report.compliance_status

    def test_report_summarizes_applicable_regulations(self):
        """The report summarizes applicable regulations."""
        report = generate_compliance_report()
        assert len(report.applicable_regulations) > 0

    def test_report_includes_organization_compliance_status(self):
        """The report includes the organization's current compliance status."""
        report = generate_compliance_report()
        assert len(report.compliance_status) > 0
        assert report.summary


class TestCase32LimitedComplianceInfo:
    """Test Case 3.2 — Generate report with limited compliance information."""

    def test_system_generates_report_with_available_info(self):
        """The system generates a structured report using available information."""
        report = generate_compliance_report(
            compliance_file="compliance_info_partial.json",
        )
        assert report.can_generate is True
        assert report.id
        assert report.compliance_status

    def test_report_includes_available_compliance_status(self):
        """The report includes the current compliance status based on available data."""
        report = generate_compliance_report(
            compliance_file="compliance_info_partial.json",
        )
        assert report.compliance_status

    def test_missing_info_not_falsely_presented_as_complete(self):
        """Missing information is not falsely presented as complete."""
        report = generate_compliance_report(
            compliance_file="compliance_info_partial.json",
        )
        assert "missing" in report.compliance_status.values() or "partial" in report.compliance_status.values() or "Missing information" in report.summary


class TestCase33NoDataAvailable:
    """Test Case 3.3 — Attempt report generation with no available data."""

    def test_system_does_not_produce_misleading_report(self):
        """The system does not produce a misleading report with invented content."""
        report = generate_compliance_report(
            compliance_file="compliance_info_empty.json",
            requirements_file="regulatory_requirements_empty.json",
        )
        assert report.can_generate is False
        assert len(report.applicable_regulations) == 0
        assert len(report.compliance_status) == 0

    def test_system_indicates_report_generation_cannot_be_completed(self):
        """The system indicates that report generation cannot be completed due to unavailable input data."""
        report = generate_compliance_report(
            compliance_file="compliance_info_empty.json",
            requirements_file="regulatory_requirements_empty.json",
        )
        assert "cannot be completed" in report.summary

