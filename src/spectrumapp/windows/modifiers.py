from functools import wraps
from typing import Any, Callable

from PySide6 import QtCore, QtWidgets

from spectrumapp.helpers import find_window


def wait(func: Callable) -> Callable:
    """Waiting cursor decorator for long time processes."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        is_decorated = QtWidgets.QApplication.overrideCursor() is None  # check nested decorations
        if is_decorated:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        try:
            return func(*args, **kwargs)
        except Exception:
            raise
        finally:
            if is_decorated:
                QtWidgets.QApplication.restoreOverrideCursor()

    return wrapper


def refresh(__window_name: str = 'mainWindow') -> Callable:
    """Refresh decorator for selected window."""

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:

            try:
                return func(*args, **kwargs)
            except Exception:
                raise
            finally:
                window = find_window(__window_name)
                window.refreshed.emit()

        return wrapper
    return decorator


def close(__window_name: str) -> Callable:
    """Close decorator for selected window."""

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            window = find_window(__window_name)
            if window:
                window.close()

            return func(*args, **kwargs)

        return wrapper
    return decorator
