"""Module for bot."""

from os import getenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import settings


API_TOKEN = getenv('TELEGRAM_API_TOKEN')
bot = Bot(
    token=settings.TELEGRAM_API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


def get_bot() -> Bot:
    """
    Retrieve the current instance of the Bot.

    Returns:
        Bot: The current instance of the Bot.
    """
    return bot
