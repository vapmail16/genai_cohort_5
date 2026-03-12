"""Tickets router with endpoints for ticket management."""
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, List
from datetime import datetime, timedelta
import csv
import io

from backend.database.connection import get_db
from backend.models.ticket import Ticket, TicketStatus, TicketPriority
from backend.models.user import User, UserRole
from backend.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketAssign,
    TicketResponse,
    TicketListResponse
)
from backend.services.sla import check_sla_breach

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


@router.post("", response_model=TicketResponse, status_code=201)
async def create_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db)
) -> TicketResponse:
    """
    Create a new support ticket.

    Args:
        ticket_data: Ticket creation data
        db: Database session

    Returns:
        TicketResponse: Created ticket with full details

    Raises:
        HTTPException 404: If category or user not found
        HTTPException 422: If validation fails
    """
    # Verify category exists
    category_result = await db.execute(
        select(User.__table__.c.id).where(User.id == ticket_data.category_id)
    )
    if not category_result.first():
        # Check if it's actually a valid category by checking categories table
        from backend.models.category import Category
        cat_result = await db.execute(
            select(Category).where(Category.id == ticket_data.category_id)
        )
        if not cat_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Category not found")

    # Verify submitter exists
    user_result = await db.execute(
        select(User).where(User.id == ticket_data.submitted_by)
    )
    if not user_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")

    # Create ticket
    new_ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        priority=ticket_data.priority,
        category_id=ticket_data.category_id,
        submitted_by=ticket_data.submitted_by,
        status=TicketStatus.OPEN,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        sla_breach=0
    )

    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)

    return TicketResponse.model_validate(new_ticket)


@router.get("", response_model=TicketListResponse)
async def list_tickets(
    status: Optional[TicketStatus] = Query(None, description="Filter by status"),
    category: Optional[int] = Query(None, description="Filter by category ID"),
    assigned_to: Optional[int] = Query(None, description="Filter by assigned agent ID"),
    submitted_by: Optional[int] = Query(None, description="Filter by submitter ID"),
    priority: Optional[TicketPriority] = Query(None, description="Filter by priority"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db)
) -> TicketListResponse:
    """
    List tickets with optional filtering and pagination.

    Args:
        status: Filter by ticket status
        category: Filter by category ID
        assigned_to: Filter by assigned agent ID
        submitted_by: Filter by submitter ID
        priority: Filter by priority level
        page: Page number (1-indexed)
        page_size: Number of items per page
        db: Database session

    Returns:
        TicketListResponse: Paginated list of tickets
    """
    # Build query with filters
    query = select(Ticket)

    if status:
        query = query.where(Ticket.status == status)
    if category:
        query = query.where(Ticket.category_id == category)
    if assigned_to:
        query = query.where(Ticket.assigned_to == assigned_to)
    if submitted_by:
        query = query.where(Ticket.submitted_by == submitted_by)
    if priority:
        query = query.where(Ticket.priority == priority)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    query = query.order_by(Ticket.created_at.desc())

    # Execute query
    result = await db.execute(query)
    tickets = result.scalars().all()

    return TicketListResponse(
        total=total,
        page=page,
        page_size=page_size,
        tickets=[TicketResponse.model_validate(ticket) for ticket in tickets]
    )


@router.get("/export/csv")
async def export_tickets_csv(
    status: Optional[TicketStatus] = Query(None, description="Filter by status"),
    category: Optional[int] = Query(None, description="Filter by category ID"),
    assigned_to: Optional[int] = Query(None, description="Filter by assigned agent ID"),
    submitted_by: Optional[int] = Query(None, description="Filter by submitter ID"),
    priority: Optional[TicketPriority] = Query(None, description="Filter by priority"),
    db: AsyncSession = Depends(get_db)
) -> Response:
    """
    Export tickets to CSV format with optional filtering.

    Args:
        status: Filter by ticket status
        category: Filter by category ID
        assigned_to: Filter by assigned agent ID
        submitted_by: Filter by submitter ID
        priority: Filter by priority level
        db: Database session

    Returns:
        Response: CSV file download
    """
    # Build query with same filters as list
    query = select(Ticket)

    if status:
        query = query.where(Ticket.status == status)
    if category:
        query = query.where(Ticket.category_id == category)
    if assigned_to:
        query = query.where(Ticket.assigned_to == assigned_to)
    if submitted_by:
        query = query.where(Ticket.submitted_by == submitted_by)
    if priority:
        query = query.where(Ticket.priority == priority)

    query = query.order_by(Ticket.created_at.desc())

    # Execute query
    result = await db.execute(query)
    tickets = result.scalars().all()

    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        "ID", "Title", "Description", "Status", "Priority",
        "Category", "Submitted By", "Assigned To",
        "Created At", "Updated At", "Resolved At",
        "Resolution Note", "SLA Breach"
    ])

    # Write data
    for ticket in tickets:
        writer.writerow([
            ticket.id,
            ticket.title,
            ticket.description,
            ticket.status.value,
            ticket.priority.value,
            ticket.category.name if ticket.category else "",
            ticket.submitter.username if ticket.submitter else "",
            ticket.agent.username if ticket.agent else "",
            ticket.created_at.isoformat() if ticket.created_at else "",
            ticket.updated_at.isoformat() if ticket.updated_at else "",
            ticket.resolved_at.isoformat() if ticket.resolved_at else "",
            ticket.resolution_note or "",
            ticket.sla_breach
        ])

    # Return CSV response
    csv_content = output.getvalue()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=tickets_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db)
) -> TicketResponse:
    """
    Get a single ticket by ID.

    Args:
        ticket_id: Ticket ID
        db: Database session

    Returns:
        TicketResponse: Ticket details

    Raises:
        HTTPException 404: If ticket not found
    """
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    return TicketResponse.model_validate(ticket)


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    update_data: TicketUpdate,
    db: AsyncSession = Depends(get_db)
) -> TicketResponse:
    """
    Update ticket status and resolution note.

    Args:
        ticket_id: Ticket ID
        update_data: Update data
        db: Database session

    Returns:
        TicketResponse: Updated ticket

    Raises:
        HTTPException 404: If ticket not found
        HTTPException 400: If invalid status transition or missing resolution note
    """
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    # Validate status transition
    if update_data.status:
        # Cannot transition from RESOLVED to other states
        if ticket.status == TicketStatus.RESOLVED and update_data.status != TicketStatus.RESOLVED:
            raise HTTPException(
                status_code=400,
                detail="Invalid transition: Cannot reopen a resolved ticket"
            )

        # Require resolution note when resolving
        if update_data.status == TicketStatus.RESOLVED:
            if not update_data.resolution_note:
                raise HTTPException(
                    status_code=400,
                    detail="resolution_note is required when resolving a ticket"
                )
            ticket.resolved_at = datetime.utcnow()
            ticket.resolution_note = update_data.resolution_note

            # Check for SLA breach
            if check_sla_breach(ticket):
                ticket.sla_breach = 1

        ticket.status = update_data.status
        ticket.updated_at = datetime.utcnow()

    # Update resolution note even if not resolving (e.g., updating existing note)
    if update_data.resolution_note and update_data.status != TicketStatus.RESOLVED:
        ticket.resolution_note = update_data.resolution_note
        ticket.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(ticket)

    return TicketResponse.model_validate(ticket)


@router.patch("/{ticket_id}/assign", response_model=TicketResponse)
async def assign_ticket(
    ticket_id: int,
    assign_data: TicketAssign,
    db: AsyncSession = Depends(get_db)
) -> TicketResponse:
    """
    Assign a ticket to an agent.

    Args:
        ticket_id: Ticket ID
        assign_data: Assignment data
        db: Database session

    Returns:
        TicketResponse: Updated ticket

    Raises:
        HTTPException 404: If ticket or user not found
        HTTPException 400: If user is not an agent
    """
    # Get ticket
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    # Get user and verify they are an agent
    user_result = await db.execute(
        select(User).where(User.id == assign_data.assigned_to)
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role not in [UserRole.SUPPORT_AGENT, UserRole.ADMIN]:
        raise HTTPException(
            status_code=400,
            detail="User must have SUPPORT_AGENT or ADMIN role to be assigned tickets"
        )

    # Assign ticket
    ticket.assigned_to = assign_data.assigned_to
    ticket.updated_at = datetime.utcnow()

    # Auto-transition to IN_PROGRESS if currently OPEN
    if ticket.status == TicketStatus.OPEN:
        ticket.status = TicketStatus.IN_PROGRESS

    await db.commit()
    await db.refresh(ticket)

    return TicketResponse.model_validate(ticket)


# TODO: POST /api/tickets/{id}/comments endpoint
# This endpoint is reserved for live demo and will be implemented during the demonstration.
# Expected functionality:
# - Accept comment_text and user_id in request body
# - Create a new Comment associated with the ticket
# - Return the created comment with user details
# - Validate that ticket exists
# - Update ticket's updated_at timestamp
