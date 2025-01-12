import logging
import os
from datetime import datetime

from PySide6 import QtWidgets

from spectrumapp.config import BaseConfig
from spectrumapp.windows.exception_window import attempt
from spectrumapp.windows.modifiers import wait
from spectrumapp.windows.report_issue_window.archiver import AbstractArchiver, ZipArchiver
from spectrumapp.windows.report_issue_window.delivery import AbstractDelivery, TelegramDelivery
from spectrumapp.windows.report_issue_window.utils import explore
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

    def __init__(self, *args, archiver: AbstractArchiver, **kwargs):
        super().__init__(
            *args,
            text='Dump locally',
            objectName='dumpLocallyPushButton',
            **kwargs,
        )

        self.archiver = archiver

        self.setFixedWidth(120)
        self.clicked.connect(self._on_clicked)

    @wait
    @attempt()
    def _on_clicked(self, *args, **kwargs):
        LOGGER.debug('%s clicked.', self.__class__.__name__)

        file = BaseConfig.load()

        self.archiver.dump(
            files=explore(file),
            directory=file.directory,
        )


class DumpRemotePushButton(QtWidgets.QPushButton):

    def __init__(
        self,
        *args,
        archiver: AbstractArchiver,
        delivery: AbstractDelivery,
        is_enabled: bool = False,
        **kwargs,
    ):
        super().__init__(*args, text='Dump remote', objectName='dumpRemotePushButton', **kwargs)

        self.archiver = archiver
        self.delivery = delivery

        self.setFixedWidth(120)
        self.setEnabled(is_enabled)
        self.clicked.connect(self._on_clicked)

    @wait
    @attempt()
    def _on_clicked(self, *args, **kwargs):
        LOGGER.debug('%s clicked.', self.__class__.__name__)

        file = BaseConfig.load()

        self.archiver.dump(
            files=explore(file),
            directory=file.directory,
        )
        self.delivery.send(
            filepath=self.archiver.filepath,
            description=self.parent().findChild(QtWidgets.QPlainTextEdit, 'descriptionPlainText').toPlainText(),
        )


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
        archiver: AbstractArchiver | None = None,
        delivery: AbstractDelivery | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        timestamp = datetime.now().strftime('%Y.%m.%d %H:%M')
        archiver = archiver or ZipArchiver(
            filename=timestamp,
        )
        delivery = delivery or TelegramDelivery(
            timestamp=timestamp,
            token=os.environ.get('TELEGRAM_TOKEN', ''),
            chat_id=os.environ.get('TELEGRAM_CHAT_ID', ''),
        )

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
        layout.addRow('Timestamp:', QtWidgets.QLabel(
            timestamp,
            objectName='timestampLabel',
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
            archiver=archiver,
            parent=self,
        ))
        layout.addWidget(DumpRemotePushButton(
            archiver=archiver,
            delivery=delivery,
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
