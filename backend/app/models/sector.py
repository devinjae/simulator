"""
Sector model
"""

from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid_utils import uuid7


class Sector(SQLModel, table=True):
    __tablename__ = "sectors"

    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(nullable=False, index=True)
