"""Module for dispatcher."""

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from integrations.redis_connection import get_redis
from integrations.bot import get_bot
from config import settings

redis = get_redis()
storage = RedisStorage(redis)
dp = Dispatcher(
    bot=get_bot(),
    storage=storage,
    queue=[],
    api_url=settings.API_URL
)


def get_dispatcher() -> Dispatcher:
    """
    Retrieve the current instance of the Dispatcher.

    Returns:
        Dispatcher: The current instance of the Dispatcher.
    """
    return dp
