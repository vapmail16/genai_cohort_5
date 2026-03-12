"""Pydantic schemas for analytics operations."""
from pydantic import BaseModel, Field, ConfigDict


class AnalyticsSummaryResponse(BaseModel):
    """Schema for analytics summary response."""
    open_count: int = Field(..., description="Number of tickets with OPEN status")
    in_progress_count: int = Field(..., description="Number of tickets with IN_PROGRESS status")
    resolved_today_count: int = Field(..., description="Number of tickets resolved today")
    sla_breach_count: int = Field(..., description="Number of tickets with SLA breach")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "open_count": 15,
                "in_progress_count": 8,
                "resolved_today_count": 12,
                "sla_breach_count": 3
            }
        }
    )
