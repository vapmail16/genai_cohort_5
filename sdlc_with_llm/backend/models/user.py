"""User model for IT Support Portal."""
from sqlalchemy import Column, Integer, String, Enum
from backend.database.connection import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration."""
    END_USER = "END_USER"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    ADMIN = "ADMIN"


class User(Base):
    """
    User model representing system users.

    Attributes:
        id: Primary key
        username: Unique username
        email: User email address
        full_name: Full name of the user
        role: User role (END_USER, SUPPORT_AGENT, ADMIN)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.END_USER)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
