"""
FastAPI Application Entry Point

This is the main application file that configures and starts the FastAPI server.
"""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.environment import settings
from app.lib.database.connection import close_db, init_db
from app.lib.utils.logger import configure_logging
from app.routes import api, health

# Configure logging
configure_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler for startup and shutdown.
    
    Replaces deprecated @app.on_event("startup") and @app.on_event("shutdown").
    """
    # Startup
    logger.info(
        "server_starting",
        host=settings.HOST,
        port=settings.PORT,
        environment=settings.ENVIRONMENT,
        flowless_url=settings.FLOWLESS_API_URL,
        database_type=settings.DATABASE_URL.split("://")[0],
    )

    # Initialize database
    try:
        await init_db()
        logger.info("database_ready")
    except Exception as e:
        logger.error("database_initialization_failed", error=str(e))

    yield

    # Shutdown
    logger.info("server_shutting_down")

    # Close database connections
    try:
        await close_db()
    except Exception as e:
        logger.error("database_close_failed", error=str(e))


# Create FastAPI app with lifespan
app = FastAPI(
    title="Flowfull Python Starter",
    description="Production-ready Python backend with Flowless integration",
    version="0.1.0",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.cors_methods_list,
    allow_headers=settings.cors_headers_list,
    max_age=settings.CORS_MAX_AGE,
)


@app.get("/")
async def root() -> dict[str, Any]:
    """Root endpoint."""
    return {
        "name": "Flowfull Python Starter",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.is_development else None,
    }


# Import and include routers
app.include_router(health.router, tags=["Health"])
app.include_router(api.router, prefix="/api/v1", tags=["API"])
