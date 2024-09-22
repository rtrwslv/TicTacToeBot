"""Module for schema."""

from pydantic import UUID4, BaseModel


class GameCreate(BaseModel):
    """Model for create game."""

    player1_id: int
    player2_id: int
    result: str


class GameResponse(GameCreate):
    """Model for ask with information about game."""

    id: UUID4
