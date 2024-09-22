"""Module for init."""

from .game import game_router
from .user import user_router

__all__ = (
    "game_router",
    "user_router",
)
