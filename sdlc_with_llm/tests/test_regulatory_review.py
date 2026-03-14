"""
Test Case 2.1 — View structured regulatory update details
Test Case 2.2 — Review multiple regulatory updates
Test Case 2.3 — Attempt to review updates when none exist
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.regulatory_monitor import monitor_regulations


def get_updates_for_review(updates_file: str = "regulatory_updates.json"):
    """Get identified regulatory updates for review (simulates opening the list)."""
    result = monitor_regulations(updates_file=updates_file)
    return result.updates


class TestCase21ViewStructuredDetails:
    """Test Case 2.1 — View structured regulatory update details."""

    def test_selected_update_shown_in_structured_format(self):
        """The selected update is shown in a structured format."""
        updates = get_updates_for_review()
        assert len(updates) >= 1
        update = updates[0]
        # Structured format: has required fields
        assert hasattr(update, "regulation_id")
        assert hasattr(update, "regulation_name")
        assert hasattr(update, "title")
        assert hasattr(update, "summary")
        assert hasattr(update, "effective_date")
        assert hasattr(update, "status")

    def test_details_clearly_indicate_relevant_regulation(self):
        """The details clearly indicate the relevant regulation being updated."""
        updates = get_updates_for_review()
        update = updates[0]
        assert update.regulation_id
        assert update.regulation_name


class TestCase22ReviewMultipleUpdates:
    """Test Case 2.2 — Review multiple regulatory updates."""

    def test_each_update_can_be_viewed_separately(self):
        """Each regulatory update can be viewed separately."""
        updates = get_updates_for_review()
        assert len(updates) >= 2
        for update in updates:
            assert update.id
            assert update.regulation_name

    def test_each_update_shows_relevant_regulation_clearly(self):
        """Each update shows its relevant regulation clearly."""
        updates = get_updates_for_review()
        for update in updates:
            assert update.regulation_id
            assert update.regulation_name


class TestCase23NoUpdatesWhenNoneExist:
    """Test Case 2.3 — Attempt to review updates when none exist."""

    def test_system_shows_no_updates_available(self):
        """The system shows that no regulatory updates are available for review."""
        updates = get_updates_for_review(updates_file="regulatory_updates_empty.json")
        assert len(updates) == 0

    def test_no_incomplete_or_blank_update_details_displayed(self):
        """No incomplete or blank update details are displayed."""
        updates = get_updates_for_review(updates_file="regulatory_updates_empty.json")
        assert updates == []
