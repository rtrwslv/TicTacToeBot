"""Module for state."""

from aiogram.fsm.state import StatesGroup, State


class GameState(StatesGroup):
    """Define the states for a Tic-Tac-Toe game session."""
    games = State()
