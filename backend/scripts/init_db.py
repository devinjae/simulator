"""
Database initialization script
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel

from app.db.database import engine

# Import all models to register them with SQLModel metadata
from app.models import (
    Bot,
    BotPosition,
    Instrument,
    InstrumentFactorExposure,
    InstrumentSectorExposure,
    MacroFactor,
    NewsEvent,
    NewsEventFactor,
    Sector,
)


def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_database()
