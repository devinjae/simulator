"""
Bot model
"""

from typing import Any, Dict

from sqlmodel import JSON, Column, Field, SQLModel


class Bot(SQLModel, table=True):
    __tablename__ = "bots"

    id: int = Field(primary_key=True, ge=0)
    name: str = Field(nullable=False, index=True)
    params: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
