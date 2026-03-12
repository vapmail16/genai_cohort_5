"""Pydantic schemas for ticket operations."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from backend.models.ticket import TicketStatus, TicketPriority


class UserBase(BaseModel):
    """Base user schema for nested representations."""
    id: int
    username: str
    full_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    """Base category schema for nested representations."""
    id: int
    name: str
    sla_hours: int

    model_config = ConfigDict(from_attributes=True)


class TicketCreate(BaseModel):
    """Schema for creating a new ticket."""
    title: str = Field(..., min_length=1, max_length=200, description="Short title of the issue")
    description: str = Field(..., min_length=1, description="Detailed description of the issue")
    priority: TicketPriority = Field(default=TicketPriority.MEDIUM, description="Priority level")
    category_id: int = Field(..., gt=0, description="Category ID")
    submitted_by: int = Field(..., gt=0, description="User ID of the submitter")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Cannot access shared drive",
                "description": "I'm getting a permission denied error when trying to access //server/shared",
                "priority": "HIGH",
                "category_id": 1,
                "submitted_by": 5
            }
        }
    )


class TicketUpdate(BaseModel):
    """Schema for updating ticket status and resolution."""
    status: Optional[TicketStatus] = Field(None, description="New status")
    resolution_note: Optional[str] = Field(None, description="Resolution note (required when resolving)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "RESOLVED",
                "resolution_note": "Reset password and verified access restored"
            }
        }
    )


class TicketAssign(BaseModel):
    """Schema for assigning a ticket to an agent."""
    assigned_to: int = Field(..., gt=0, description="User ID of the agent to assign")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "assigned_to": 3
            }
        }
    )


class TicketResponse(BaseModel):
    """Schema for ticket response with full details."""
    id: int
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    category_id: int
    category: CategoryBase
    submitted_by: int
    submitter: UserBase
    assigned_to: Optional[int] = None
    agent: Optional[UserBase] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_note: Optional[str] = None
    sla_breach: int

    model_config = ConfigDict(from_attributes=True)


class TicketListResponse(BaseModel):
    """Schema for paginated ticket list response."""
    total: int = Field(..., description="Total number of tickets matching filters")
    page: int = Field(..., description="Current page number (1-indexed)")
    page_size: int = Field(..., description="Number of items per page")
    tickets: List[TicketResponse] = Field(..., description="List of tickets")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 42,
                "page": 1,
                "page_size": 10,
                "tickets": []
            }
        }
    )
