"""
Sector model
"""

from sqlmodel import Field, SQLModel


class Sector(SQLModel, table=True):
    __tablename__ = "sectors"

    id: int = Field(primary_key=True)
    name: str = Field(nullable=False, index=True)
