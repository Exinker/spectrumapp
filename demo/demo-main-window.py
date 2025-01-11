import sys

from PySide6 import QtWidgets

from spectrumapp.application import BaseApplication
from spectrumapp.loggers import log
from spectrumapp.windows.main_window import BaseMainWindow
from spectrumapp.windows.splash_screen_window import splashscreen
from utils import (
    setdefault_environ,
    setdefault_logger,
    setdefault_setting,
)


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

        # show
        self.show()

    def on_directory_opened(self, *args, **kwargs):  # noqa: N802
        super().on_directory_opened(*args, **kwargs)

    @splashscreen(progress=50, info='<strong>RESET</strong> user interface...', delay=1)
    def on_resetted(self, *args, **kwargs):  # noqa: N802
        super().on_resetted(*args, **kwargs)

    @splashscreen(progress=100, info='<strong>REFRESH</strong> user interface...', delay=1)
    def on_refreshed(self, *args, **kwargs):  # noqa: N802
        super().on_refreshed(*args, **kwargs)


class Application(BaseApplication):

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


if __name__ == '__main__':
    setdefault_environ()
    setdefault_setting()
    setdefault_logger()

    app = Application(sys.argv)
    app.run()

    sys.exit(app.exec())
