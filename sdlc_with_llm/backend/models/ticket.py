"""Ticket model for IT Support Portal."""
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.connection import Base
import enum


class TicketStatus(str, enum.Enum):
    """Ticket status enumeration."""
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class TicketPriority(str, enum.Enum):
    """Ticket priority enumeration."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Ticket(Base):
    """
    Ticket model representing support tickets.

    Attributes:
        id: Primary key
        title: Short title of the issue
        description: Detailed description of the issue
        status: Current status (OPEN, IN_PROGRESS, RESOLVED)
        priority: Priority level (LOW, MEDIUM, HIGH, CRITICAL)
        category_id: Foreign key to Category
        submitted_by: Foreign key to User (who submitted the ticket)
        assigned_to: Foreign key to User (agent assigned to the ticket)
        created_at: Timestamp when ticket was created
        updated_at: Timestamp when ticket was last updated
        resolved_at: Timestamp when ticket was resolved
        resolution_note: Note added when ticket is resolved
        sla_breach: Boolean indicating if SLA was breached
    """
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.OPEN, index=True)
    priority = Column(Enum(TicketPriority), nullable=False, default=TicketPriority.MEDIUM, index=True)

    # Foreign keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    submitted_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Resolution
    resolution_note = Column(Text, nullable=True)
    sla_breach = Column(Integer, nullable=False, default=0)  # 0 = no breach, 1 = breach

    # Relationships
    category = relationship("Category", lazy="joined")
    submitter = relationship("User", foreign_keys=[submitted_by], lazy="joined")
    agent = relationship("User", foreign_keys=[assigned_to], lazy="joined")
    comments = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Ticket(id={self.id}, title='{self.title}', status='{self.status}')>"
