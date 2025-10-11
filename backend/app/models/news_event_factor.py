"""
News Event Factor model (junction table)
"""

from uuid import UUID

from sqlmodel import Field, ForeignKey, SQLModel


class NewsEventFactor(SQLModel, table=True):
    __tablename__ = "news_event_factors"

    news_event_id: UUID = Field(foreign_key="news_events.id", primary_key=True)
    factor_id: UUID = Field(foreign_key="macro_factors.id", primary_key=True)
