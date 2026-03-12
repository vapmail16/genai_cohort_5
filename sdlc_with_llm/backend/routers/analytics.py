"""Analytics router with endpoints for dashboard metrics."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta

from backend.database.connection import get_db
from backend.models.ticket import Ticket, TicketStatus
from backend.schemas.analytics import AnalyticsSummaryResponse

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    db: AsyncSession = Depends(get_db)
) -> AnalyticsSummaryResponse:
    """
    Get analytics summary for dashboard.

    Returns counts for:
    - Open tickets
    - In-progress tickets
    - Tickets resolved today
    - Tickets with SLA breach

    Args:
        db: Database session

    Returns:
        AnalyticsSummaryResponse: Summary metrics
    """
    # Count OPEN tickets
    open_result = await db.execute(
        select(func.count()).select_from(Ticket).where(Ticket.status == TicketStatus.OPEN)
    )
    open_count = open_result.scalar() or 0

    # Count IN_PROGRESS tickets
    in_progress_result = await db.execute(
        select(func.count()).select_from(Ticket).where(Ticket.status == TicketStatus.IN_PROGRESS)
    )
    in_progress_count = in_progress_result.scalar() or 0

    # Count tickets resolved today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    resolved_today_result = await db.execute(
        select(func.count()).select_from(Ticket).where(
            and_(
                Ticket.status == TicketStatus.RESOLVED,
                Ticket.resolved_at >= today_start,
                Ticket.resolved_at < today_end
            )
        )
    )
    resolved_today_count = resolved_today_result.scalar() or 0

    # Count tickets with SLA breach
    sla_breach_result = await db.execute(
        select(func.count()).select_from(Ticket).where(Ticket.sla_breach == 1)
    )
    sla_breach_count = sla_breach_result.scalar() or 0

    return AnalyticsSummaryResponse(
        open_count=open_count,
        in_progress_count=in_progress_count,
        resolved_today_count=resolved_today_count,
        sla_breach_count=sla_breach_count
    )
