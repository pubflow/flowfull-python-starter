"""
Health Check Routes

Provides endpoints for monitoring application health and status.
"""

from datetime import UTC, datetime
from typing import Any

import structlog
from fastapi import APIRouter, status

from app.config.environment import settings
from app.lib.cache.cache_instances import session_cache
from app.lib.database.connection import check_db_health

logger = structlog.get_logger()

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, Any]:
    """
    Basic health check endpoint.

    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0",
    }


@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check() -> dict[str, Any]:
    """
    Detailed health check with component status.

    Returns:
        Detailed health status including database and cache
    """
    # Check database
    db_healthy = await check_db_health()

    # Check cache stats
    cache_stats = session_cache.get_stats()

    return {
        "status": "healthy" if db_healthy else "degraded",
        "timestamp": datetime.now(UTC).isoformat(),
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0",
        "components": {
            "database": {
                "status": "healthy" if db_healthy else "unhealthy",
                "type": settings.DATABASE_URL.split("://")[0],
            },
            "cache": {
                "status": "healthy" if cache_stats["redis_available"] else "degraded",
                "redis_available": cache_stats["redis_available"],
                "lru_size": cache_stats["lru_size"],
            },
        },
    }


@router.get("/health/cache", status_code=status.HTTP_200_OK)
async def cache_health() -> dict[str, Any]:
    """
    Cache health and statistics.

    Returns:
        Cache statistics and health status
    """
    stats = session_cache.get_stats()

    return {
        "status": "healthy" if stats["redis_available"] else "degraded",
        "timestamp": datetime.now(UTC).isoformat(),
        "cache_stats": stats,
    }


@router.get("/health/database", status_code=status.HTTP_200_OK)
async def database_health() -> dict[str, Any]:
    """
    Database health check.

    Returns:
        Database health status
    """
    db_healthy = await check_db_health()

    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "database_type": settings.DATABASE_URL.split("://")[0],
        "pool_size": settings.DATABASE_POOL_SIZE,
        "max_overflow": settings.DATABASE_MAX_OVERFLOW,
    }
