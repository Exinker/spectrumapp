
import traceback

from PySide6 import QtWidgets, QtCore, QtGui

from spectrumapp.utils.find import find_window


def show_exception_dialog(message: str | None = None):
        """Show exception message box."""
        template = '{traceback}' if message is None else '{message}\n\n\n{traceback}'

        parent = find_window('mainWindow')
        title = 'Ошибка'
        text = template.format(
            message=message,
            traceback=traceback.format_exc(limit=2),
        )

        QtWidgets.QMessageBox().warning(
            parent,
            title,
            text,
            buttons=QtWidgets.QMessageBox.Close,
            defaultButton=QtWidgets.QMessageBox.Close,
        )


class ExceptionWindow(QtWidgets.QDialog):
    """Exception dialog."""

    def __init__(self, *args, title: str = 'Exception Window', message: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)

        # flags
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # title
        self.setWindowTitle(title)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # layout / content
        contentLayout = QtWidgets.QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(10)
        layout.addLayout(contentLayout)
        layout.addStretch()

        template = '{traceback}' if message is None else '{message}\n\n\n{traceback}'
        textLabel = QtWidgets.QLabel(
            parent=self,
            text=template.format(
                message=message,
                traceback=traceback.format_exc(limit=2),
            ),
        )
        # textLabel.setAlignment(QtCore.Qt.AlignCenter)
        textLabel.setWordWrap(True)
        contentLayout.addWidget(textLabel)

        # layout / handlers
        handlerLayout = QtWidgets.QHBoxLayout()
        handlerLayout.setContentsMargins(0, 0, 0, 0)
        handlerLayout.setSpacing(10)
        layout.addLayout(handlerLayout)

        handlerLayout.addStretch()

        button = QtWidgets.QPushButton('cancel', self)
        button.setObjectName('cancelPushButton')
        button.clicked.connect(self._onPushButtonClicked)
        handlerLayout.addWidget(button)

        # geometry
        self.setMinimumWidth(480)
        self.setMinimumHeight(340)

        #
        self.show()
        self.exec()

    def _onPushButtonClicked(self):
        widget = self.sender()

        if widget.objectName() == 'cancelPushButton':
            self.close()


if __name__ == '__main__':

    app = QtWidgets.QApplication()

    message = 'Try to calculate "1/0".'
    try:
        1/0
    except ZeroDivisionError as error:
        window = ExceptionWindow(message=message)
        # show_exception_dialog(message=message)

    app.quit()
