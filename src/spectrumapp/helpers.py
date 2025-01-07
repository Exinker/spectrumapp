import platform
from tkinter import Tk

from PySide6 import QtCore, QtGui, QtWidgets


def find_window(__window_name: str) -> QtCore.QObject | None:
    """Find a window by name."""
    app = QtWidgets.QApplication.instance()

    if app:
        for widget in app.topLevelWidgets():
            if widget.objectName() == __window_name:
                return widget

    return None


def find_action(__widget: QtWidgets.QWidget, text: str) -> QtGui.QAction | None:
    """Find an action by text."""
    actions = __widget.actions()

    for action in actions:
        if action.text() == text:
            return action


def find_menu(__widget: QtWidgets.QWidget, title: str) -> QtWidgets.QMenu | None:
    """Find a menu by title."""
    for widget in __widget.children():
        if isinstance(widget, QtWidgets.QMenu) and widget.title() == title:
            return widget

    return None


def find_tab(__widget: QtWidgets.QTabWidget, text: str) -> QtWidgets.QWidget:
    """Find a tab by text."""

    for i in range(__widget.count()):
        if text == __widget.tabText(i):
            return __widget.widget(i)


def getdefault_object_name(obj: QtCore.QObject, prefix: str = '') -> str:
    """Get a default object name for a given ofject."""
    cls = obj.__class__

    name = prefix + cls.__name__
    name = name[0].lower() + name[1:]

    return name


def getdefault_geometry(window: QtWidgets.QWidget) -> QtCore.QRect:
    """Get a default geometry for a given window."""

    def get_screen_size(default: tuple[int, int] = (1920, 1080)) -> tuple[int, int]:

        match platform.system():
            case 'Windows':
                root = Tk()
                root.withdraw()
                return root.winfo_screenwidth(), root.winfo_screenheight()

            case _:
                return default

    screen_width, screen_height = get_screen_size()

    window_width = window.layout().sizeHint().width() if window.layout() else int(screen_width / 4)
    window_height = int(screen_height / 2)
    geometry = QtCore.QRect(
        int(screen_width/2 - window_width/2),
        int(screen_height/2 - window_height/2),
        window_width,
        window_height,
    )

    return geometry
