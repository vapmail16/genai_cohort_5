"""Audit log model for IT Support Portal."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from backend.database.connection import Base


class AuditLog(Base):
    """
    Audit log model for tracking system changes.

    Attributes:
        id: Primary key
        ticket_id: Foreign key to Ticket (nullable for non-ticket actions)
        user_id: Foreign key to User (who performed the action)
        action: Type of action performed (e.g., "CREATE", "UPDATE", "ASSIGN")
        details: JSON or text details of the change
        created_at: Timestamp when action was performed
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action='{self.action}', ticket_id={self.ticket_id})>"
