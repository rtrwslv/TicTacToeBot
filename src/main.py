"""Model for main."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.logger import setup_logger
from integrations.redis import get_redis
from middleware.logger import LogServerMiddleware
from models.meta import create_db
from api import game_router, user_router
from metrics import counter_metrics, metrics


def setup_middleware(app: FastAPI) -> None:
    """
    Configure middleware for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None
    """
    app.add_middleware(
        LogServerMiddleware,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware("http")(counter_metrics)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the lifespan of the FastAPI application.

    Yields:
        None: This context manager does not yield any value.
    """
    await create_db()
    setup_logger()
    get_redis()
    print("START WEB APP")
    yield
    print("END WEB APP")


def main() -> FastAPI:
    """
    Create and configures the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    app = FastAPI(lifespan=lifespan)
    app.include_router(user_router)
    app.include_router(game_router)
    app.add_route("/metrics", metrics)

    setup_middleware(app)
    return app
