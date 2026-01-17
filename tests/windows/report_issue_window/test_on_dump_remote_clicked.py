import platform

import pytest
from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.exception_window import ExceptionDialog, ExceptionLevel
from spectrumapp.windows.report_issue_window import ReportIssueWindow


class FakeExceptionDialog(ExceptionDialog):

    DIALOGS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show(self) -> None:  # noqa: N802
        cls = self.__class__

        cls.DIALOGS.append(self)


def test_on_click_error_when_env_file_not_found(
    report_issue_window: ReportIssueWindow,
    monkeypatch: pytest.MonkeyPatch,
    qtbot: QtBot,
):
    monkeypatch.setattr('spectrumapp.windows.report_issue_window.report_managers.telegram_report_managers.ExceptionDialog', FakeExceptionDialog)  # noqa: E501

    button = report_issue_window.findChild(QtWidgets.QPushButton, 'dumpRemotePushButton')
    button.click()

    assert len(FakeExceptionDialog.DIALOGS) == 1

    dialog, *_ = FakeExceptionDialog.DIALOGS
    assert dialog.message == 'Send message failed with AuthorizationError!'
    assert dialog.info == 'File is not found. Create .env file with Telegram credentials!'
    assert dialog.level == ExceptionLevel.WARNING
