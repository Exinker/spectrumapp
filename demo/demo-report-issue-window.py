import sys

from PySide6 import QtWidgets

from spectrumapp.application import AbstractApplication
from spectrumapp.loggers import log
from spectrumapp.windows.report_issue_window import ReportIssueWindow
from utils import (
    setdefault_environ,
    setdefault_logger,
)


class Application(AbstractApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._window = None

    @property
    def window(self) -> QtWidgets.QWidget:
        return self._window

    @log(message='app: run')
    def run(self):
        """Run the application."""

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
    setdefault_logger()

    app = Application(sys.argv)

    window = ReportIssueWindow()
    window.show()

    sys.exit(app.exec())
