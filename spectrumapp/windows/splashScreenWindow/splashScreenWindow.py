import os

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.paths import pave


class SplashScreenWindow(QtWidgets.QWidget):
    """Splash screen decorator for Qt applications and long time processes."""

    def __init__(self, flags: QtCore.Qt.WindowType | None = None):
        super().__init__()

        self.setObjectName('splashScreenWindow')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # flags
        flags = flags or QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.WindowStaysOnTopHint
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

    def update(self, progress: int | None = None, info: str | None = None, message: str | None = None):

        if progress:
            widget = self.findChild(QtWidgets.QProgressBar, 'progressBar')
            widget.setValue(progress)

        if info:
            widget = self.findChild(QtWidgets.QLabel, 'infoLabel')
            widget.setText(info)

        if message:
            widget = self.findChild(QtWidgets.QLabel, 'messageLabel')
            widget.setText(message)

        #
        app = QtWidgets.QApplication.instance()
        app.processEvents()


class ContentWidget(QtWidgets.QFrame):

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
            parent=self,
        ))
        layout.addWidget(LabelWidget(
            objectName='infoLabel',
            text='<strong>LOADING</strong>...',
            parent=self,
        ))
        layout.addWidget(LabelWidget(
            objectName='messageLabel',
            text='',
            parent=self,
        ))
        layout.addSpacing(50)


class LabelWidget(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


class ProgressBarWidget(QtWidgets.QProgressBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setValue(0)
