import os
import uuid
from pathlib import Path

import pytest
from telepot.exception import (
    TelegramError,
)

from spectrumapp.windows.exception_window import ExceptionDialog, ExceptionLevel
from spectrumapp.windows.report_issue_window.report_managers import TelegramReportManager


@pytest.fixture(scope='function')
def filepath(
    tmp_path: Path,
) -> Path:

    filepath = tmp_path / f'{uuid.uuid4()}.zip'
    with open(filepath, 'wb') as file:
        file.write(b'')

    yield filepath

    os.remove(filepath)


@pytest.mark.skip(reason='FIXNE: переделать на mock!')
def test_telegram_delivery_send(
    report_manager: TelegramReportManager,
    filepath: Path,
    description: str,
    mocker,
):
    mock = mocker.patch.object(report_manager.bot, 'sendDocument')

    report_manager.send(
        archive_path=filepath,
        description=description,
    )

    mock.assert_called_once()


def raise_exception(exception, *args, **kwargs):

    def wrapper(
        chat_id: str,
        document: bytes,
        caption: str,
    ):
        raise exception(*args, **kwargs)

    return wrapper


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
) -> FakeExceptionDialog:

    match telegram_error_code:
        case 400:
            return FakeExceptionDialog(
                message='Send message failed with AuthorizationError!',
                info='TELEGRAM_CHAT_ID is invalid!',
                level=ExceptionLevel.WARNING,
            )
        case 404:
            return FakeExceptionDialog(
                message='Send message failed with AuthorizationError!',
                info='File is not found. Create .env file with Telegram credentials!',
                level=ExceptionLevel.WARNING,
            )


def assert_dialog(
    dialog: ExceptionDialog,
    expected: ExceptionDialog,
) -> None:
    assert dialog.message == expected.message
    assert dialog.info == expected.info
    assert dialog.level == expected.level


@pytest.mark.skip(reason='FIXNE: переделать на mock!')
def test_telegram_delivery_send_with_telegram_error_raised(
    report_manager: TelegramReportManager,
    filepath: Path,
    description: str,
    telegram_error_code: int,
    expected: FakeExceptionDialog,
    monkeypatch: pytest.MonkeyPatch,
    mocker,
):
    monkeypatch.setattr('spectrumapp.windows.report_issue_window.delivery.ExceptionDialog', FakeExceptionDialog)
    mock = mocker.patch.object(report_manager.bot, 'sendDocument', side_effect=raise_exception(
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
    assert_dialog(
        dialog=FakeExceptionDialog.DIALOGS[-1],
        expected=expected,
    )
