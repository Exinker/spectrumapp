import os

from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.reportIssueWindow import ReportIssueWindow
from spectrumapp.windows.reportIssueWindow.reportIssueWindow import (
    AttacheDumpCheckBox,
    DescriptionPlainText,
)


def test_window(
    description: str,
    timestamp: str,
    window: ReportIssueWindow,
    qtbot: QtBot,
):

    assert window.windowTitle() == 'Report Issue Window'
    assert window.findChild(QtWidgets.QLabel, 'appNameLabel').text() == os.environ['APPLICATION_NAME']
    assert window.findChild(QtWidgets.QLabel, 'appVersionLabel').text() == os.environ['APPLICATION_VERSION']
    assert window.findChild(QtWidgets.QLabel, 'timestampLabel').text() == timestamp
    assert window.findChild(DescriptionPlainText, 'descriptionPlainText').toPlainText() == description
    assert window.findChild(AttacheDumpCheckBox, 'attacheDumpCheckBox').isChecked() is True
