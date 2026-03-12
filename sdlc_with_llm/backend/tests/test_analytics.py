"""Tests for analytics router following TDD methodology."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_summary_counts(test_client: AsyncClient, sample_tickets: dict):
    """Test analytics summary returns correct counts."""
    response = await test_client.get("/api/analytics/summary")

    assert response.status_code == 200
    data = response.json()

    # Check all required fields are present
    assert "open_count" in data
    assert "in_progress_count" in data
    assert "resolved_today_count" in data
    assert "sla_breach_count" in data

    # Verify counts based on sample data
    # We have 2 OPEN tickets (open_ticket and sla_breach_ticket)
    assert data["open_count"] == 2

    # We have 1 IN_PROGRESS ticket (in_progress_ticket)
    assert data["in_progress_count"] == 1

    # We have 1 SLA breach ticket (sla_breach_ticket)
    assert data["sla_breach_count"] == 1


@pytest.mark.asyncio
async def test_sla_breach_count(test_client: AsyncClient, sample_tickets: dict):
    """Test that SLA breach count is accurate."""
    response = await test_client.get("/api/analytics/summary")

    assert response.status_code == 200
    data = response.json()

    # Should have at least 1 SLA breach from sample data
    assert data["sla_breach_count"] >= 1


@pytest.mark.asyncio
async def test_summary_returns_integers(test_client: AsyncClient, sample_tickets: dict):
    """Test that all counts are integers."""
    response = await test_client.get("/api/analytics/summary")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data["open_count"], int)
    assert isinstance(data["in_progress_count"], int)
    assert isinstance(data["resolved_today_count"], int)
    assert isinstance(data["sla_breach_count"], int)


@pytest.mark.asyncio
async def test_summary_counts_non_negative(test_client: AsyncClient, sample_tickets: dict):
    """Test that all counts are non-negative."""
    response = await test_client.get("/api/analytics/summary")

    assert response.status_code == 200
    data = response.json()

    assert data["open_count"] >= 0
    assert data["in_progress_count"] >= 0
    assert data["resolved_today_count"] >= 0
    assert data["sla_breach_count"] >= 0
