"""Module for logger."""

import logging.config
from os import getenv


from logger import LOGGING_CONFIG, logger


def setup_logger() -> None:
    """
    Configure the logging settings for the application.

    Returns:
        None
    """
    logging.config.dictConfig(LOGGING_CONFIG)

    if getenv("DEBUG") == "debug":
        logger.setLevel(logging.DEBUG)
