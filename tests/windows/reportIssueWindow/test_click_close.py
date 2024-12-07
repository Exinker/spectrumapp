import os

from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.reportIssueWindow import ReportIssueWindow
from spectrumapp.windows.reportIssueWindow.archiver import (
    ZipArchiver,
)


def test_on_click_close(
    timestamp: str,
    window: ReportIssueWindow,
    archiver: ZipArchiver,
    qtbot: QtBot,
):
    button = window.findChild(QtWidgets.QPushButton, 'cancelPushButton')
    button.click()

    assert archiver.filename == timestamp.replace('.', '').replace(':', '')
    assert not os.path.exists(archiver.filepath)
