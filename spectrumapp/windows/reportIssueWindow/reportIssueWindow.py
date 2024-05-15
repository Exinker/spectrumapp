import os
from datetime import datetime

from PySide6 import QtWidgets

from spectrumapp.config import File
from spectrumapp.utils.modifier import attempt, wait
from spectrumapp.windows.window import BaseWindow

from .archiver import AbstractArchiver, ZipArchiver
from .delivery import AbstractDelivery, TelegramDelivery
from .utils import walk


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
        super().__init__(*args, text='Dump locally', objectName='dumpLocallyPushButton', **kwargs)

        self.setFixedWidth(120)
        self.clicked.connect(self._onClicked)

        self.archiver = archiver

    @wait
    @attempt()
    def _onClicked(self, *args, **kwargs):
        archiver = self.archiver
        parent = self.parent()

        #
        timestamp = parent.findChild(QtWidgets.QLabel, 'timestampLabel').text()

        archiver.dump(
            files=walk(file=File.load()),
            timestamp=timestamp,
        )


class DumpRemotePushButton(QtWidgets.QPushButton):

    def __init__(self, *args, archiver: AbstractArchiver, delivery: AbstractDelivery, **kwargs):
        super().__init__(*args, text='Dump remote', objectName='dumpRemotePushButton', **kwargs)

        self.setFixedWidth(120)
        self.clicked.connect(self._onClicked)

        self.archiver = archiver
        self.delivery = delivery

    @wait
    @attempt()
    def _onClicked(self, *args, **kwargs):
        archiver = self.archiver
        delivery = self.delivery
        parent = self.parent()

        #
        timestamp = parent.findChild(QtWidgets.QLabel, 'timestampLabel').text()

        archiver.dump(
            files=walk(file=File.load()),
            timestamp=timestamp,
        )
        delivery.send(
            filepath=archiver.get_filepath(timestamp),
            description=parent.findChild(QtWidgets.QPlainTextEdit, 'descriptionPlainText').toPlainText(),
            timestamp=timestamp,
        )


class CancelPushButton(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Cancel', objectName='cancelPushButton', **kwargs)

        self.setFixedWidth(120)
        self.clicked.connect(self._onClicked)

    @wait
    @attempt()
    def _onClicked(self, *args, **kwargs):
        parent = self.parent()
        parent.close()


class ReportIssueWindow(BaseWindow):

    def __init__(self, *args, archiver: AbstractArchiver | None = None, delivery: AbstractDelivery | None = None, **kwargs):
        super().__init__(*args, **kwargs)

        archiver = archiver or ZipArchiver()
        delivery = delivery or TelegramDelivery(
            token=os.environ['API_TOKEN'],
            chat_id=os.environ['CHAT_ID'],
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
            datetime.now().strftime('%Y.%m.%d %H:%M'),
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
            parent=self,
        ))
        layout.addStretch()
        layout.addWidget(CancelPushButton(
            parent=self,
        ))
        self.layout.addLayout(layout)

        # geometry
        self.setFixedSize(480, self.sizeHint().height())

        #
        self.show()

    def closeEvent(self, event):
        super().closeEvent(event=event)
