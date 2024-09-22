"""Module for start in the bot."""

import logging
import uuid
from http import HTTPStatus
from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from handlers.router import router
from utils.state import GameState
from utils import get_game_keyboard

import httpx


@router.message(
    Command("start"),
)
async def start_game(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
    queue: list,
    api_url: str,
):
    """
    Initiate a new Tic-Tac-Toe game or adds the user to the waiting queue.

    Args:
        message (types.Message): The message object initiating the game.
        bot (Bot): The bot used to send messages with the Telegram API.
        state (FSMContext): Machine context for managing user states.
        games (dict): A dictionary containing games, keyed by game ID.
        queue (list): A list of user IDs waiting for an opponent.
        api_url (str): A string representing api url.
    """
    logging.info(f"MESSAGE {message}")
    if message.from_user is None:
        return

    if message.from_user.id in queue:
        await message.answer("Вы уже в очереди. Пожалуйста, подождите противника.")
        return
    async with httpx.AsyncClient(base_url=api_url) as client:
        response = await client.post(
            "/users/",
            json={
                "telegram_id": message.from_user.id,
                "username": message.from_user.username,
            },
        )
        await state.update_data({"access_token": response.json()["access_token"]})
        if response.status_code != HTTPStatus.CREATED:
            await message.answer(
                "Не удалось зарегистрировать пользователя. Попробуйте еще раз."
            )
            return

    if queue:
        opponent = queue.pop(0)
        board = [[" " for _ in range(3)] for _ in range(3)]
        game_id = str(uuid.uuid4())
        games = await state.get_data('games')
        games[game_id] = {
            "board": board,
            "turn": "X",
            "players": {
                message.from_user.id: {
                    "symbol": "X",
                    "username": message.from_user.first_name,
                },
                opponent: {
                    "symbol": "O",
                    "username": (
                        await bot.get_chat_member(opponent, opponent)
                    ).user.first_name,
                },
            },
        }
        await bot.send_message(
            opponent,
            (
                f"{
                    games[game_id]['players'][message.from_user.id]['username']
                }"
                f" бросил вам вызов! Игра началась. Вы за 'X' и ходите первым!."
            ),
            reply_markup=get_game_keyboard(board),
        )
        await message.answer(
            "Игра началась! Вы за 'O'. Ожидайте ход соперника", reply_markup=get_game_keyboard(board)
        )
    else:
        queue.append(message.from_user.id)
        await message.answer("Вы добавлены в очередь. Ожидание противника...")
