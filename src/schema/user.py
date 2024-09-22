"""Module for user."""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Model for create user."""

    telegram_id: int
    username: str
