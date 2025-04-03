import logging
from datetime import datetime
import functools
from typing import Callable

logger = logging.getLogger(__name__)

def timer_function(func: Callable):
    @functools.wraps(func)
    def wrapper_timer_function(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()
        logger.info(f"{func.__name__} function completed in {int(elapsed // 60)} minutes {elapsed % 60:.2f} seconds.")
        return result
    return wrapper_timer_function