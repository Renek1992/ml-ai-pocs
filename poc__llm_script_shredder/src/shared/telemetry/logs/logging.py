"""
Shared function for logging
"""

import sys

import logging
from logging import Logger
from src.shared.common.utils import LogFormatter
from src.shared.common.types import LogLevel

class PythonLogger:
    def get_logger(log_level: LogLevel, name: str) -> Logger:
        log_handler = logging.StreamHandler(stream=sys.stdout)
        logger = logging.getLogger(name)

        formatter = LogFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
        )

        logger.setLevel(log_level)
        log_handler.setFormatter(formatter)
        logger.propagate = False
        logger.addHandler(log_handler)

        return logger