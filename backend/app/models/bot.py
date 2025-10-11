"""
Bot model
"""

from typing import Any, Dict
from uuid import UUID

from sqlmodel import JSON, Column, Field, SQLModel
from uuid_utils import uuid7


class Bot(SQLModel, table=True):
    __tablename__ = "bots"

    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(nullable=False, index=True)
    params: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
