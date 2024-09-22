"""Module for logger."""

from datetime import datetime
import logging
import uuid

from starlette.types import ASGIApp, Receive, Scope, Send

from logger import correlation_id_ctx


class LogServerMiddleware:
    """
    Middleware for logging correlation IDs in ASGI applications.

    Attributes:
        app (ASGIApp): The ASGI application.
    """

    def __init__(self, app: ASGIApp):
        """
        Initialize the LogServerMiddleware with the given ASGI application.

        Args:
            app (ASGIApp): The ASGI application to wrap with this middleware.
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Process incoming requests and sets a correlation ID.

        Args:
            scope (Scope): The ASGI scope containing request information.
            receive (Receive): A callable to receive messages from the client.
            send (Send): A callable to send messages to the client.

        Returns:
            None
        """
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        for header, value in scope["headers"]:
            if header == b"x-correlation-id":
                correlation_id = value.decode()
                break
        else:
            correlation_id = uuid.uuid4().hex

        correlation_id_ctx.set(correlation_id)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(
            f"[{correlation_id}] - {current_time} {scope['method']} {scope['path']}"
        )

        await self.app(scope, receive, send)
