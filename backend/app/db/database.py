"""
Database configuration for the backend service.

This module is responsible for creating the PostgreSQL database engine and
dependency helpers. It does not define ORM models; those should live in a
dedicated models package.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
