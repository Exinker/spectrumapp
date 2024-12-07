import os
import tempfile
from datetime import datetime

import pytest

from spectrumapp.config import File
from spectrumapp.windows.reportIssueWindow import ReportIssueWindow
from spectrumapp.windows.reportIssueWindow.archiver import (
    AbstractArchiver,
    ZipArchiver,
)
from spectrumapp.windows.reportIssueWindow.delivery import (
    AbstractDelivery,
    TelegramDelivery,
)
from spectrumapp.windows.reportIssueWindow.reportIssueWindow import (
    DescriptionPlainText,
)


@pytest.fixture
def tmpdir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory()


@pytest.fixture
def timestamp() -> str:
    return datetime.now().strftime('%Y.%m.%d %H:%M')


@pytest.fixture
def description() -> str:
    return 'test description'


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
def window(
    description: str,
    archiver: AbstractArchiver,
    delivery: AbstractDelivery,
    monkeypatch: pytest.MonkeyPatch,
) -> ReportIssueWindow:
    monkeypatch.setattr('time.sleep', lambda *args, **kwargs: ...)

    window = ReportIssueWindow(
        archiver=archiver,
        delivery=delivery,
    )

    plain_text = window.findChild(DescriptionPlainText, 'descriptionPlainText')
    plain_text.setPlainText(description)

    return window


@pytest.fixture(autouse=True)
def create_files(
    tmpdir: tempfile.TemporaryDirectory,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(File, 'FILEPATH', os.path.join(tmpdir.name, 'config.json'))
    file = File(
        version=os.environ['APPLICATION_VERSION'],
        directory=tmpdir.name,
    )
    file.dump()

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
