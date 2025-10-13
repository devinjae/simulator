"""
Sector model
"""

from sqlmodel import Field, SQLModel


class Sector(SQLModel, table=True):
    __tablename__ = "sectors"

    id: str = Field(primary_key=True)  # name of the sector
    description: str = Field(nullable=True)
