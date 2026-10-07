"""Configure SQLAlchemy's PostgreSQL engine and sessions."""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Copy .env.example to .env and set your PostgreSQL password."
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class that registers ORM models and their table definitions."""


def get_db_session() -> Generator[Session, None, None]:
    """Provide one database session per API request and always close it."""
    with SessionLocal() as session:
        yield session
