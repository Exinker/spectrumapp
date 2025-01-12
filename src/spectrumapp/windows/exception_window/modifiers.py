from functools import wraps
from typing import Any, Callable

from spectrumapp.windows.exception_window import ExceptionDialog, ExceptionLevel


def attempt(level: ExceptionLevel = ExceptionLevel.ERROR) -> Callable:
    """Attempt decorator for not save windows or process."""

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:

            try:
                return func(*args, **kwargs)

            except Exception:
                dialog = ExceptionDialog(
                    message=f'The attempt to complete {func.__name__} failed.',
                    level=level,
                )
                dialog.show()

        return wrapper
    return decorator
