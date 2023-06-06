
from typing import Callable

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.utils.find import find_window
# from spectrumapp.windows.exceptionWindow import ExceptionWindow  # FIXME: implement ExceptionWindow


def wait(func: Callable) -> Callable:
    """Waiting cursor decorator for long time processes."""

    def inner(*args, **kwargs):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        try:
            return func(*args, **kwargs)

        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    return inner


def attempt(func: Callable) -> Callable:
    """Attempt decorator for not save windows or process."""

    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except Exception as error:
            ExceptionWindow(
                error=error,
            )

    return inner


def refresh(func: Callable):
    """Refresh decorator for the main window."""

    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        finally:
            window = find_window('mainWindow')
            window._onRefreshAppAction()

    return inner


def commit(func: Callable) -> Callable:
    """Сommit editors decorator for PySide6 table views."""

    def inner(widget: QtWidgets.QTableView, event: QtCore.QEvent):

        # commit all editors of the view
        editors = widget.findChildren(QtWidgets.QWidget, 'editor')
        for editor in editors:
            widget.commitData(editor)

    return inner
