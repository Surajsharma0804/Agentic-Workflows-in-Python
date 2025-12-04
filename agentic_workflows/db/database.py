"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Optional
from ..config import get_settings

settings = get_settings()

# Lazy initialization - don't create engine at import time
_engine: Optional[any] = None
_SessionLocal: Optional[any] = None


def get_engine():
    """Get or create database engine (lazy initialization)."""
    global _engine
    if _engine is None:
        try:
            _engine = create_engine(
                settings.database_url,
                pool_pre_ping=True,
                pool_size=5,  # Reduced for FREE tier (max 97 connections)
                max_overflow=5,  # Reduced for FREE tier
                pool_recycle=300,  # Recycle connections every 5 min
                pool_timeout=30,
                connect_args={"connect_timeout": 10}  # Add connection timeout
            )
        except Exception as e:
            # If database connection fails, use SQLite fallback
            import structlog
            logger = structlog.get_logger()
            logger.warning("database_connection_failed", error=str(e), fallback="sqlite")
            _engine = create_engine("sqlite:///./agentic_workflows.db")
    return _engine


def get_session_local():
    """Get or create session factory (lazy initialization)."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


# For backward compatibility
engine = property(lambda self: get_engine())
SessionLocal = property(lambda self: get_session_local())


def get_db() -> Session:
    """Get database session."""
    session_local = get_session_local()
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Get database session as context manager."""
    session_local = get_session_local()
    db = session_local()
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
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
