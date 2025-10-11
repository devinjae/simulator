"""
News Event model
"""

from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid_utils import uuid7


class NewsEvent(SQLModel, table=True):
    __tablename__ = "news_events"

    id: UUID = Field(default_factory=uuid7, primary_key=True)
    ts_release_ms: int = Field(nullable=False, index=True)
    headline: str = Field(nullable=False)
    magnitude: float = Field(nullable=False)
    decay_halflife_s: float = Field(nullable=False)
    shock_type: str = Field(nullable=False)
    scope: str = Field(nullable=False)
