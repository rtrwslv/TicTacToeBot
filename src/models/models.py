"""Module for models."""

from dataclasses import dataclass
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .meta import Base


@dataclass
class User(Base):
    """Represent a user in the Tic-Tac-Toe game application."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)

    games_as_player1: Mapped[list["Game"]] = relationship(
        "Game", back_populates="player1", foreign_keys="[Game.player1_id]"
    )
    games_as_player2: Mapped[list["Game"]] = relationship(
        "Game", back_populates="player2", foreign_keys="[Game.player2_id]"
    )


@dataclass
class Game(Base):
    """Represent a Tic-Tac-Toe game in the application."""

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    player1_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id"), nullable=False
    )
    player2_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id"), nullable=False
    )
    result: Mapped[str] = mapped_column(String, nullable=False)

    player1: Mapped["User"] = relationship(
        "User", back_populates="games_as_player1", foreign_keys=[player1_id]
    )
    player2: Mapped["User"] = relationship(
        "User", back_populates="games_as_player2", foreign_keys=[player2_id]
    )
