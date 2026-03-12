"""Tests for tickets router following TDD methodology."""
import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient
from backend.models.ticket import TicketStatus, TicketPriority
from backend.models.user import UserRole


@pytest.mark.asyncio
async def test_create_ticket_success(test_client: AsyncClient, sample_users: dict, sample_categories: dict):
    """Test creating a ticket successfully."""
    ticket_data = {
        "title": "Mouse not working",
        "description": "My wireless mouse is not connecting",
        "priority": "HIGH",
        "category_id": sample_categories["hardware"].id,
        "submitted_by": sample_users["end_user"].id
    }

    response = await test_client.post("/api/tickets", json=ticket_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == ticket_data["title"]
    assert data["description"] == ticket_data["description"]
    assert data["status"] == "OPEN"
    assert data["priority"] == "HIGH"
    assert data["category_id"] == ticket_data["category_id"]
    assert data["submitted_by"] == ticket_data["submitted_by"]
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_create_ticket_missing_title(test_client: AsyncClient, sample_users: dict, sample_categories: dict):
    """Test creating a ticket without title fails."""
    ticket_data = {
        "description": "My wireless mouse is not connecting",
        "priority": "HIGH",
        "category_id": sample_categories["hardware"].id,
        "submitted_by": sample_users["end_user"].id
    }

    response = await test_client.post("/api/tickets", json=ticket_data)

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_ticket_not_found(test_client: AsyncClient, sample_users: dict, sample_categories: dict):
    """Test getting a non-existent ticket returns 404."""
    response = await test_client.get("/api/tickets/99999")

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


@pytest.mark.asyncio
async def test_get_ticket_success(test_client: AsyncClient, sample_tickets: dict):
    """Test getting a ticket successfully."""
    ticket = sample_tickets["open_ticket"]
    response = await test_client.get(f"/api/tickets/{ticket.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ticket.id
    assert data["title"] == ticket.title
    assert data["submitter"]["username"] == "john_doe"


@pytest.mark.asyncio
async def test_update_status_valid(test_client: AsyncClient, sample_tickets: dict):
    """Test updating ticket status with valid transition."""
    ticket = sample_tickets["open_ticket"]
    update_data = {
        "status": "IN_PROGRESS"
    }

    response = await test_client.patch(f"/api/tickets/{ticket.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "IN_PROGRESS"


@pytest.mark.asyncio
async def test_update_status_invalid_transition(test_client: AsyncClient, sample_tickets: dict):
    """Test updating ticket status with invalid transition (RESOLVED to OPEN) fails."""
    ticket = sample_tickets["resolved_ticket"]
    update_data = {
        "status": "OPEN"
    }

    response = await test_client.patch(f"/api/tickets/{ticket.id}", json=update_data)

    assert response.status_code == 400
    data = response.json()
    assert "transition" in data["detail"].lower() or "invalid" in data["detail"].lower()


@pytest.mark.asyncio
async def test_update_status_resolved_without_note(test_client: AsyncClient, sample_tickets: dict):
    """Test resolving ticket without resolution note fails."""
    ticket = sample_tickets["in_progress_ticket"]
    update_data = {
        "status": "RESOLVED"
    }

    response = await test_client.patch(f"/api/tickets/{ticket.id}", json=update_data)

    assert response.status_code == 400
    data = response.json()
    assert "resolution_note" in data["detail"].lower()


@pytest.mark.asyncio
async def test_update_status_resolved_with_note(test_client: AsyncClient, sample_tickets: dict):
    """Test resolving ticket with resolution note succeeds."""
    ticket = sample_tickets["in_progress_ticket"]
    update_data = {
        "status": "RESOLVED",
        "resolution_note": "Issue fixed by resetting password"
    }

    response = await test_client.patch(f"/api/tickets/{ticket.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RESOLVED"
    assert data["resolution_note"] == update_data["resolution_note"]
    assert data["resolved_at"] is not None


@pytest.mark.asyncio
async def test_assign_to_agent_success(test_client: AsyncClient, sample_tickets: dict, sample_users: dict):
    """Test assigning ticket to agent successfully."""
    ticket = sample_tickets["open_ticket"]
    assign_data = {
        "assigned_to": sample_users["agent"].id
    }

    response = await test_client.patch(f"/api/tickets/{ticket.id}/assign", json=assign_data)

    assert response.status_code == 200
    data = response.json()
    assert data["assigned_to"] == sample_users["agent"].id
    assert data["agent"]["username"] == "agent_smith"


@pytest.mark.asyncio
async def test_assign_to_non_agent_fails(test_client: AsyncClient, sample_tickets: dict, sample_users: dict):
    """Test assigning ticket to non-agent user fails."""
    ticket = sample_tickets["open_ticket"]
    assign_data = {
        "assigned_to": sample_users["end_user"].id  # End user, not agent
    }

    response = await test_client.patch(f"/api/tickets/{ticket.id}/assign", json=assign_data)

    assert response.status_code == 400
    data = response.json()
    assert "agent" in data["detail"].lower() or "role" in data["detail"].lower()


@pytest.mark.asyncio
async def test_list_tickets_pagination(test_client: AsyncClient, sample_tickets: dict):
    """Test listing tickets with pagination."""
    response = await test_client.get("/api/tickets?page=1&page_size=2")

    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "tickets" in data
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["tickets"]) <= 2


@pytest.mark.asyncio
async def test_filter_by_status(test_client: AsyncClient, sample_tickets: dict):
    """Test filtering tickets by status."""
    response = await test_client.get("/api/tickets?status=OPEN")

    assert response.status_code == 200
    data = response.json()
    assert all(ticket["status"] == "OPEN" for ticket in data["tickets"])


@pytest.mark.asyncio
async def test_filter_by_category(test_client: AsyncClient, sample_tickets: dict, sample_categories: dict):
    """Test filtering tickets by category."""
    response = await test_client.get(f"/api/tickets?category={sample_categories['hardware'].id}")

    assert response.status_code == 200
    data = response.json()
    assert all(ticket["category_id"] == sample_categories["hardware"].id for ticket in data["tickets"])


@pytest.mark.asyncio
async def test_filter_by_priority(test_client: AsyncClient, sample_tickets: dict):
    """Test filtering tickets by priority."""
    response = await test_client.get("/api/tickets?priority=CRITICAL")

    assert response.status_code == 200
    data = response.json()
    assert all(ticket["priority"] == "CRITICAL" for ticket in data["tickets"])


@pytest.mark.asyncio
async def test_filter_by_assigned_to(test_client: AsyncClient, sample_tickets: dict, sample_users: dict):
    """Test filtering tickets by assigned agent."""
    response = await test_client.get(f"/api/tickets?assigned_to={sample_users['agent'].id}")

    assert response.status_code == 200
    data = response.json()
    assert all(
        ticket["assigned_to"] == sample_users["agent"].id
        for ticket in data["tickets"]
        if ticket["assigned_to"] is not None
    )


@pytest.mark.asyncio
async def test_filter_by_submitted_by(test_client: AsyncClient, sample_tickets: dict, sample_users: dict):
    """Test filtering tickets by submitter."""
    response = await test_client.get(f"/api/tickets?submitted_by={sample_users['end_user'].id}")

    assert response.status_code == 200
    data = response.json()
    assert all(ticket["submitted_by"] == sample_users["end_user"].id for ticket in data["tickets"])


@pytest.mark.asyncio
async def test_sla_breach_detected(test_client: AsyncClient, sample_tickets: dict):
    """Test that SLA breach is properly detected and marked."""
    ticket = sample_tickets["sla_breach_ticket"]
    response = await test_client.get(f"/api/tickets/{ticket.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["sla_breach"] == 1


@pytest.mark.asyncio
async def test_export_csv(test_client: AsyncClient, sample_tickets: dict):
    """Test exporting tickets to CSV."""
    response = await test_client.get("/api/tickets/export/csv")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "content-disposition" in response.headers

    # Check CSV content
    csv_content = response.text
    assert "ID" in csv_content or "id" in csv_content
    assert "Title" in csv_content or "title" in csv_content


@pytest.mark.asyncio
async def test_export_csv_with_filters(test_client: AsyncClient, sample_tickets: dict):
    """Test exporting filtered tickets to CSV."""
    response = await test_client.get("/api/tickets/export/csv?status=OPEN")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
