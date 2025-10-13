"""
Instrument model
"""

from typing import Optional

from sqlmodel import Field, SQLModel


class Instrument(SQLModel, table=True):
    __tablename__ = "instruments"

    id: str = Field(primary_key=True)
    full_name: str = Field(nullable=False, index=True)
    s_0: float = Field(nullable=False)
    mean: float = Field(nullable=False)
    variance: float = Field(nullable=False)
