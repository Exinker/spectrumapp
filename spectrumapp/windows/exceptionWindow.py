from enum import Enum, auto

from PySide6 import QtWidgets

from spectrumapp.exceptions import format_exception
from spectrumapp.utils.finder import find_window


class ExceptionLevel(Enum):
    fatal = auto()
    error = auto()
    warning = auto()
    info = auto()


class ExceptionDialog:

    def __init__(self, message: str | None = None, info: str | None = None, level: ExceptionLevel = ExceptionLevel.warning, parent: QtWidgets.QWidget | None = None):
        self.message = message or ''
        self.info = info or format_exception()
        self.level = level
        self.parent = parent or find_window('mainWindow')

    @property
    def dialog(self) -> type[QtWidgets.QMessageBox]:
        level = self.level

        window = QtWidgets.QMessageBox()
        if level == ExceptionLevel.fatal:
            return window.critical
        if level == ExceptionLevel.error:
            return window.critical
        if level == ExceptionLevel.warning:
            return window.warning
        if level == ExceptionLevel.info:
            return window.information

        raise ValueError(f'Level {level} is not supported yet!')

    @property
    def template(self) -> str:
        if not self.message:
            return '{info}'

        return '{message}\n\n{info}'

    @property
    def title(self) -> str:
        level = self.level

        if level == ExceptionLevel.fatal:
            return 'Fatal'
        if level == ExceptionLevel.error:
            return 'Error'
        if level == ExceptionLevel.warning:
            return 'Warning'
        if level == ExceptionLevel.info:
            return 'Info'

        raise ValueError(f'Level {level} is not supported yet!')

    @property
    def text(self) -> str:
        template = self.template

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


if __name__ == '__main__':

    app = QtWidgets.QApplication()

    message = 'Try to calculate "1/0".'
    try:
        1/0
    except ZeroDivisionError:
        dialog = ExceptionDialog(
            message=message,
            level=ExceptionLevel.error,
        )
        dialog.show()

    app.quit()
