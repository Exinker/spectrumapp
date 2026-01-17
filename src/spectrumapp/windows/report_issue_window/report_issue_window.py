import logging
import os
from datetime import datetime
from pathlib import Path

from PySide6 import QtWidgets

from spectrumapp.windows.exception_window import attempt
from spectrumapp.windows.modifiers import wait
from spectrumapp.windows.report_issue_window.archive_managers.base_archive_manager import ArchiveManagerABC
from spectrumapp.windows.report_issue_window.report_managers.base_report_manager import ReportManagerABS
from spectrumapp.windows.window import BaseWindow


LOGGER = logging.getLogger('spectrumapp')


class DescriptionPlainText(QtWidgets.QPlainTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('descriptionPlainText')
        self.setPlaceholderText('Describe the issue in details')
        self.setFixedHeight(300)


class AttacheDumpCheckBox(QtWidgets.QCheckBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('attacheDumpCheckBox')
        self.setEnabled(False)
        self.setChecked(2)


class DumpLocallyPushButton(QtWidgets.QPushButton):

    def __init__(self, *args, archive_manager: ArchiveManagerABC, **kwargs):
        super().__init__(
            *args,
            text='Dump locally',
            objectName='dumpLocallyPushButton',
            **kwargs,
        )

        self._archive_manager = archive_manager

        self.setFixedWidth(120)
        self.clicked.connect(self._on_clicked)

    @wait
    @attempt()
    def _on_clicked(self, *args, **kwargs):
        LOGGER.debug('%s clicked.', self.__class__.__name__)

        self._archive_manager.dump()

        parent = self.parent()
        parent.close()


class DumpRemotePushButton(QtWidgets.QPushButton):

    def __init__(
        self,
        *args,
        archive_manager: ArchiveManagerABC,
        report_manager: ReportManagerABS,
        is_enabled: bool = False,
        **kwargs,
    ):
        super().__init__(*args, text='Dump remote', objectName='dumpRemotePushButton', **kwargs)

        self._archive_manager = archive_manager
        self._report_manager = report_manager

        self.setFixedWidth(120)
        self.setEnabled(is_enabled)
        self.clicked.connect(self._on_clicked)

    @wait
    @attempt()
    def _on_clicked(self, *args, **kwargs):
        LOGGER.debug('%s clicked.', self.__class__.__name__)

        self._archive_manager.dump()
        self._report_manager.send(
            archive_path=self._archive_manager.archive_path,
            description=self.parent().findChild(QtWidgets.QPlainTextEdit, 'descriptionPlainText').toPlainText(),
        )

        parent = self.parent()
        parent.close()


class CancelPushButton(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Cancel', objectName='cancelPushButton', **kwargs)

        self.setFixedWidth(120)
        self.clicked.connect(self._on_clicked)

    @wait
    @attempt()
    def _on_clicked(self, *args, **kwargs):
        LOGGER.debug('%s clicked.', self.__class__.__name__)

        parent = self.parent()
        parent.close()


class ReportIssueWindow(BaseWindow):

    def __init__(
        self,
        *args,
        timestamp: float,
        archive_manager: ArchiveManagerABC,
        report_manager: ReportManagerABS,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # title
        title = 'Report Issue Window'
        self.setWindowTitle(title)

        # layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        # content
        layout = QtWidgets.QFormLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addRow('Application:', QtWidgets.QLabel(
            os.environ['APPLICATION_NAME'],
            objectName='appNameLabel',
            parent=self,
        ))
        layout.addRow('Version:', QtWidgets.QLabel(
            os.environ['APPLICATION_VERSION'],
            objectName='appVersionLabel',
            parent=self,
        ))
        layout.addRow('Datetime:', QtWidgets.QLabel(
            datetime.fromtimestamp(timestamp).strftime('%Y.%m.%d %H:%M'),
            objectName='datetimeLabel',
            parent=self,
        ))
        layout.addRow('Description:', DescriptionPlainText(
            '',
            parent=self,
        ))
        layout.addRow('', AttacheDumpCheckBox(
            text='Attache dump',
            parent=self,
        ))
        self.layout.addLayout(layout)

        # control
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(DumpLocallyPushButton(
            archive_manager=archive_manager,
            parent=self,
        ))
        layout.addWidget(DumpRemotePushButton(
            archive_manager=archive_manager,
            report_manager=report_manager,
            is_enabled=all([
                os.environ.get('TELEGRAM_TOKEN', ''),
                os.environ.get('TELEGRAM_CHAT_ID', ''),
            ]),
            parent=self,
        ))
        layout.addStretch()
        layout.addWidget(CancelPushButton(
            parent=self,
        ))
        self.layout.addLayout(layout)

        # geometry
        self.setFixedSize(480, self.sizeHint().height())

        # show
        self.show()

    def closeEvent(self, event):  # noqa: N802
        super().closeEvent(event=event)


if __name__ == '__main__':
    import sys

    import spectrumapp
    from spectrumapp.windows.report_issue_window.archive_managers import ZipArchiveManager
    from spectrumapp.windows.report_issue_window.archive_managers.utils import explore
    from spectrumapp.windows.report_issue_window.report_managers import TelegramReportManager

    os.environ['APPLICATION_NAME'] = 'Demo'
    os.environ['APPLICATION_VERSION'] = spectrumapp.__version__
    os.environ['ORGANIZATION_NAME'] = spectrumapp.__organization__

    app = QtWidgets.QApplication()

    timestamp = datetime.timestamp(datetime.now())
    window = ReportIssueWindow(
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
            timestamp=timestamp,
            token=os.environ.get('TELEGRAM_TOKEN', ''),
            chat_id=os.environ.get('TELEGRAM_CHAT_ID', ''),
        ),
    )
    window.show()

    sys.exit(app.exec())
