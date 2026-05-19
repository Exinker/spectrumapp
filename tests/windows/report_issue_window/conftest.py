import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Callable

import pytest
from PySide6 import QtCore, QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.configs import BaseConfig
from spectrumapp.windows.report_issue_window import ReportIssueWindow
from spectrumapp.windows.report_issue_window.archive_managers import ZipArchiveManager
from spectrumapp.windows.report_issue_window.archive_managers.base_archive_manager import ArchiveManagerABC
from spectrumapp.windows.report_issue_window.archive_managers.utils import explore
from spectrumapp.windows.report_issue_window.report_issue_window import DescriptionPlainText
from spectrumapp.windows.report_issue_window.report_managers import TelegramReportManager
from spectrumapp.windows.report_issue_window.report_managers.base_report_manager import ReportManagerABS


@pytest.fixture
def tmpdir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory()


@pytest.fixture
def timestamp() -> float:
    return datetime.timestamp(datetime.now())


@pytest.fixture(params=['test'])
def description(request) -> str:
    return request.param


@pytest.fixture
def token(
    faker,
) -> str:
    return faker.sha256()


@pytest.fixture
def chat_id(
    faker,
) -> str:
    return faker.numerify('########')


@pytest.fixture
def archive_manager(
    tmpdir: tempfile.TemporaryDirectory,
    timestamp: float,
) -> ZipArchiveManager:
    return ZipArchiveManager(
        files=explore([], prefix=None),
        archive_name='{}'.format(int(timestamp)),
        archive_dir=Path(tmpdir.name),
    )


@pytest.fixture
def report_manager(
    application_name: str,
    application_version: str,
    timestamp: float,
) -> TelegramReportManager:
    return TelegramReportManager.create(
        application_name=application_name,
        application_version=application_version,
        timestamp=timestamp,
        token='',
        chat_id='',
    )


@pytest.fixture
def create_report_issue_window(
    application_name: str,
    application_version: str,
    timestamp: float,
    archive_manager: ArchiveManagerABC,
    report_manager: ReportManagerABS,
    qtbot: QtBot,
) -> Callable[[], ReportIssueWindow]:

    def inner() -> ReportIssueWindow:
        report_issue_window = ReportIssueWindow(
            application_name=application_name,
            application_version=application_version,
            timestamp=timestamp,
            archive_manager=archive_manager,
            report_manager=report_manager,
        )
        report_issue_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, False)
        qtbot.addWidget(report_issue_window)

        return report_issue_window

    return inner


@pytest.fixture
def create_dump_remote_button(
    create_report_issue_window: Callable[[], ReportIssueWindow],
) -> Callable[[], QtWidgets.QPushButton]:
    report_issue_windows = []

    def inner() -> QtWidgets.QPushButton:
        report_issue_window = create_report_issue_window()
        report_issue_windows.append(report_issue_window)

        return report_issue_window.findChild(QtWidgets.QPushButton, 'dumpRemotePushButton')

    return inner


@pytest.fixture
def report_issue_window(
    description: str,
    create_report_issue_window: Callable[[], ReportIssueWindow],
) -> ReportIssueWindow:
    report_issue_window = create_report_issue_window()

    plain_text = report_issue_window.findChild(DescriptionPlainText, 'descriptionPlainText')
    plain_text.setPlainText(description)

    return report_issue_window


@pytest.fixture(autouse=True)
def create_files(
    application_version: str,
    tmpdir: tempfile.TemporaryDirectory,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(BaseConfig, 'FILEPATH', os.path.join(tmpdir.name, 'config.json'))
    config = BaseConfig(
        version=application_version,
        directory=tmpdir.name,
    )
    config.dump()

    filepath = os.path.join(tmpdir.name, 'settings.ini')
    with open(filepath, 'w') as file:
        file.write('')

    filepath = os.path.join(tmpdir.name, 'app.log')
    with open(filepath, 'w') as file:
        file.write('')

    n_files = 10
    for i in range(n_files - 3):
        filepath = os.path.join(tmpdir.name, f'test {i}.xml')
        with open(filepath, 'w') as file:
            file.write('')

    yield
