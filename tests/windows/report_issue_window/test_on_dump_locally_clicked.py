import os
import tempfile
from pathlib import Path

from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.report_issue_window import ReportIssueWindow
from spectrumapp.windows.report_issue_window.archive_managers.zip_archive_manager import ZipArchiveManager


def test_on_click_dump_locally(
    tmpdir: tempfile.TemporaryDirectory,
    timestamp: float,
    report_issue_window: ReportIssueWindow,
    archive_manager: ZipArchiveManager,
    qtbot: QtBot,
):
    button = report_issue_window.findChild(QtWidgets.QPushButton, 'dumpLocallyPushButton')
    button.click()

    assert archive_manager.archive_name == '{}'.format(int(timestamp))
    assert archive_manager.archive_dir == Path(tmpdir.name)
    assert os.path.exists(archive_manager.archive_path)
