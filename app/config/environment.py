"""
Environment Configuration - Pydantic Settings

This module provides type-safe configuration management with automatic validation.
All environment variables are loaded from .env file and validated using Pydantic.
"""

from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration with Pydantic validation.

    Features:
    - Type-safe configuration
    - Automatic validation
    - Environment variable loading
    - Default values
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # Server Configuration
    PORT: int = Field(default=3001, ge=1, le=65535)
    HOST: str = Field(default="0.0.0.0")
    ENVIRONMENT: Literal["development", "production", "test"] = Field(default="development")
    BASE_URL: str = Field(default="http://localhost:3001")

    # Database Configuration
    DATABASE_URL: str = Field(..., min_length=1)
    DATABASE_POOL_SIZE: int = Field(default=10, ge=1)
    DATABASE_MAX_OVERFLOW: int = Field(default=20, ge=0)
    DATABASE_POOL_TIMEOUT: int = Field(default=30, ge=1)
    DATABASE_POOL_RECYCLE: int = Field(default=3600, ge=0)

    # Flowless Integration
    FLOWLESS_API_URL: str = Field(..., min_length=1)
    BRIDGE_VALIDATION_SECRET: str = Field(..., min_length=32)
    BRIDGE_VALIDATION_TIMEOUT: int = Field(default=5000, ge=1000)
    BRIDGE_RETRY_ATTEMPTS: int = Field(default=3, ge=1, le=10)

    # Session Management
    SESSION_VALIDATION_CACHE_TTL: int = Field(default=300, ge=60)
    SESSION_HEADER_NAME: str = Field(default="X-Session-Id")
    SESSION_COOKIE_NAME: str = Field(default="session_id")

    # Authentication & Validation
    AUTH_VALIDATION_MODE: Literal["DISABLED", "STANDARD", "ADVANCED", "STRICT"] = Field(
        default="STANDARD"
    )
    AUTH_ENABLE_VALIDATION_MODE: bool = Field(default=True)
    AUTH_IP_VALIDATION: bool = Field(default=True)
    AUTH_USER_AGENT_VALIDATION: bool = Field(default=True)
    AUTH_DEVICE_VALIDATION: bool = Field(default=False)
    AUTH_AUTO_INVALIDATE: bool = Field(default=False)
    AUTH_LOG_VIOLATIONS: bool = Field(default=True)

    # Cache Configuration
    CACHE_ENABLED: bool = Field(default=True)
    REDIS_URL: str | None = Field(default=None)

    # Trust Tokens (PASETO)
    PASETO_PRIVATE_KEY: str | None = Field(default=None)
    TOKEN_TTL_HOURS: int = Field(default=168, ge=1)
    TOKEN_EMAIL_VERIFICATION_TTL_HOURS: int = Field(default=24, ge=1)
    TOKEN_PASSWORD_RESET_TTL_HOURS: int = Field(default=1, ge=1)
    TOKEN_INVITATION_TTL_HOURS: int = Field(default=168, ge=1)

    # Security & CORS
    CORS_ORIGINS: str = Field(default="http://localhost:3000")
    CORS_METHODS: str = Field(default="GET,POST,PUT,DELETE,OPTIONS")
    CORS_HEADERS: str = Field(default="Content-Type,Authorization,X-Session-Id")
    CORS_CREDENTIALS: bool = Field(default=True)
    CORS_MAX_AGE: int = Field(default=86400, ge=0)

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_REQUESTS: int = Field(default=100, ge=1)
    RATE_LIMIT_WINDOW: int = Field(default=60, ge=1)

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO")
    LOG_FORMAT: Literal["json", "text"] = Field(default="json")
    LOG_MODE: bool = Field(default=False)

    # Development
    DEV_MODE: bool = Field(default=False)
    DEV_CORS_RELAXED: bool = Field(default=False)
    DEV_LOG_REQUESTS: bool = Field(default=False)
    RELOAD: bool = Field(default=False)

    # Computed Properties
    @property
    def cors_origins_list(self) -> list[str]:
        """Convert CORS_ORIGINS string to list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def cors_methods_list(self) -> list[str]:
        """Convert CORS_METHODS string to list."""
        return [method.strip() for method in self.CORS_METHODS.split(",")]

    @property
    def cors_headers_list(self) -> list[str]:
        """Convert CORS_HEADERS string to list."""
        return [header.strip() for header in self.CORS_HEADERS.split(",")]

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production"

    @property
    def is_test(self) -> bool:
        """Check if running in test mode."""
        return self.ENVIRONMENT == "test"

    @field_validator("BRIDGE_VALIDATION_SECRET")
    @classmethod
    def validate_bridge_secret(cls, v: str) -> str:
        """Validate that bridge secret has at least 32 characters."""
        if len(v) < 32:
            raise ValueError("BRIDGE_VALIDATION_SECRET must be at least 32 characters")
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate DATABASE_URL format."""
        allowed_prefixes = [
            "postgresql://",
            "postgres://",
            "mysql://",
            "sqlite://",
            "libsql://",
            "cockroachdb://",
            "cockroachdb+asyncpg://",
        ]
        if not any(v.startswith(prefix) for prefix in allowed_prefixes):
            raise ValueError(
                "DATABASE_URL must start with postgresql://, postgres://, mysql://, sqlite://, libsql://, or cockroachdb://"
            )
        return v


# Singleton instance
settings = Settings()


# Helper functions
def get_database_type() -> Literal["postgresql", "mysql", "sqlite", "cockroachdb"]:
    """Detect database type from URL."""
    url = settings.DATABASE_URL.lower()

    if url.startswith("cockroachdb://") or url.startswith("cockroachdb+"):
        return "cockroachdb"
    if url.startswith("postgresql://") or url.startswith("postgres://"):
        return "postgresql"
    if url.startswith("mysql://"):
        return "mysql"
    if url.startswith("sqlite://") or url.startswith("libsql://"):
        return "sqlite"

    raise ValueError(f"Unsupported database type in URL: {settings.DATABASE_URL}")


def validate_config() -> None:
    """Validate complete configuration."""
    errors = []

    # Validate DATABASE_URL
    if not settings.DATABASE_URL:
        errors.append("DATABASE_URL is required")

    # Validate FLOWLESS_API_URL
    if not settings.FLOWLESS_API_URL:
        errors.append("FLOWLESS_API_URL is required")

    # Validate BRIDGE_VALIDATION_SECRET
    if len(settings.BRIDGE_VALIDATION_SECRET) < 32:
        errors.append("BRIDGE_VALIDATION_SECRET must be at least 32 characters")

    # Validate PASETO_PRIVATE_KEY in production
    if settings.is_production and not settings.PASETO_PRIVATE_KEY:
        errors.append("PASETO_PRIVATE_KEY is required in production")

    if errors:
        raise ValueError(
            "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
        )

    print("✅ Configuration validated successfully")
