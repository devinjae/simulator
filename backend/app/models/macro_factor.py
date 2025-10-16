"""
Macro Factor model
"""

from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid_utils import uuid7


class MacroFactor(SQLModel, table=True):
    __tablename__ = "macro_factors"

    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(nullable=False, index=True)
    alpha: float = Field(nullable=False)
    cap_up: float = Field(nullable=False)
    cap_down: float = Field(nullable=False)
