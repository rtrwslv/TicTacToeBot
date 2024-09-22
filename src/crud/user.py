"""Module for user."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schema.user import UserCreate
from metrics import async_integrations_timer


@async_integrations_timer
async def create_user(user: UserCreate, db: AsyncSession):
    """
    Create a new user in the database.

    Args:
        user (UserCreate): The user data to be created.
        db (AsyncSession): The database session used for the operation.

    Returns:
        User: The created user object.
    """
    db_user = User(telegram_id=user.telegram_id, username=user.username)
    db.add(db_user)
    await db.commit()
    return db_user


@async_integrations_timer
async def get_user_by_tg_id(tg_id: int, db: AsyncSession) -> User | None:
    """
    Retrieve a user from the database by their Telegram ID.

    Args:
        tg_id (int): The Telegram ID of the user to be retrieved.
        db (AsyncSession): The database session used for the operation.

    Returns:
        User | None: The user object if found, or None.
    """
    user = await db.execute(select(User).where(User.telegram_id == tg_id))
    user = user.scalar()
    return user
