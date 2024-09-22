"""Module for tg."""

import asyncio
import logging
from asyncio import Task
from typing import Any

from aiogram import Bot, Dispatcher, types
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from integrations import get_dispatcher, get_bot
from utils.background_tasks import tg_background_tasks

tg_router = APIRouter()


@tg_router.post("/")
async def tg_api(
    request: Request,
    dp: Dispatcher = Depends(get_dispatcher),
    bot: Bot = Depends(get_bot),
) -> ORJSONResponse:
    """
    Handle incoming Telegram webhook updates.

    Args:
        request (Request): The incoming HTTP request.
        dp (Dispatcher): The dispatcher for handling updates.
        bot (Bot): The Telegram bot instance (default: Depends on get_bot).

    Returns:
        ORJSONResponse: A JSON response indicating success.
    """
    data = await request.json()
    update = types.Update(**data)

    task: Task[Any] = asyncio.create_task(dp.feed_webhook_update(bot, update))
    tg_background_tasks.add(task)

    logging.info(len(tg_background_tasks))

    task.add_done_callback(tg_background_tasks.discard)

    return ORJSONResponse({"success": True})
