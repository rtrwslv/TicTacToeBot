"""Module for leave in the bot."""

from aiogram import Bot, types
from handlers import router
from aiogram.filters import Command


@router.message(Command("leave"))
async def leave_game(message: types.Message, bot: Bot, games: dict):
    """
    Handle the /leave command, allowing a player to exit a game.

    Args:
        message (types.Message): The Telegram message containing the command.
        bot (Bot): The Telegram bot instance.
        games (dict): A dictionary containing games, with game IDs as keys.

    Returns:
        None: This function returns None.
    """
    if message.from_user is None:
        return

    user_id = message.from_user.id
    game_id = next(
        (gid for gid, game in games.items() if user_id in game['players']),
        None
    )

    if game_id is not None:
        opponent = next(
            pid for pid in games[game_id]['players'] if pid != user_id
        )
        await bot.send_message(
            opponent,
            f"{games[game_id]['players'][user_id]['username']} покинул игру.",
            reply_markup=None
        )
        del games[game_id]
        await message.answer("Вы покинули игру.")
    else:
        await message.answer("Вы не находитесь в игре.")
