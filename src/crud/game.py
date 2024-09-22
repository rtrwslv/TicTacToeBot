"""Module for game."""

from typing import Sequence
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from metrics import async_integrations_timer
from models import Game
from schema.game import GameCreate


@async_integrations_timer
async def create_game(game: GameCreate, db: AsyncSession) -> Game:
    """
    Create a new game in the database.

    Args:
        game (GameCreate): The game data to be created.
        db (AsyncSession): The database session used for the operation.

    Returns:
        Game: The created game object.
    """
    db_game = Game(
        player1_id=game.player1_id,
        player2_id=game.player2_id,
        result=game.result)
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game


@async_integrations_timer
async def get_user_games(user_id: int, db: AsyncSession) -> Sequence[Game]:
    """
    Retrieve all games associated with a user.

    Args:
        user_id (int): The ID of the user whose games are to be retrieved.
        db (AsyncSession): The database session used for the operation.

    Returns:
        Sequence[Game]: A sequence of game objects associated with the user.
    """
    result = await db.execute(
        select(Game).filter(
            or_(
                Game.player1_id == user_id,
                Game.player2_id == user_id
            )
        )
    )
    games = result.scalars().all()
    return games
