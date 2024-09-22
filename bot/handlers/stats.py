"""Module for stats."""

from http import HTTPStatus
from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils import get_auth_from_state, get_chat_info_by_id, build_headers
from handlers.router import router

import httpx


@router.message(
    Command("stats"),
)
async def show_stats(message: types.Message, bot: Bot, state: FSMContext, api_url: str):
    """
    Display the user's latest 10 Tic-Tac-Toe game results.

    Args:
        message (types.Message): The message object /stats command.
        bot (Bot): The bot used to send messages.
        api_url (str): The url to api.
    """
    if message.from_user is None:
        return
    user_id = message.from_user.id
    access_token = await get_auth_from_state(
        state, api_url, user_id, message.from_user.username or ""
    )
    async with httpx.AsyncClient(
        base_url=api_url, headers=build_headers(access_token)
    ) as client:
        response = await client.get(f"/games/{user_id}")

        if response.status_code != HTTPStatus.OK:
            await message.answer(
                "Не удалось получить статистику игр. Попробуйте еще раз позже."
            )
            return

        games = response.json()
        if not games:
            await message.answer("У вас нет сыгранных игр.")
            return
        latest_games = games[-10:]
        stats_message = "Ваши последние 10 игр:\n\n"
        for game in latest_games:
            result = game.get("result")
            user1 = await get_chat_info_by_id(bot, game["player1_id"])
            user2 = await get_chat_info_by_id(bot, game["player2_id"])
            if not user1.username or not user2.username or not result:
                continue
            if result == "X":
                result = user1.username
            elif result == "O":
                result = user2.username
            else:
                result = "Ничья"
            stats_message += f"{
                user1.username
            } vs {user2.username} - Результат: {
                result
            } \n"

        await message.answer(stats_message)
