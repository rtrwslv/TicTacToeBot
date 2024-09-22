"""Module for main_webhook."""

import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.tg import tg_router
from integrations import get_bot, get_dispatcher
from middleware.logger import LogServerMiddleware
from utils.webhook import setup_webhook
from utils.background_tasks import tg_background_tasks
from utils.logger import setup_logger


def setup_middleware(app: FastAPI) -> None:
    """
    Set up middleware for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.add_middleware(
        LogServerMiddleware,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # type: ignore
        allow_credentials=True,  # type: ignore
        allow_methods=["*"],  # type: ignore
        allow_headers=["*"],  # type: ignore
    )


def setup_routers(app: FastAPI) -> None:
    """
    Set up routers for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(tg_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage the lifespan of the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    print("START APP")
    await setup_webhook(get_bot(), get_dispatcher())
    setup_logger()

    yield

    print("Stopping")

    while len(tg_background_tasks) > 0:
        logging.info("%s tasks left", len(tg_background_tasks))
        await asyncio.sleep(0)

    print("Stopped")


def create_app() -> FastAPI:
    """
    Create the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(docs_url="/swagger", lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)

    return app
