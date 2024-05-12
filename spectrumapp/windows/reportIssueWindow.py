import os
import time
from datetime import datetime
from typing import Iterator

import telepot
from PySide6 import QtWidgets
from zipfile import ZipFile

from spectrumapp.file import File
from spectrumapp.types import FilePath
from spectrumapp.utils.modifier import attempt, wait
from spectrumapp.windows.window import BaseWindow


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


class PushButton(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedWidth(120)
        self.clicked.connect(self._onClicked)

    @wait
    @attempt()
    def _onClicked(self, *args, **kwargs):
        app = QtWidgets.QApplication.instance()
        parent = self.parent()
        button = self.sender()

        #
        button_name = button.objectName()

        if button_name == 'dumpLocallyPushButton':
            archive_dump(
                files=walk(file=app.file),
                timestamp=parent.findChild(QtWidgets.QLabel, 'timestampLabel').text(),
            )

        if button_name == 'dumpRemotePushButton':
            archive_dump(
                files=walk(file=app.file),
                timestamp=parent.findChild(QtWidgets.QLabel, 'timestampLabel').text(),
            )
            send_dump(
                timestamp=parent.findChild(QtWidgets.QLabel, 'timestampLabel').text(),
                description=parent.findChild(QtWidgets.QPlainTextEdit, 'descriptionPlainText').toPlainText(),
            )

        if button_name == 'cancelPushButton':
            parent.close()


class ReportIssueWindow(BaseWindow):

    def __init__(self, *args, **kwargs):
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
        layout.addWidget(PushButton(
            text='Dump locally',
            objectName='dumpLocallyPushButton',
            parent=self,
        ))
        layout.addWidget(PushButton(
            text='Dump remote',
            objectName='dumpRemotePushButton',
            parent=self,
        ))
        layout.addStretch()
        layout.addWidget(PushButton(
            text='Cancel',
            objectName='cancelPushButton',
            parent=self,
        ))
        self.layout.addLayout(layout)

        # geometry
        self.setFixedSize(480, self.sizeHint().height())

        #
        self.show()

    def closeEvent(self, event):
        super().closeEvent(event=event)


# --------        utils        --------
def archive_dump(files: Iterator[FilePath], timestamp: str, timeout: float = .5) -> None:
    """Archive dump and support files to .zip file."""
    filedir = get_archive_filedir()
    filename = get_archive_filename(timestamp)

    filepath = os.path.join(filedir, filename)
    with ZipFile(filepath, 'w') as zip:
        for file in files:
            zip.write(file)

    #
    time.sleep(timeout)  # add timeout for realistic


def send_dump(timestamp: str, description: str) -> None:
    token = os.environ['API_TOKEN']
    chat_id = os.environ['CHAT_ID']

    bot = telepot.Bot(token)

    caption = '\n'.join([
        os.environ['APPLICATION_NAME'],
        os.environ['APPLICATION_VERSION'],
        timestamp,
        description,
    ])

    filedir = get_archive_filedir()
    filename = get_archive_filename(timestamp)
    filepath = os.path.join(filedir, filename)
    with open(filepath, 'rb') as file:
        bot.sendDocument(
            chat_id=chat_id,
            document=file,
            caption=caption,
        )


def walk(file: File) -> Iterator[FilePath]:
    """Walk iterable along folders."""

    # app's folder
    filedir = '.'

    for filename in ('app.log', 'config.json', 'settings.ini'):
        filepath = os.path.join(filedir, filename)

        if os.path.exists(filepath):
            yield filepath

    # data's folder
    for filedir, _, filenames in os.walk(file.filedir):
        for filename in filenames:
            filepath = os.path.join(filedir, filename)

            yield filepath


def get_archive_filedir() -> str:

    filedir = os.path.join('.', 'dumps')
    if not os.path.isdir(filedir):
        os.mkdir(filedir)

    return filedir


def get_archive_filename(timestamp: str) -> str:
    filename = '{name}.zip'.format(
        name=timestamp.replace('.', '').replace(':', '').replace(' ', '_'),
    )

    return filename
