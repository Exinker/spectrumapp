
import os
import sys
from typing import Callable

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.utils.find import find_window
# from spectrumapp.windows.exceptionWindow import ExceptionWindow  # FIXME: implement ExceptionWindow


# ----------------        decotators        ----------------
def committing(func: Callable) -> Callable:
    """commit editors decorator for PySide6 table views"""

    def inner(self, event):

        # commit all editors of the view
        editors = self.findChildren(QtWidgets.QWidget, 'editor')
        for editor in editors:
            self.commitData(editor)

    return inner


def trying(func: Callable) -> Callable:
    """try/except decorator for PySide6 applications"""

    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except Exception as error:
            ExceptionWindow(
                error=error,
            )

    return inner


def waiting(func) -> Callable:
    """waiting cursor decorator for PySide6 applications"""

    def inner(*args, **kwargs):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        try:
            return func(*args, **kwargs)

        # except Exception as error:
        #     ExceptionWindow(
        #         error=error,
        #     )

        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    return inner


def refreshing(func: Callable):
    """refresh the main window decorator for PySide6 applications"""

    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        finally:
            window = find_window('mainWindow')
            window._onRefreshAppAction()

    return inner
