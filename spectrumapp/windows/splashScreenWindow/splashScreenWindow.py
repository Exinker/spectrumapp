import os
import time
from typing import Any, Callable, Generator, Iterable, Sequence

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.paths import pave
from spectrumapp.utils import find_window


# --------        windows        --------
class SplashScreenWindow(QtWidgets.QWidget):
    """Splash screen decorator for Qt applications and long time processes."""

    def __init__(self, flags: Sequence[QtCore.Qt.WindowType] | None = None):
        super().__init__()

        self.setObjectName('splashScreenWindow')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # flags
        flags = flags or (QtCore.Qt.WindowType.Window, QtCore.Qt.WindowType.WindowStaysOnTopHint)
        for flag in flags:
            self.setWindowFlag(flag, True)

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


# --------        decorators        --------
def splashscreen(progress: int | None = None, info: str | None = None, message: str | None = None, delay: float = 0) -> Callable:
    """Splash screen decorator for Qt applications."""
    window_name = 'splashScreenWindow'

    def decorator(func):
        def wrapper(*args, **kwargs):

            # window
            window = find_window(window_name) or SplashScreenWindow()
            window.show()
            window.update(
                progress=progress,
                info=info,
                message=message,
            )

            # delay
            time.sleep(delay)

            #
            return func(*args, **kwargs)

        return wrapper
    return decorator


def iterate(items: Iterable[Any], info: str | None = '') -> Generator:
    """Iterate decorator with a progress window."""
    window_name = 'splashScreenWindow'

    # n_items
    try:
        n_items = len(items)
    except (TypeError, AttributeError):
        n_items = None

    # window
    window = find_window(window_name) or SplashScreenWindow()
    window.show()

    try:
        for i, item in enumerate(items):
            window.update(
                progress='' if n_items is None else int((i + 1)*100/n_items),
                info=info,
                message='' if n_items is None else f'<strong>{item}</strong> ({i + 1}/{n_items})',
            )

            yield item
    finally:
        window.close()
