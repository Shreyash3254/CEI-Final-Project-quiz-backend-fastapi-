"""
Database configuration and session management.

Sets up SQLite database using SQLAlchemy ORM.
Provides a session dependency for FastAPI routes.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL — creates a local file 'quiz.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./quiz.db"

# Create the SQLAlchemy engine
# connect_args is needed for SQLite to allow multi-threaded access
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session to each request.
    Ensures the session is closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
