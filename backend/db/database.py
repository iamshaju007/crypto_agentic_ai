"""
Database module for async SQLAlchemy connection and session management.

This module initializes the database engine, sessionmaker, and provides
helper functions for database initialization and dependency injection in FastAPI.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.utils.config import get_config
from backend.db.schemas import Base
from typing import AsyncGenerator

# Database URL from config
DATABASE_URL = get_config()["DATABASE_URL"]

# Async engine and session factory
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """
    Initialize the database by creating all tables defined in Base.metadata.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an asynchronous database session.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session
    """
    async with AsyncSessionLocal() as session:
        yield session
