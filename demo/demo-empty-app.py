import os
import sys

from PySide6 import QtWidgets

import spectrumapp
from spectrumapp.application import AbstractApplication
from spectrumapp.loggers import log, setdefault_logger
from spectrumapp.settings import setdefault_setting
from spectrumapp.windows.mainWindow import BaseMainWindow
from spectrumapp.windows.splashScreenWindow import splashscreen


class EmptyWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedHeight(200)


class EmptyFrame(QtWidgets.QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedWidth(320)
        self.setFixedHeight(480)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)


class CentralWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        layout.addWidget(
            EmptyFrame(parent=self),
        )

    def _onResetTriggered(self, refresh: bool = True):  # noqa: N802
        """Reset the widget all sub widget."""
        if refresh:
            self._onRefreshTriggered()

    def _onRefreshTriggered(self):  # noqa: N802
        """Refresh the widget and all sub widgets."""


class Window(BaseMainWindow):

    @splashscreen(progress=100, info='<strong>LOADING</strong> user interface...', delay=1)
    def __init__(self, *args, show: bool = False, **kwargs):
        super().__init__(*args, show=show, **kwargs)

        # widget
        widget = CentralWidget(parent=self)
        self.setCentralWidget(widget)

        #
        self.show()

    def _onOpenTriggered(self, *args, **kwargs):  # noqa: N802
        super()._onOpenTriggered(*args, **kwargs)

    @splashscreen(progress=50, info='<strong>RESET</strong> user interface...', delay=1)
    def _onResetTriggered(self, *args, **kwargs):  # noqa: N802
        super()._onResetTriggered(*args, **kwargs)

    @splashscreen(progress=100, info='<strong>REFRESH</strong> user interface...', delay=1)
    def _onRefreshTriggered(self, *args, **kwargs):  # noqa: N802
        super()._onRefreshTriggered(*args, **kwargs)


class Application(AbstractApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        self._window = None

    @property
    def window(self) -> QtWidgets.QWidget:
        return self._window

    @log(message='app: run')
    def run(self):
        """Run the application."""

        self._window = Window()

    @log(message='app: refresh')
    def refresh(self):
        """Refresh all windows and widgets of an application."""

        self.window._onRefreshTriggered()

    @log(message='app: reset')
    def reset(self, refresh: bool = True):
        """Update setting, config and refresh the app."""

        # refresh (windows and widgets)
        if refresh:
            self.window._onRefreshTriggered()


def setdefault_environ(debug: bool = False) -> None:
    os.environ['APPLICATION_NAME'] = 'Demo'
    os.environ['APPLICATION_VERSION'] = spectrumapp.__version__
    os.environ['ORGANIZATION_NAME'] = spectrumapp.__organization__

    os.environ['DEBUG'] = str(debug)


if __name__ == '__main__':

    # setup env
    setdefault_environ()

    # setup settings
    setdefault_setting()

    # setup loggers
    setdefault_logger()

    # app
    app = Application(sys.argv)
    app.run()

    # exit
    sys.exit(app.exec())
