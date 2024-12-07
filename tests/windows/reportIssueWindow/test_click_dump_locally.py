import os

from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.reportIssueWindow import ReportIssueWindow
from spectrumapp.windows.reportIssueWindow.archiver import (
    ZipArchiver,
)


def test_on_click_dump_locally(
    timestamp: str,
    window: ReportIssueWindow,
    archiver: ZipArchiver,
    qtbot: QtBot,
):
    button = window.findChild(QtWidgets.QPushButton, 'dumpLocallyPushButton')
    button.click()

    assert archiver.filename == timestamp.replace('.', '').replace(':', '')
    assert os.path.exists(archiver.filepath)
