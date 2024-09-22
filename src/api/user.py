"""Module for user in the game."""

from fastapi import Depends, APIRouter, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from integrations.auth import sign_jwt
from crud.redis import redis_get_model, redis_set_model
from models import User
from crud.user import get_user_by_tg_id, create_user
from schema.user import UserCreate
from config.db import get_db

user_router = APIRouter()


@user_router.post("/users/")
async def create_user_endpoint(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> ORJSONResponse:
    """
    Create a new user.

    Args:
        user (UserCreate): Data for creating a new user.
        db (AsyncSession): Database session.

    Returns:
        ORJSONResponse: Response with the created user in JSON format.

    Raises:
        HTTPException: If a user with the same Telegram ID already exists.
    """
    cached_user = await redis_get_model(User.__tablename__, user.telegram_id)
    if cached_user:
        cached_user["access_token"] = sign_jwt(str(user.telegram_id))
        return ORJSONResponse(cached_user, status_code=status.HTTP_201_CREATED)

    existing_user = await get_user_by_tg_id(user.telegram_id, db)
    if existing_user:
        existing_user.access_token = sign_jwt(str(user.telegram_id))
        return ORJSONResponse(existing_user, status_code=status.HTTP_201_CREATED)
    db_user = await create_user(user, db)
    db_user.access_token = sign_jwt(str(user.telegram_id))
    await redis_set_model(User.__tablename__, db_user.telegram_id, db_user)
    return ORJSONResponse(db_user, status_code=status.HTTP_201_CREATED)
