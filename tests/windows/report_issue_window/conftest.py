import os
import tempfile
from datetime import datetime

import pytest

from spectrumapp.config import BaseConfig
from spectrumapp.windows.report_issue_window import ReportIssueWindow
from spectrumapp.windows.report_issue_window.archiver import (
    AbstractArchiver,
    ZipArchiver,
)
from spectrumapp.windows.report_issue_window.delivery import (
    AbstractDelivery,
    TelegramDelivery,
)
from spectrumapp.windows.report_issue_window.report_issue_window import (
    DescriptionPlainText,
)


@pytest.fixture
def tmpdir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory()


@pytest.fixture
def timestamp() -> str:
    return datetime.now().strftime('%Y.%m.%d %H:%M')


@pytest.fixture(params=['test'])
def description(request) -> str:
    return request.param


@pytest.fixture
def archiver(
    tmpdir: tempfile.TemporaryDirectory,
    timestamp: str,
) -> ZipArchiver:
    return ZipArchiver(
        filename=timestamp,
        filedir=tmpdir.name,
    )


@pytest.fixture
def delivery(
    timestamp: str,
) -> TelegramDelivery:
    return TelegramDelivery(
        timestamp=timestamp,
        token='',
        chat_id='',
    )


@pytest.fixture
def report_issue_window(
    description: str,
    archiver: AbstractArchiver,
    delivery: AbstractDelivery,
    monkeypatch: pytest.MonkeyPatch,
) -> ReportIssueWindow:
    monkeypatch.setattr('time.sleep', lambda *args, **kwargs: ...)

    report_issue_window = ReportIssueWindow(
        archiver=archiver,
        delivery=delivery,
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
