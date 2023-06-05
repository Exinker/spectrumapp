
import os
from typing import Any, Callable, Generator, Iterable

from PySide6 import QtWidgets, QtCore, QtGui

from spectrumapp.core.utils import pave
from spectrumapp.utils import find_window


APPLICATION_NAME = os.environ['APPLICATION_NAME']
APPLICATION_VERSION = os.environ['APPLICATION_VERSION']


def splashscreen(progress: int | None = None, info: str | None = None, message: str | None = None) -> Callable:
    """Splash screen decorator for PyQt5 applications"""
    window_name = 'splashScreenWindow'

    def decorator(func):
        def wrapper(*args, **kwargs):

            # window
            window = find_window(window_name)
            if window is None:
                window = SplashScreenWindow()

            window.show()
            window.set(
                progress=progress,
                info=info,
                message=message,
            )

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
    window = find_window(window_name)
    if window is None:
        window = SplashScreenWindow()

    window.show()
    try:
        for i, item in enumerate(items):
            window.set(
                progress='' if n_items is None else int((i + 1)*100/n_items),
                info=info,
                message='' if n_items is None else f'<strong>{item}</strong> ({i + 1}/{n_items})',
            )

            yield item
    finally:
        window.close()


class SplashScreenWindow(QtWidgets.QWidget):

    def __init__(self, flags=(QtCore.Qt.WindowType.Window, QtCore.Qt.WindowType.WindowStaysOnTopHint, )):
        # super().__init__(flags=flags)
        super().__init__()

        for flag in flags:
            self.setWindowFlag(flag, True)

        self.setObjectName('splashScreenWindow')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # style
        filepath = pave(os.path.join('.', 'static', 'splash-screen.css'))
        style = open(filepath, 'r').read()
        self.setStyleSheet(style)

        #
        filepath = pave('icon.ico')
        icon = QtGui.QIcon(filepath)
        self.setWindowIcon(icon)

        # size
        self.setFixedSize(
            QtCore.QSize(680, 400)
        )

        # frame
        layout = QtWidgets.QVBoxLayout(self)

        frame = QtWidgets.QFrame()
        layout.addWidget(frame)

        # layout
        self.layout = QtWidgets.QVBoxLayout(frame)

        self.layout.addStretch()

        appNameLabel = QtWidgets.QLabel(parent=self, text=f'<strong>{APPLICATION_NAME.upper()}</strong>')
        appNameLabel.setObjectName('appNameLabel')
        appNameLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout.addWidget(appNameLabel)

        appDescriptionLabel = QtWidgets.QLabel(parent=self, text=f'<strong>VERSION</strong> {APPLICATION_VERSION}')
        appDescriptionLabel.setObjectName('appDescriptionLabel')
        appDescriptionLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout.addWidget(appDescriptionLabel)

        self.layout.addSpacing(50)

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setValue(0)
        self.layout.addWidget(self.progressBar)

        self.infoLabel = QtWidgets.QLabel(parent=self, text='<strong>LOADING</strong>...')
        self.infoLabel.setObjectName('infoLabel')
        self.infoLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.infoLabel)

        self.messageLabel = QtWidgets.QLabel(parent=self, text='')
        self.messageLabel.setObjectName('messageLabel')
        self.messageLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.messageLabel)

        self.layout.addSpacing(50)

    def set(self, progress: int | None = None, info: str | None = None, message: str | None = None):

        if progress:
            self.progressBar.setValue(progress)
        if info:
            self.infoLabel.setText(info)
        if message:
            self.messageLabel.setText(message)

        #
        app = QtWidgets.QApplication.instance()
        app.processEvents()


if __name__ == '__main__':
    from time import sleep


    app = QtWidgets.QApplication()

    window = SplashScreenWindow()
    window.show()
    for i in range(1, 100+1):
        window.set(
            progress=i,
            info='<strong>PLEASE, WAIT!</strong>',
            message='Loading {value} {label} is complited!'.format(
                value=i,
                label='percent' if i == 1 else 'percents',
            )
        )
        sleep(.1)

    app.quit()
