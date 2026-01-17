import os
from datetime import datetime

from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.report_issue_window import ReportIssueWindow
from spectrumapp.windows.report_issue_window.report_issue_window import (
    AttacheDumpCheckBox,
    DescriptionPlainText,
)


def test_report_issue_window(
    application_name: str,
    application_version: str,
    description: str,
    timestamp: float,
    report_issue_window: ReportIssueWindow,
    qtbot: QtBot,
):

    assert report_issue_window.windowTitle() == 'Report Issue Window'
    assert report_issue_window.findChild(QtWidgets.QLabel, 'appNameLabel').text() == application_name
    assert report_issue_window.findChild(QtWidgets.QLabel, 'appVersionLabel').text() == application_version  # noqa: E501
    assert report_issue_window.findChild(QtWidgets.QLabel, 'datetimeLabel').text() == datetime.fromtimestamp(timestamp).strftime('%Y.%m.%d %H:%M')  # noqa: E501
    assert report_issue_window.findChild(DescriptionPlainText, 'descriptionPlainText').toPlainText() == description
    assert report_issue_window.findChild(AttacheDumpCheckBox, 'attacheDumpCheckBox').isChecked() is True
