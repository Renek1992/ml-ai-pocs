"""
Shared function for logging
"""

import sys
from typing import Literal
import logging
from logging import Logger
from shared.common.utils import LogFormatter


class PythonLogger:
    def get_logger(name: str, log_level: Literal['INFO', 'DEBUG', 'ERROR', 'WARNING']) -> Logger:
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