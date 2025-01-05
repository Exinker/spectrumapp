import json
import logging
import logging.config
from functools import wraps
from typing import Any, Callable

from PySide6 import QtCore

from spectrumapp.config import LOGGING_LEVEL


LOGGER = logging.getLogger('spectrumapp')


def log(message: str, level: int = logging.DEBUG) -> Callable:
    """Logging decorator."""

    def decorator(func: Callable):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if level or (LOGGING_LEVEL > logging.DEBUG):

                context = _parse_context(*args, **kwargs)
                if context:
                    LOGGER.log(level, '%s %s', message, context)
                else:
                    LOGGER.log(level, '%s', message)

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
