"""
API Routes - Example routes demonstrating authentication patterns

This module provides example routes showing different authentication patterns:
- Public routes (no authentication)
- Protected routes (authentication required)
- Optional authentication routes
- User type restricted routes
"""

from datetime import UTC, datetime
from typing import Any

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.auth.bridge_validator import SessionData
from app.lib.auth.middleware import optional_auth, require_auth, require_user_type
from app.lib.database.connection import get_db
from app.models.user import User

logger = structlog.get_logger()

router = APIRouter()


class UserResponse(BaseModel):
    """Response model for user data."""

    id: str
    email: str
    name: str | None = None
    last_name: str | None = None
    user_type: str


# ============================================================================
# PUBLIC ROUTES - No authentication required
# ============================================================================


@router.get("/public")
async def public_route() -> dict[str, Any]:
    """
    Public route - no authentication required.

    Returns:
        Public message
    """
    return {
        "message": "This is a public route",
        "timestamp": datetime.now(UTC).isoformat(),
        "authenticated": False,
    }


# ============================================================================
# PROTECTED ROUTES - Authentication required
# ============================================================================


@router.get("/profile")
async def get_profile(session: SessionData = Depends(require_auth)) -> dict[str, Any]:
    """
    Get user profile - authentication required.

    Args:
        session: Validated session data

    Returns:
        User profile data
    """
    return {
        "user_id": session.user_id,
        "email": session.email,
        "name": session.name,
        "user_type": session.user_type,
        "organization_id": session.organization_id,
        "permissions": session.permissions,
    }


@router.get("/protected")
async def protected_route(session: SessionData = Depends(require_auth)) -> dict[str, Any]:
    """
    Protected route - authentication required.

    Args:
        session: Validated session data

    Returns:
        Protected message with user info
    """
    logger.info("protected_route_accessed", user_id=session.user_id)

    return {
        "message": f"Hello {session.name}!",
        "user_id": session.user_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "authenticated": True,
    }


# ============================================================================
# OPTIONAL AUTHENTICATION ROUTES
# ============================================================================


@router.get("/content")
async def get_content(session: SessionData | None = Depends(optional_auth)) -> dict[str, Any]:
    """
    Content route with optional authentication.

    Args:
        session: Optional validated session data

    Returns:
        Content based on authentication status
    """
    if session:
        return {
            "message": f"Welcome back, {session.name}!",
            "premium_content": True,
            "user_id": session.user_id,
            "authenticated": True,
        }
    else:
        return {
            "message": "Welcome, guest!",
            "premium_content": False,
            "authenticated": False,
        }


# ============================================================================
# USER TYPE RESTRICTED ROUTES
# ============================================================================


@router.get("/admin/dashboard")
async def admin_dashboard(
    session: SessionData = Depends(require_user_type("admin", "superadmin"))
) -> dict[str, Any]:
    """
    Admin dashboard - requires admin or superadmin user type.

    Args:
        session: Validated session data with admin privileges

    Returns:
        Admin dashboard data
    """
    logger.info("admin_dashboard_accessed", user_id=session.user_id, user_type=session.user_type)

    return {
        "message": "Admin dashboard",
        "user_id": session.user_id,
        "user_type": session.user_type,
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/admin/users", response_model=list[UserResponse])
async def admin_list_users(
    db: AsyncSession = Depends(get_db),
    session: SessionData = Depends(require_user_type("admin", "superadmin")),
) -> list[UserResponse]:
    """
    List users for admin/superadmin.
    """
    result = await db.execute(select(User))
    users = result.scalars().all()

    return [
        UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            last_name=getattr(user, "last_name", None),
            user_type=user.user_type,
        )
        for user in users
    ]


# ============================================================================
# DATABASE EXAMPLE ROUTES
# ============================================================================


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    session: SessionData = Depends(require_user_type("admin", "superadmin")),
) -> list[UserResponse]:
    """
    List all users - authentication required.

    Args:
        db: Database session
        session: Validated session data

    Returns:
        List of users
    """
    result = await db.execute(select(User))
    users = result.scalars().all()

    return [
        UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            last_name=getattr(user, "last_name", None),
            user_type=user.user_type,
        )
        for user in users
    ]


# Removed create_user route per request


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    session: SessionData = Depends(require_user_type("admin", "superadmin")),
) -> UserResponse:
    """
    Get user by ID - authentication required.

    Args:
        user_id: User ID
        db: Database session
        session: Validated session data

    Returns:
        User data

    Raises:
        HTTPException: 404 if user not found
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        last_name=getattr(user, "last_name", None),
        user_type=user.user_type,
    )
