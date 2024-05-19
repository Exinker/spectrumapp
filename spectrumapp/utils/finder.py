from PySide6 import QtCore, QtGui, QtWidgets


# --------        windows        --------
def find_window(__window_name: str) -> QtCore.QObject | None:
    """Find window by name."""
    app = QtWidgets.QApplication.instance()

    if app:
        for widget in app.topLevelWidgets():
            if widget.objectName() == __window_name:
                return widget

    return None


# --------        widgets        --------
def find_action(__widget: QtWidgets.QWidget, text: str) -> QtGui.QAction | None:
    """Find action by text."""
    actions = __widget.actions()

    for action in actions:
        if action.text() == text:
            return action


def find_menu(__widget: QtWidgets.QWidget, title: str) -> QtWidgets.QMenu | None:
    """Find action by title."""
    for widget in __widget.children():
        if isinstance(widget, QtWidgets.QMenu) and widget.title() == title:
            return widget

    return None


def find_tab(__widget: QtWidgets.QTabWidget, text: str) -> QtWidgets.QWidget:
    """Find tab by text."""

    for i in range(__widget.count()):
        if text == __widget.tabText(i):
            return __widget.widget(i)
