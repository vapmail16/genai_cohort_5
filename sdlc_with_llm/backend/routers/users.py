"""Users router with authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, ConfigDict

from backend.database.connection import get_db
from backend.models.user import User, UserRole

router = APIRouter(prefix="/api/users", tags=["users"])


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


@router.get("/authenticate", response_model=UserResponse)
async def authenticate_user(
    username: str = Query(..., description="Username to authenticate"),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Authenticate a user by username.

    This endpoint is used by middleware to verify user credentials
    and retrieve user information for authorization.

    Args:
        username: Username to look up
        db: Database session

    Returns:
        UserResponse: User details if found

    Raises:
        HTTPException 404: If user not found
    """
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{username}' not found"
        )

    return UserResponse.model_validate(user)
