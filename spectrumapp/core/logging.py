
import json
import logging
import logging.config
import os
from typing import Callable

from PySide6 import QtWidgets, QtCore, QtGui

from .exception import eprint


def _to_str(value, key: str | None = None) -> str:

    try:
        if key:
            if isinstance(value, QtCore.QRect):
                value = value.getRect()

            return '{key}: {value}'.format(
                key=key,
                value=json.dumps(value),
            )

        else:
            return '{value}'.format(
                value=json.dumps(value),
            )

    except TypeError as error:
        eprint(error)
        return ''


def _get_log_context(*args, **kwargs) -> str:
    context = []

    for value in args:
        context.append(_to_str(value=value))

    for key, value in kwargs.items():
        context.append(_to_str(value=value, key=key))

    return '; '.join(context)


def log(msg: str, level: int = logging.DEBUG) -> Callable:
    logger = logging.getLogger('app')

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            is_debugging = json.loads(
                os.environ.get('DEBUG', 'false')
            )

            if is_debugging or (level > logging.DEBUG):
                context = _get_log_context(*args, **kwargs)
                if context:
                    logger.log(level, f'{msg} ({context})')

                else:
                    logger.log(level, msg)

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
