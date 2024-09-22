"""Module for redis."""

from datetime import timedelta
from typing import Any

import orjson

from integrations.redis import get_redis
from metrics import async_integrations_timer


async def get_model_cache(model: str, user_id: int) -> str:
    """
    Generate a cache key for a specific model and user.

    Args:
        model (str): The name of the model.
        user_id (int): The ID of the user.

    Returns:
        str: The generated cache key.
    """
    return f"TICTACTOE:{model}:{user_id}"


@async_integrations_timer
async def redis_set_model(model: str, model_id: int, payload: Any) -> None:
    """
    Store a model payload in Redis cache.

    Args:
        model (str): The name of the model.
        model_id (int): The ID of the model.
        payload (Any): The data to be stored in the cache.

    Returns:
        None
    """
    redis = get_redis()
    redis_key = await get_model_cache(model, model_id)
    await redis.set(redis_key, orjson.dumps(payload), ex=timedelta(minutes=10))


@async_integrations_timer
async def redis_get_model(model: str, model_id: int) -> dict[str, str]:
    """
    Retrieve a model payload from Redis cache.

    Args:
        model (str): The name of the model.
        model_id (int): The ID of the model.

    Returns:
        dict[str, str]: The deserialized payload from the cache.
    """
    redis = get_redis()
    redis_key = await get_model_cache(model, model_id)
    cache = await redis.get(redis_key)
    if cache is None:
        return {}
    return orjson.loads(cache)


@async_integrations_timer
async def redis_drop_model_key(model: str, model_id: int) -> None:
    """
    Delete a model key from Redis cache.

    Args:
        model (str): The name of the model.
        model_id (int): The ID of the model.

    Returns:
        None
    """
    redis = get_redis()
    redis_key = await get_model_cache(model, model_id)
    await redis.delete(redis_key)
