from tkinter import Tk

from PySide6 import QtCore, QtWidgets


def getdefault_object_name(obj: QtCore.QObject, prefix: str = '') -> str:
    """Get a default object name for a given ofject."""
    cls = obj.__class__

    name = prefix + cls.__name__
    name = name[0].lower() + name[1:]

    return name


def getdefault_geometry(window: QtWidgets.QWidget) -> QtCore.QRect:
    """Get a default geometry for a given window."""

    def get_screen_size() -> tuple[int, int]:
        root = Tk()
        root.withdraw()

        return root.winfo_screenwidth(), root.winfo_screenheight()

    screen_width, screen_height = get_screen_size()

    window_width = window.layout().sizeHint().width() if window.layout() else int(screen_width / 4)
    window_height = int(screen_height / 2)
    geometry = QtCore.QRect(int(screen_width/2 - window_width/2), int(screen_height/2 - window_height/2), window_width, window_height)

    return geometry
