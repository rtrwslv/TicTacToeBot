"""Module for game router."""

from fastapi import Depends, APIRouter, status
from fastapi.responses import ORJSONResponse
from integrations.bearer import JWTBearer
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from crud.game import get_user_games
from schema.game import GameCreate
from config.db import get_db
from crud.game import create_game

game_router = APIRouter()


@game_router.post("/games/")
async def create_game_endpoint(
    game: GameCreate,
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(JWTBearer()),
) -> ORJSONResponse:
    """
    Create a new game.

    Args:
        game (GameCreate): Data for creating a new game.
        db (AsyncSession): Database session.

    Returns:
        ORJSONResponse: Response with the created game in JSON format.
    """
    db_game = await create_game(game, db)
    return ORJSONResponse(db_game, status_code=status.HTTP_201_CREATED)


@game_router.get("/games/{user_id}")
async def get_games_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(JWTBearer()),
) -> ORJSONResponse:
    """
    Retrieve all games played by a specific user.

    Args:
        user_id (int): The ID of the user to retrieve games for.
        db (AsyncSession): Database session.

    Returns:
        ORJSONResponse: Response with a list played by the user in JSON.
    """
    games = await get_user_games(user_id, db)
    return ORJSONResponse(games)
