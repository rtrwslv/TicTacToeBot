"""Module for logger."""

import logging
from contextvars import ContextVar

import yaml


with open("logging.conf.yml", "r") as f:
    LOGGING_CONFIG = yaml.full_load(f)

correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id_ctx")
logger = logging.getLogger("tictactoe")
