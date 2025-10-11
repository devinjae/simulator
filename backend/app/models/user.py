"""
User model for authentication and user management
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(unique=True, index=True, nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": "now()"},
    )
    updated_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"onupdate": "now()"}
    )

    # Trading specific fields
    initial_cash: float = Field(default=100000.0)
    current_cash: float = Field(default=100000.0)
