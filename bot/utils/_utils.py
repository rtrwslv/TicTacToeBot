"""Module for utils in the bot."""

import httpx
import jwt
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatFullInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from logger import correlation_id_ctx


def get_game_keyboard(board):
    """
    Create an inline keyboard for the Tic-Tac-Toe on the current board state.

    Args:
        board (list): A 2D list representing the current state of the board.

    Returns:
        InlineKeyboardMarkup: An inline keyboard markup object.
    """
    builder = InlineKeyboardBuilder()
    for i in range(3):
        row = []
        for j in range(3):
            cell = board[i][j]
            text = cell if cell != " " else " "
            callback_data = f"cell_{i}_{j}"
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=callback_data
            ))
        builder.add(*row)
    builder.adjust(3, 3, 3)
    return builder.as_markup()


def check_winner(board):
    """
    Check the Tic-Tac-Toe board for a winner.

    Args:
        board (list): A 2D list representing the current state of the board.

    Returns:
        str or None: The symbol of the winning player ('X' or 'O').
    """
    lines = []
    lines.extend(board)
    lines.extend([[board[i][j] for i in range(3)] for j in range(3)])
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line[0] == line[1] == line[2] and line[0] != " ":
            return line[0]
    return None


def is_board_full(board):
    """
    Check if the Tic-Tac-Toe board is full.

    Args:
        board (list): A 2D list representing the current state of the board.

    Returns:
        bool: True if the board is full, False if there are any empty cells.
    """
    return all(cell != " " for row in board for cell in row)


async def get_chat_info_by_id(bot: Bot, user_id: int) -> ChatFullInfo:
    """
    Retrieve detailed information about a Telegram user by their ID.

    Args:
        bot (Bot): The bot instance used to interact with the Telegram API.
        user_id (int): The ID of the user for which to retrieve information.

    Returns:
        ChatFullInfo: An object containing detailed information about the user.
    """
    chat_info = await bot.get_chat(user_id)
    return chat_info


async def get_auth_from_state(
    state: FSMContext, api_url: str, user_id: int, username: str
) -> str:
    """
    Retrieve or refresh the access token from the state.

    Args:
        state (FSMContext): The finite state machine context that holds
                            the current state data.
        api_url (str): The base URL of the API used.
        user_id (int): The unique identifier of the user.
        username (str): The username of the user.

    Returns:
        str: The access token, either retrieved from the state.

    Raises:
        HTTPException: If there is an error during the API request.
    """
    state_data = await state.get_data()
    if "access_token" not in state_data.keys() or (
        jwt.decode(
            state_data["access_token"],
            options={"verify_signature": False}
        ).get(
            "exp"
        )
        is None
    ):
        async with httpx.AsyncClient(base_url=api_url) as client:
            response = await client.post(
                "/users/",
                json={
                    "telegram_id": user_id,
                    "username": username,
                },
            )
            new_token = response.json()["access_token"]
            await state.update_data({"access_token": new_token})
            return new_token

    return state_data["access_token"]


def build_headers(access_token):
    """
    Construct HTTP headers for authorization.

    Args:
        access_token (str): The access token.

    Returns:
        dict: A dictionary containing the Authorization.
    """
    return {
        "Authorization": f"Bearer {access_token}",
        "X-Correlation-Id": correlation_id_ctx.get(),
    }
