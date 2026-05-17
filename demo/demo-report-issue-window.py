import os
import sys
from datetime import datetime
from pathlib import Path

from PySide6 import QtWidgets

from spectrumapp.application import BaseApplication
from spectrumapp.configs import TELEGRAM_CONFIG
from spectrumapp.loggers import log
from spectrumapp.windows.report_issue_window import ReportIssueWindow
from spectrumapp.windows.report_issue_window.archive_managers import ZipArchiveManager
from spectrumapp.windows.report_issue_window.archive_managers.utils import explore
from spectrumapp.windows.report_issue_window.report_managers import TelegramReportManager
from utils import (
    setdefault_environ,
    setdefault_logger,
)


class Application(BaseApplication):

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
    timestamp = datetime.timestamp(datetime.now())

    window = ReportIssueWindow(
        application_name=os.environ['APPLICATION_NAME'],
        application_version=os.environ['APPLICATION_VERSION'],
        timestamp=timestamp,
        archive_manager=ZipArchiveManager(
            files=explore(
                [
                    Path.cwd() / '.env',
                    Path.cwd() / '.log',
                    Path.cwd() / 'config.json',
                    Path.cwd() / 'settings.ini',
                ],
                prefix=Path.cwd(),
            ),
            archive_name='{}'.format(int(timestamp)),
        ),
        report_manager=TelegramReportManager.create(
            application_name=os.environ['APPLICATION_NAME'],
            application_version=os.environ['APPLICATION_VERSION'],
            timestamp=timestamp,
            token=TELEGRAM_CONFIG.token.get_secret_value(),
            chat_id=TELEGRAM_CONFIG.chat_id,
        ),
    )
    window.show()

    sys.exit(app.exec())
