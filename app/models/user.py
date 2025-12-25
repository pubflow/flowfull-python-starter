"""
User Model - Example SQLAlchemy model

This is an example model to demonstrate database usage.
Customize or remove based on your application needs.
"""

from typing import Any
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from app.lib.database.connection import Base


class User(Base):
    """User model - simplified to match actual database schema."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    user_type = Column(String(50), default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "user_type": self.user_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
