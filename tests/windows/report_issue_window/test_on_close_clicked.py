import os

from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.report_issue_window import ReportIssueWindow
from spectrumapp.windows.report_issue_window.archiver import ZipArchiver


def test_on_close_clicked(
    timestamp: str,
    report_issue_window: ReportIssueWindow,
    archiver: ZipArchiver,
    qtbot: QtBot,
):
    button = report_issue_window.findChild(QtWidgets.QPushButton, 'cancelPushButton')
    button.click()

    assert archiver.filename == timestamp.replace('.', '').replace(':', '')
    assert not os.path.exists(archiver.filepath)
