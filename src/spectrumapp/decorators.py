from functools import wraps
from typing import Any, Callable

from PySide6 import QtCore, QtWidgets

from spectrumapp.helpers import find_window
from spectrumapp.windows.exceptionWindow import ExceptionDialog, ExceptionLevel


def wait(func: Callable) -> Callable:
    """Waiting cursor decorator for long time processes."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        to_decorate = QtWidgets.QApplication.overrideCursor() is None  # check nested decorations
        if to_decorate:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        try:
            return func(*args, **kwargs)

        except Exception:
            raise  # propagate an exception

        finally:
            if to_decorate:
                QtWidgets.QApplication.restoreOverrideCursor()

    return wrapper


def attempt(level: ExceptionLevel = ExceptionLevel.WARNING) -> Callable:
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
                window._onRefreshAction()

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


def commit(func: Callable) -> Callable:
    """Close all editors (by commiting) decorator for PySide6 table views."""

    @wraps(func)
    def wrapper(view: QtWidgets.QTableView, event: QtCore.QEvent) -> None:
        editors = view.findChildren(QtWidgets.QWidget, 'editor')

        for editor in editors:
            view.commitData(editor)

    return wrapper
