import json
import logging
import logging.config
from typing import Any, Callable

from PySide6 import QtCore

from spectrumapp.config import LOGGING_LEVEL


def log(message: str, level: int = logging.DEBUG) -> Callable:
    """Logging decorator."""
    logger = logging.getLogger('spectrumapp')

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):

            if level or (logging.getLevelNamesMapping[LOGGING_LEVEL] > logging.DEBUG):

                context = _parse_context(*args, **kwargs)
                if context:
                    logger.log(level, f'{message} ({context})')
                else:
                    logger.log(level, message)

            return func(*args, **kwargs)
        return wrapper

    return decorator


def _parse_context(*args, **kwargs) -> str:
    """Parse params of the executed function's."""
    items = []

    for value in args:
        item = _format_context(value=value)
        if item:
            items.append(item)

    for key, value in kwargs.items():
        item = _format_context(value=value, key=key)
        if item:
            items.append(item)

    return '; '.join(items)


def _format_context(value: Any, key: str | None = None) -> str:
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
