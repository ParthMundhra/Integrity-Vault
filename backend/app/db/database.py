"""
Database configuration for the backend service.

This module is responsible for creating the PostgreSQL database engine and
dependency helpers. It does not define ORM models; those should live in a
dedicated models package.
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://forensics_user:forensics_password@localhost:5432/forensics_db",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session.

    Callers must not hold on to the session outside the request scope.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

