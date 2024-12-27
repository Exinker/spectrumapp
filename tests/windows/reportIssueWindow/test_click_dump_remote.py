import sys

import pytest
from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.exceptionWindow import ExceptionDialog, ExceptionLevel
from spectrumapp.windows.reportIssueWindow import ReportIssueWindow


class FakeExceptionDialog(ExceptionDialog):

    DIALOGS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show(self) -> None:  # noqa: N802
        cls = self.__class__

        cls.DIALOGS.append(self)


@pytest.mark.skipif(condition=sys.platform == 'darwin', reason='FIXME: fix it in Mac OS')
def test_on_click_error_when_env_file_not_found(
    window: ReportIssueWindow,
    monkeypatch: pytest.MonkeyPatch,
    qtbot: QtBot,
):
    monkeypatch.setattr('spectrumapp.windows.reportIssueWindow.delivery.ExceptionDialog', FakeExceptionDialog)

    button = window.findChild(QtWidgets.QPushButton, 'dumpRemotePushButton')
    button.click()

    dialog, *_ = FakeExceptionDialog.DIALOGS
    assert len(FakeExceptionDialog.DIALOGS) == 1
    assert dialog.level == ExceptionLevel.WARNING
    assert dialog.message == 'Send message failed with AuthorizationError!'
    assert dialog.info == 'File is not found. Create .env file with Telegram credentials!'
