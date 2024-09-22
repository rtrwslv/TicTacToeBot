"""Module for db."""

from typing import AsyncGenerator, Union

from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from config import settings


def create_engine() -> AsyncEngine:
    """
    Create and returns an asynchronous SQLAlchemy engine.

    Returns:
        AsyncEngine: An instance of the asynchronous SQLAlchemy engine.
    """
    return create_async_engine(
        settings.POSTGRES_URL,
        poolclass=AsyncAdaptedQueuePool,
        connect_args={
            'statement_cache_size': 0,
        },
    )


engine = create_engine()


def create_session(
    engine: Union[AsyncEngine, None] = None
) -> async_sessionmaker[AsyncSession]:
    """
    Create an asynchronous session maker for SQLAlchemy.

    Args:
        engine (Union[AsyncEngine, None], optional): An optional AsyncEngine.

    Returns:
        async_sessionmaker[AsyncSession]: An async session maker.
    """
    return async_sessionmaker(
        bind=engine or create_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


async_session = create_session(engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session generator.

    Yields:
        AsyncSession: An asynchronous database session for executing queries.
    """
    async with async_session() as session:
        yield session
