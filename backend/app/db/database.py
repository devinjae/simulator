"""
Database configuration and session management
"""

from sqlmodel import Session, create_engine

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,  # Set to True for SQL query logging
)


# Dependency to get database session
def get_db():
    with Session(engine) as session:
        yield session
