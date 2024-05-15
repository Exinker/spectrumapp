import os
import pytest

from PySide6 import QtWidgets

from spectrumapp import ORGANIZATION_NAME, VERSION
from spectrumapp.windows.reportIssueWindow import ReportIssueWindow, ZipArchiver


def setup_environ() -> None:
    os.environ['APPLICATION_NAME'] = 'Tests'
    os.environ['APPLICATION_VERSION'] = VERSION
    os.environ['ORGANIZATION_NAME'] = ORGANIZATION_NAME

    os.environ['DEBUG'] = str(True)


@pytest.fixture(autouse=True)
def cleanup_files(window: QtWidgets.QWidget, archiver: ZipArchiver) -> None:
    yield

    timestamp = window.findChild(QtWidgets.QLabel, 'timestampLabel').text()

    filepath = archiver.get_filepath(timestamp)
    if os.path.exists(filepath):
        os.remove(filepath)


@pytest.fixture
def window(archiver: ZipArchiver) -> QtWidgets.QWidget:
    setup_environ()

    return ReportIssueWindow(
        archiver=archiver,
    )


@pytest.fixture
def archiver() -> ZipArchiver:
    return ZipArchiver()


def test_on_click_dump_locally(qtbot, window: QtWidgets.QWidget, archiver: ZipArchiver):

    button = window.findChild(QtWidgets.QPushButton, 'dumpLocallyPushButton')
    button.click()

    timestamp = window.findChild(QtWidgets.QLabel, 'timestampLabel').text()

    filepath = archiver.get_filepath(timestamp)
    assert os.path.exists(filepath)
