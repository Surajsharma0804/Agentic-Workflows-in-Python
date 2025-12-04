"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from ..config import get_settings

settings = get_settings()

# Create database engine (FREE tier optimized)
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,  # Reduced for FREE tier (max 97 connections)
    max_overflow=5,  # Reduced for FREE tier
    pool_recycle=300,  # Recycle connections every 5 min
    pool_timeout=30
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Get database session as context manager."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    from .models import Base
    Base.metadata.create_all(bind=engine)
