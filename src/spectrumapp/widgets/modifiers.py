from functools import wraps
from typing import Callable

from PySide6 import QtCore, QtWidgets


def commit(func: Callable) -> Callable:
    """Close all editors (by commiting) decorator for PySide6 table views."""

    @wraps(func)
    def wrapper(view: QtWidgets.QTableView, event: QtCore.QEvent) -> None:
        editors = view.findChildren(QtWidgets.QWidget, 'editor')

        for editor in editors:
            view.commitData(editor)

    return wrapper
