"""
Instrument model
"""

from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid_utils import uuid7


class Instrument(SQLModel, table=True):
    __tablename__ = "instruments"

    id: UUID = Field(default_factory=uuid7, primary_key=True)
    symbol: str = Field(nullable=False, index=True)
    s_0: float = Field(nullable=False)
    mean: float = Field(nullable=False)
    variance: float = Field(nullable=False)
