
import traceback
from enum import Enum, auto
from typing import Callable

from PySide6 import QtWidgets, QtCore, QtGui

from spectrumapp.utils.find import find_window
from spectrumapp.core.exception import format_exception


class MessageLevel(Enum):
    fatal = auto()
    error = auto()
    warning = auto()
    info = auto()


def _fetch_title(__level: MessageLevel) -> str:
    return {
        MessageLevel.fatal: 'Fatal',
        MessageLevel.error: 'Error',
        MessageLevel.warning: 'Warning',
        MessageLevel.info: 'Info',
    }.get(__level)


def _fetch_dialog(__level: MessageLevel) -> Callable:

    window = QtWidgets.QMessageBox()
    return {
        MessageLevel.fatal: window.critical,
        MessageLevel.error: window.critical,
        MessageLevel.warning: window.warning,
        MessageLevel.info: window.information,
    }.get(__level)


def show_message_dialog(msg: str | None = None, info: str | None = None, level: MessageLevel = MessageLevel.warning):
        """Show exception message box.

        To show exception traceback `info` have to be `None`!
        """
        template = '{info}' if msg is None else '{msg}\n\n\n{info}'
        info = format_exception() if info is None else info

        dialog = _fetch_dialog(level)
        parent = find_window('mainWindow')
        title = _fetch_title(level)
        text = template.format(
            msg=msg,
            info=info,
        )

        dialog(
            parent,
            title,
            text,
            buttons=QtWidgets.QMessageBox.Close,
            defaultButton=QtWidgets.QMessageBox.Close,
        )


if __name__ == '__main__':

    app = QtWidgets.QApplication()

    message = 'Try to calculate "1/0".'
    try:
        1/0
    except ZeroDivisionError as error:
        show_message_dialog(msg=message, level=MessageLevel.info)

    app.quit()
