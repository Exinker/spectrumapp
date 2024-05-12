import json
import logging
import logging.config
import os
from typing import Any, Callable

from PySide6 import QtCore


def setdefault_logger():
    """Setup default logger."""

    config = {
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
                'handlers': ['file_handler'],
                'propagate': False,
            },
        },
    }

    logging.config.dictConfig(config)


# ---------        decorators        ---------
def log(message: str, level: int = logging.DEBUG) -> Callable:
    """Logging decorator."""
    logger = logging.getLogger('app')

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):

            if os.environ['DEBUG'] or (level > logging.DEBUG):

                context = parse_context(*args, **kwargs)
                if context:
                    logger.log(level, f'{message} ({context})')

                else:
                    logger.log(level, message)

            return func(*args, **kwargs)
        return wrapper

    return decorator


# ---------        private        ---------
def parse_context(*args, **kwargs) -> str:
    """Parse params of the executed function's."""
    items = []

    # parse args
    for value in args:
        item = format_context(value=value)
        if item:
            items.append(item)

    # parse kwargs
    for key, value in kwargs.items():
        item = format_context(value=value, key=key)
        if item:
            items.append(item)

    #
    return '; '.join(items)


def format_context(value: Any, key: str | None = None) -> str:
    """Format param of the executed function's."""
    template = '{key}: {value}' if key else '{value}'

    try:
        if isinstance(value, QtCore.QRect):
            return template.format(
                key=key,
                value=json.dumps(value.getRect()),
            )

        return '{value}'.format(
            value=json.dumps(value),
        )

    except TypeError:
        return ''
