"""
Instrument Sector Exposure model (junction table)
"""

from sqlmodel import Field, ForeignKey, SQLModel


class InstrumentSectorExposure(SQLModel, table=True):
    __tablename__ = "instrument_sector_exposure"

    instrument_id: str = Field(foreign_key="instruments.id", primary_key=True)
    sector_id: int = Field(foreign_key="sectors.id", primary_key=True)
    weight: float = Field(nullable=False)
