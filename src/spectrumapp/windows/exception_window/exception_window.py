from enum import Enum, auto
from typing import Type, assert_never

from PySide6 import QtWidgets

from spectrumapp.exceptions import format_exception
from spectrumapp.helpers import find_window


class ExceptionLevel(Enum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


class ExceptionDialog:

    def __init__(
        self,
        message: str = '',
        info: str = '',
        level: ExceptionLevel = ExceptionLevel.WARNING,
        parent: QtWidgets.QWidget | None = None,
    ):
        self.message = message
        self.info = info or format_exception()
        self.level = level
        self.parent = parent or find_window('mainWindow')

    @property
    def dialog(self) -> Type[QtWidgets.QMessageBox]:

        match self.level:
            case ExceptionLevel.ERROR:
                return QtWidgets.QMessageBox.critical
            case ExceptionLevel.WARNING:
                return QtWidgets.QMessageBox.warning
            case ExceptionLevel.INFO:
                return QtWidgets.QMessageBox.information
            case _:
                assert_never(self.level)

    @property
    def title(self) -> str:

        match self.level:
            case ExceptionLevel.ERROR:
                return 'Error'
            case ExceptionLevel.WARNING:
                return 'Warning'
            case ExceptionLevel.INFO:
                return 'Info'
            case _:
                assert_never(self.level)

    @property
    def text(self) -> str:

        template = _get_text_template(
            message=self.message,
        )
        return template.format(
            message=self.message,
            info=self.info,
        )

    def show(self) -> None:
        self.dialog(
            self.parent,
            self.title,
            self.text,
            buttons=QtWidgets.QMessageBox.Close,
            defaultButton=QtWidgets.QMessageBox.Close,
        )


def _get_text_template(message: str) -> str:

    if message:
        return '{message}\n\n{info}'
    return '{info}'


if __name__ == '__main__':

    app = QtWidgets.QApplication()

    message = 'Try to calculate "1/0".'
    try:
        1/0
    except ZeroDivisionError:
        dialog = ExceptionDialog(
            message=message,
            level=ExceptionLevel.ERROR,
        )
        dialog.show()

    app.quit()
