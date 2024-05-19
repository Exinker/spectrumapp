from PySide6 import QtCore


def getdefault_object_name(obj: QtCore.QObject) -> str:
    """Get a default object name for a given ofject."""
    cls = obj.__class__

    name = cls.__name__
    name = name[0].lower() + name[1:]

    return name
