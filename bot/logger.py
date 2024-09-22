"""Module for logger."""

import logging
from contextvars import ContextVar

import yaml

with open("logging_bot.conf.yml") as f:
    LOGGING_CONFIG = yaml.full_load(f)


class ConsoleFormatter(logging.Formatter):
    """
    Custom logging formatter for console output.

    Inherits from:
        logging.Formatter: The base class for all logging formatters.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message, including the correlation ID.
        """
        try:
            correlation_id = correlation_id_ctx.get()
            return "[%s] %s" % (correlation_id, super().format(record))
        except LookupError:
            return super().format(record)


correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id_ctx")
logger = logging.getLogger("tictactoe_bot")
