import os
import sys

from PySide6 import QtWidgets

import spectrumapp
from spectrumapp.application import AbstractApplication
from spectrumapp.loggers import log, setdefault_logger
from spectrumapp.windows.reportIssueWindow import ReportIssueWindow


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

    # setup loggers
    setdefault_logger()

    # app
    app = Application(sys.argv)

    window = ReportIssueWindow()
    window.show()

    sys.exit(app.exec())
