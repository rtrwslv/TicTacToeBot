"""Module for webhook."""

import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from fastapi import Depends
from handlers import router
from integrations.dispatcher import get_dispatcher
from config import settings


async def setup_webhook(bot: Bot, dp: Dispatcher = Depends(get_dispatcher)) -> None:
    """
    Set up the webhook for the specified Telegram 

    Args:
        bot (Bot): The Telegram bot instance.

    Raises:
        ValueError: If the WEBHOOK_URL environment variable is not set.
    """
    logging.info("Setup webhook")
    dp.include_router(router)
    webhook = await bot.get_webhook_info()
    url = settings.WEBHOOK_DOMAIN

    if url is None:
        raise ValueError("WEBHOOK_DOMAIN env var is not set")
    if webhook.url != url:
        logging.info("Delete webhook")
        await bot.delete_webhook()

    logging.info("Set webhook")
    await bot.set_webhook(url)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start game"),
            BotCommand(command="leave", description="Leave game"),
            BotCommand(command="stats", description="Game stats"),
        ]
    )

    logging.info("Finish setup")
