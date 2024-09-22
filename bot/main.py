"""Module for main."""

import logging
import asyncio

from aiogram.types import BotCommand
from bot.handlers import router
from bot.integrations import get_bot, get_dispatcher


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    """Initialize and starts the Telegram bot."""
    bot = get_bot()
    dp = get_dispatcher()
    dp.include_router(router)
    webhook = await bot.get_webhook_info()
    if webhook.url:
        await bot.delete_webhook()
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start game"),
            BotCommand(command="leave", description="Leave game"),
            BotCommand(command="stats", description="Game stats"),
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
