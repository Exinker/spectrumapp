import os
import uuid
from dataclasses import dataclass
from pathlib import Path

import pytest
from telepot.exception import (
    TelegramError,
)

from spectrumapp.windows.exception_window import ExceptionDialog, ExceptionLevel
from spectrumapp.windows.report_issue_window.report_managers import TelegramReportManager


@dataclass
class ExpectedDialog:
    message: str
    info: str
    level: ExceptionLevel


@pytest.fixture(scope='function')
def filepath(
    tmp_path: Path,
) -> Path:

    filepath = tmp_path / f'{uuid.uuid4()}.zip'
    with open(filepath, 'wb') as file:
        file.write(b'')

    yield filepath

    os.remove(filepath)


def test_telegram_delivery_send(
    report_manager: TelegramReportManager,
    filepath: Path,
    description: str,
    mocker,
):
    mock = mocker.patch.object(report_manager._bot, 'sendDocument')

    report_manager.send(
        archive_path=filepath,
        description=description,
    )

    mock.assert_called_once()


def raise_exception(exception, *args, **kwargs):

    def inner(
        chat_id: str,
        document: bytes,
        caption: str,
    ):
        raise exception(*args, **kwargs)

    return inner


class FakeExceptionDialog(ExceptionDialog):

    DIALOGS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show(self) -> None:  # noqa: N802
        cls = self.__class__

        cls.DIALOGS.append(self)


@pytest.fixture(params=[400, 404])
def telegram_error_code(request) -> int:
    return request.param


@pytest.fixture
def expected(
    telegram_error_code: int,
) -> ExpectedDialog:

    match telegram_error_code:
        case 400:
            return ExpectedDialog(
                message='Send message failed with AuthorizationError!',
                info='TELEGRAM_CHAT_ID is invalid!',
                level=ExceptionLevel.WARNING,
            )
        case 404:
            return ExpectedDialog(
                message='Send message failed with AuthorizationError!',
                info='File is not found. Create .env file with Telegram credentials!',
                level=ExceptionLevel.WARNING,
            )


def test_telegram_delivery_send_with_telegram_error_raised(
    report_manager: TelegramReportManager,
    filepath: Path,
    description: str,
    telegram_error_code: int,
    expected: FakeExceptionDialog,
    monkeypatch: pytest.MonkeyPatch,
    mocker,
):
    FakeExceptionDialog.DIALOGS.clear()
    monkeypatch.setattr(
        'spectrumapp.windows.report_issue_window.report_managers.telegram_report_managers.ExceptionDialog',
        FakeExceptionDialog,
    )
    mock = mocker.patch.object(report_manager._bot, 'sendDocument', side_effect=raise_exception(
        TelegramError,
        description='',
        error_code=telegram_error_code,
        json='',
    ))

    report_manager.send(
        archive_path=filepath,
        description=description,
    )

    mock.assert_called_once()

    dialog = FakeExceptionDialog.DIALOGS[-1]
    assert dialog.message == expected.message
    assert dialog.info == expected.info
    assert dialog.level == expected.level
