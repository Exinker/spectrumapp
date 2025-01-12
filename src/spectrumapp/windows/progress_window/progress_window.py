import os
from dataclasses import dataclass, field

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.helpers import find_window
from spectrumapp.paths import pave


@dataclass
class ProgressState:
    progress: int | None = field(default=None)
    info: str | None = field(default=None)
    message: str | None = field(default=None)


class ProgressWindow(QtWidgets.QWidget):

    updated = QtCore.Signal(ProgressState)

    DEFAULT_FLAGS = QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint  # noqa: E501
    DEFAULT_SIZE = QtCore.QSize(680, 200)

    def __init__(self, *args, flags: QtCore.Qt.WindowType | None = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('progressWindow')
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.updated.connect(self.on_updated)

        # flags
        flags = flags or self.DEFAULT_FLAGS
        self.setWindowFlags(flags)

        # style
        filepath = pave(os.path.join('.', 'static', 'progress-window.css'))
        style = open(filepath, 'r').read()
        self.setStyleSheet(style)

        # icon
        filepath = pave(os.path.join('.', 'static', 'icon.ico'))
        icon = QtGui.QIcon(filepath)
        self.setWindowIcon(icon)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(ContentWidget(
            parent=self,
        ))

        # geometry
        self.setFixedSize(self.DEFAULT_SIZE)

        # move window
        window = find_window('splashScreenWindow')
        if window:
            self.move(
                window.geometry().left(),
                window.geometry().bottom(),
            )

    def on_updated(self, state: ProgressState) -> None:

        if state.progress:
            widget = self.findChild(QtWidgets.QProgressBar, 'progressBar')
            widget.setValue(state.progress)
        if state.info:
            widget = self.findChild(QtWidgets.QLabel, 'infoLabel')
            widget.setText(state.info)
        if state.message:
            widget = self.findChild(QtWidgets.QLabel, 'messageLabel')
            widget.setText(state.message)

        # process events on the main window
        app = QtWidgets.QApplication.instance()
        app.processEvents()

    def closeEvent(self, event):  # noqa: N802

        self.setParent(None)
        event.accept()


class ContentWidget(QtWidgets.QFrame):

    DEFAULT_LOGGING_TEXT = ''
    DEFAULT_PROGRESS = 0
    DEFAULT_INFO = '<strong>LOADING</strong>...'
    DEFAULT_MESSAGE = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('contentWidget')

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addSpacing(50)
        layout.addWidget(LoggingPlainTextEditWidget(
            self.DEFAULT_LOGGING_TEXT,
            objectName='loggingPlainText',
            parent=self,
        ))
        layout.addWidget(ProgressBarWidget(
            objectName='progressBar',
            value=self.DEFAULT_PROGRESS,
            parent=self,
        ))
        layout.addWidget(LabelWidget(
            objectName='infoLabel',
            text=self.DEFAULT_INFO,
            parent=self,
        ))
        layout.addWidget(LabelWidget(
            objectName='messageLabel',
            text=self.DEFAULT_MESSAGE,
            parent=self,
        ))
        layout.addSpacing(50)


class LoggingPlainTextEditWidget(QtWidgets.QPlainTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPlaceholderText('')
        self.setEnabled(False)

        # geometry
        self.setFixedHeight(100)


class ProgressBarWidget(QtWidgets.QProgressBar):

    def __init__(self, value: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setValue(value)


class LabelWidget(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
