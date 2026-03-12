"""SLA (Service Level Agreement) checking service."""
from datetime import datetime, timedelta
from typing import Literal
from backend.models.ticket import Ticket, TicketStatus


def check_sla_breach(ticket: Ticket) -> bool:
    """
    Check if a ticket has breached its SLA.

    Args:
        ticket: Ticket instance with category relationship loaded

    Returns:
        bool: True if SLA is breached, False otherwise

    Logic:
        - If ticket is RESOLVED, check if resolution time exceeded SLA
        - If ticket is OPEN or IN_PROGRESS, check if current time exceeds SLA
        - SLA is based on category.sla_hours from ticket creation time
    """
    if not ticket.category:
        # If category is not loaded, cannot determine SLA
        return False

    sla_deadline = ticket.created_at + timedelta(hours=ticket.category.sla_hours)

    if ticket.status == TicketStatus.RESOLVED:
        # Check if resolution time exceeded SLA
        if ticket.resolved_at:
            return ticket.resolved_at > sla_deadline
        return False
    else:
        # Check if current time exceeds SLA
        return datetime.utcnow() > sla_deadline


def get_sla_status(ticket: Ticket) -> Literal["ON_TRACK", "AT_RISK", "BREACHED"]:
    """
    Get the SLA status of a ticket.

    Args:
        ticket: Ticket instance with category relationship loaded

    Returns:
        str: One of "ON_TRACK", "AT_RISK", or "BREACHED"

    Logic:
        - BREACHED: SLA deadline has passed
        - AT_RISK: Within 2 hours of SLA deadline
        - ON_TRACK: More than 2 hours before SLA deadline
    """
    if not ticket.category:
        return "ON_TRACK"

    sla_deadline = ticket.created_at + timedelta(hours=ticket.category.sla_hours)
    current_time = datetime.utcnow() if ticket.status != TicketStatus.RESOLVED else ticket.resolved_at

    if not current_time:
        current_time = datetime.utcnow()

    time_remaining = sla_deadline - current_time

    if time_remaining.total_seconds() < 0:
        return "BREACHED"
    elif time_remaining.total_seconds() < 7200:  # Less than 2 hours
        return "AT_RISK"
    else:
        return "ON_TRACK"
