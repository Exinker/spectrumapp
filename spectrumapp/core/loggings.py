
import logging
import logging.config
import os
from typing import Callable

from .configs import DEBUG


def log(msg: str) -> Callable:
    logger = logging.getLogger('app')

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            if DEBUG:
                logger.debug(msg)

            return func(*args, **kwargs)
        return wrapper

    return decorator


def setdefault_logging():

    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'file_formatter': {
                'format': '[%(asctime)s: %(levelname)s] %(message)s',
            },
        },

        'handlers': {
            'file_handler': {
                'class': 'logging.FileHandler',
                'level': logging.DEBUG,
                'filename': os.path.join('.', 'app.log'),
                'mode': 'a',
                'formatter': 'file_formatter',
                'encoding': 'utf-8',
            },
        },

        'loggers': {
            'app': {
                'level': logging.DEBUG,
                'handlers': ['file_handler', ],
                'propagate': False,
            }
        }
    }
    logging.config.dictConfig(LOGGING_CONFIG)
