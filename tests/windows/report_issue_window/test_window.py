import os

from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.report_issue_window import ReportIssueWindow
from spectrumapp.windows.report_issue_window.report_issue_window import (
    AttacheDumpCheckBox,
    DescriptionPlainText,
)


def test_window(
    description: str,
    timestamp: str,
    report_issue_window: ReportIssueWindow,
    qtbot: QtBot,
):

    assert report_issue_window.windowTitle() == 'Report Issue Window'
    assert report_issue_window.findChild(QtWidgets.QLabel, 'appNameLabel').text() == os.environ['APPLICATION_NAME']
    assert report_issue_window.findChild(QtWidgets.QLabel, 'appVersionLabel').text() == os.environ['APPLICATION_VERSION']  # noqa: E501
    assert report_issue_window.findChild(QtWidgets.QLabel, 'timestampLabel').text() == timestamp
    assert report_issue_window.findChild(DescriptionPlainText, 'descriptionPlainText').toPlainText() == description
    assert report_issue_window.findChild(AttacheDumpCheckBox, 'attacheDumpCheckBox').isChecked() is True
