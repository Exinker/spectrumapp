import os
from dataclasses import dataclass, field

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.paths import pave


@dataclass
class SplashScreenState:
    progress: int | None = field(default=None)
    info: str | None = field(default=None)
    message: str | None = field(default=None)


class SplashScreenWindow(QtWidgets.QWidget):
    """Splash screen decorator for Qt applications and long time processes."""

    updated = QtCore.Signal(SplashScreenState)

    DAFAULT_FLAGS = QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint  # noqa: E501

    def __init__(self, flags: QtCore.Qt.WindowType | None = None):
        super().__init__()

        self.setObjectName('splashScreenWindow')
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.updated.connect(self.on_updated)

        # flags
        flags = flags or self.DAFAULT_FLAGS
        self.setWindowFlags(flags)

        # style
        filepath = pave(os.path.join('.', 'static', 'splash-screen-window.css'))
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
        self.setFixedSize(QtCore.QSize(680, 400))

    def on_updated(
        self,
        state: SplashScreenState,
    ) -> None:

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


class ContentWidget(QtWidgets.QFrame):

    DEFAULT_PROGRESS = 0
    DEFAULT_INFO = '<strong>LOADING</strong>...'
    DEFAULT_MESSAGE = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('contentWidget')

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(LabelWidget(
            objectName='appNameLabel',
            text='<strong>{name}</strong>'.format(
                name=os.environ['APPLICATION_NAME'].upper(),
            ),
            parent=self,
        ))
        layout.addWidget(LabelWidget(
            objectName='appVersionLabel',
            text='<strong>VERSION</strong> {version}'.format(
                version=os.environ['APPLICATION_VERSION'],
            ),
            parent=self,
        ))
        layout.addSpacing(50)
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


class LabelWidget(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


class ProgressBarWidget(QtWidgets.QProgressBar):

    def __init__(self, value: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setValue(value)
