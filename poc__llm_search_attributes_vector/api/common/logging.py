"""
Shared function for logging
"""
import os
import sys

import logging
from logging import Logger
from api.common.utils import LogFormatter


class PythonLogger:
    def get_logger(name: str) -> Logger:
        log_handler = logging.StreamHandler(stream=sys.stdout)
        logger = logging.getLogger(name)

        formatter = LogFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
        )

        logger.setLevel(os.environ.get('LOG_LEVEL'))
        log_handler.setFormatter(formatter)
        logger.propagate = False
        logger.addHandler(log_handler)

        return logger