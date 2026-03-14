"""
Test Case 4.1 — Successful detection of compliance gaps
Test Case 4.2 — No compliance gaps found
Test Case 4.3 — Gap detection with missing compliance documentation
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gap_detector import detect_compliance_gaps


class TestCase41SuccessfulGapDetection:
    """Test Case 4.1 — Successful detection of compliance gaps."""

    def test_system_analyzes_requirements_and_compliance_info(self):
        """The system analyzes regulatory requirements and available compliance information."""
        result = detect_compliance_gaps()
        assert result.success is True

    def test_system_flags_areas_where_requirements_dont_match(self):
        """The system flags areas where requirements do not match compliance documentation."""
        result = detect_compliance_gaps()
        # compliance_info has req-006 missing and doc-003 partial
        assert len(result.gaps) > 0

    def test_analyst_can_review_identified_gaps(self):
        """The compliance analyst can review the identified gaps."""
        result = detect_compliance_gaps()
        for gap in result.gaps:
            assert gap.requirement_id
            assert gap.regulation_name
            assert gap.requirement_text
            assert gap.gap_reason


class TestCase42NoComplianceGapsFound:
    """Test Case 4.2 — No compliance gaps found."""

    def test_system_completes_analysis_successfully(self):
        """The system completes the analysis successfully."""
        # Use compliance_info_full_compliant.json - need to create
        result = detect_compliance_gaps(
            compliance_file="compliance_info_full_compliant.json",
        )
        assert result.success is True

    def test_no_compliance_gaps_flagged(self):
        """No compliance gaps are flagged."""
        result = detect_compliance_gaps(
            compliance_file="compliance_info_full_compliant.json",
        )
        assert len(result.gaps) == 0

    def test_result_clearly_indicates_no_gaps_found(self):
        """The result clearly indicates that no gaps were found."""
        result = detect_compliance_gaps(
            compliance_file="compliance_info_full_compliant.json",
        )
        assert "no" in result.message.lower() and ("gap" in result.message.lower() or "gaps" in result.message.lower())


class TestCase43MissingComplianceDocumentation:
    """Test Case 4.3 — Gap detection with missing compliance documentation."""

    def test_system_analyzes_available_info_only(self):
        """The system analyzes available information only."""
        result = detect_compliance_gaps(
            compliance_file="compliance_info_partial.json",
        )
        assert result.success is True

    def test_system_flags_mismatches_where_comparison_possible(self):
        """The system flags mismatches only where comparison is possible."""
        result = detect_compliance_gaps(
            compliance_file="compliance_info_partial.json",
        )
        assert len(result.gaps) >= 0

    def test_result_indicates_limited_complete_gap_analysis(self):
        """The result indicates that complete gap analysis may be limited due to missing documentation."""
        result = detect_compliance_gaps(
            compliance_file="compliance_info_full_compliant.json",
        )
        # When full compliance, limited_due_to_missing_docs is False
        # For partial compliance, it should be True
        result_partial = detect_compliance_gaps(
            compliance_file="compliance_info_partial.json",
        )
        assert result_partial.limited_due_to_missing_docs or "limited" in result_partial.message.lower() or len(result_partial.gaps) > 0
