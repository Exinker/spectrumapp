from QtWidgets import QtCore


def getdefault_object_name(self: QtCore.QObject) -> str:
    """Get a default object name for given class."""
    cls = self.__class__

    name = cls.__name__
    name = name[0].lower() + name[1:]

    return name
