import os
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

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
def application_name(
    faker,
) -> str:
    return '-'.join(faker.catch_phrase().lower().split(' '))


@pytest.fixture
def application_version(
    faker,
) -> str:
    return faker.numerify("%#.%#.%#")


@pytest.fixture
def timestamp() -> float:
    return datetime.timestamp(datetime.now())


@pytest.fixture(params=['test'])
def description(request) -> str:
    return request.param


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
def report_issue_window(
    description: str,
    application_name: str,
    application_version: str,
    timestamp: float,
    archive_manager: ArchiveManagerABC,
    report_manager: ReportManagerABS,
    monkeypatch: pytest.MonkeyPatch,
) -> ReportIssueWindow:
    # monkeypatch.setattr('time.sleep', lambda *args, **kwargs: ...)

    report_issue_window = ReportIssueWindow(
        application_name=application_name,
        application_version=application_version,
        timestamp=timestamp,
        archive_manager=archive_manager,
        report_manager=report_manager,
    )

    plain_text = report_issue_window.findChild(DescriptionPlainText, 'descriptionPlainText')
    plain_text.setPlainText(description)

    return report_issue_window


@pytest.fixture(autouse=True)
def create_files(
    tmpdir: tempfile.TemporaryDirectory,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(BaseConfig, 'FILEPATH', os.path.join(tmpdir.name, 'config.json'))
    config = BaseConfig(
        version=os.environ['APPLICATION_VERSION'],
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
