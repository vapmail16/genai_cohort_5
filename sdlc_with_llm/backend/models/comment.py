"""Comment model for IT Support Portal."""
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.connection import Base


class Comment(Base):
    """
    Comment model representing ticket comments.

    Attributes:
        id: Primary key
        ticket_id: Foreign key to Ticket
        user_id: Foreign key to User (who made the comment)
        comment_text: The comment content
        created_at: Timestamp when comment was created
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    ticket = relationship("Ticket", back_populates="comments")
    user = relationship("User", lazy="joined")

    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, ticket_id={self.ticket_id}, user_id={self.user_id})>"
