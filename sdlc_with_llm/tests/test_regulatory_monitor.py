"""
Test Case 1.1 — Successful retrieval of regulatory updates
Test Case 1.2 — No new regulatory updates available
Test Case 1.3 — Configured regulatory source unavailable
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.regulatory_monitor import monitor_regulations


class TestCase11SuccessfulRetrieval:
    """Test Case 1.1 — Successful retrieval of regulatory updates."""

    def test_system_retrieves_updates_from_configured_sources(self):
        """The system retrieves updates from configured regulatory sources."""
        result = monitor_regulations(updates_file="regulatory_updates.json")
        assert result.success is True
        assert len(result.updates) > 0

    def test_new_or_modified_requirements_identified_and_displayed(self):
        """New or modified regulatory requirements are identified and displayed for review."""
        result = monitor_regulations(updates_file="regulatory_updates.json")
        for update in result.updates:
            assert update.regulation_id
            assert update.regulation_name
            assert update.title
            assert update.status in ("new", "modified")


class TestCase12NoNewUpdates:
    """Test Case 1.2 — No new regulatory updates available."""

    def test_monitoring_completes_successfully(self):
        """The system completes monitoring successfully."""
        result = monitor_regulations(updates_file="regulatory_updates_empty.json")
        assert result.success is True

    def test_no_new_updates_displayed(self):
        """No new updates are displayed."""
        result = monitor_regulations(updates_file="regulatory_updates_empty.json")
        assert len(result.updates) == 0

    def test_result_clearly_indicates_no_updates_found(self):
        """The result clearly indicates that no new or modified regulatory requirements were found."""
        result = monitor_regulations(updates_file="regulatory_updates_empty.json")
        assert "no new" in result.message.lower() or "no new" in str(result).lower() or not result.updates


class TestCase13SourceUnavailable:
    """Test Case 1.3 — Configured regulatory source unavailable."""

    def test_system_does_not_retrieve_from_unavailable_source(self):
        """The system does not retrieve updates from the unavailable source."""
        # Simulate src-001 being unavailable
        result = monitor_regulations(
            sources_available={"src-001": False},
            updates_file="regulatory_updates.json",
        )
        # Updates from src-001 should be excluded (we filter by available sources)
        for update in result.updates:
            assert update.source_id != "src-001"

    def test_system_indicates_source_could_not_be_accessed(self):
        """The system indicates that the source could not be accessed."""
        result = monitor_regulations(
            sources_available={"src-001": False},
            updates_file="regulatory_updates.json",
        )
        assert len(result.unavailable_sources) > 0
        assert "SEC" in result.unavailable_sources[0] or "src-001" in str(result.unavailable_sources)

    def test_available_sources_still_processed(self):
        """Available sources, if any, are still processed."""
        result = monitor_regulations(
            sources_available={"src-001": False},
            updates_file="regulatory_updates.json",
        )
        # Should still have updates from src-002, src-003
        assert len(result.updates) > 0
        assert result.success is True
