"""Module for redis."""

from os import getenv
from redis.asyncio import ConnectionPool, Redis


pool = ConnectionPool(
    host=getenv("REDIS_HOST"),
    port=getenv("REDIS_PORT"),
    password=getenv("REDIS_PASSWORD"),
)


redis = Redis(
    connection_pool=pool,
)


def get_redis() -> Redis:
    """
    Retrieve the current instance of the Redis client.

    Returns:
        Redis: The current instance of the Redis client.
    """
    return redis
