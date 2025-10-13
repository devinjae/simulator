"""
Bot Position model
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, ForeignKey, SQLModel


class BotPosition(SQLModel, table=True):
    __tablename__ = "bot_positions"

    bot_id: int = Field(foreign_key="bots.id", primary_key=True)
    instrument_id: str = Field(foreign_key="instruments.id", primary_key=True)
    qty: int = Field(nullable=False)
    cash: float = Field(nullable=False)
    last_updated: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
