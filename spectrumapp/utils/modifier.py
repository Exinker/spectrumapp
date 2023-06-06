
from typing import Callable

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.utils.find import find_window
from spectrumapp.windows.messageWindow import show_message_dialog, MessageLevel


def wait(func: Callable) -> Callable:
    """Waiting cursor decorator for long time processes."""

    def wrapper(*args, **kwargs):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        try:
            return func(*args, **kwargs)

        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    return wrapper


def attempt(level: MessageLevel = MessageLevel.warning) -> Callable:
    """Attempt decorator for not save windows or process."""

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)

            except Exception:
                show_message_dialog(
                    message=f'The attempt to complete {func.__name__} failed.',
                    level=level,
                )

        return wrapper
    return decorator


def refresh(func: Callable):
    """Refresh decorator for the main window."""

    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        finally:
            window = find_window('mainWindow')
            window._onRefreshAppAction()

    return wrapper


def commit(func: Callable) -> Callable:
    """Сommit editors decorator for PySide6 table views."""

    def wrapper(widget: QtWidgets.QTableView, event: QtCore.QEvent):

        # commit all editors of the view
        editors = widget.findChildren(QtWidgets.QWidget, 'editor')
        for editor in editors:
            widget.commitData(editor)

    return wrapper
