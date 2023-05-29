
from PySide6 import QtCore, QtGui, QtWidgets


# --------        find windows and widgets        --------
def find_window(__window_name: str) -> QtCore.QObject | None:

    app = QtWidgets.QApplication.instance()
    if app:
        for widget in app.topLevelWidgets():
            if widget.objectName() == __window_name:
                return widget

    return None
