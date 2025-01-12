import pytest
from PySide6 import QtCore, QtTest
from pytestqt.qtbot import QtBot

from spectrumapp.helpers import (
    find_action,
    find_menu,
    find_window,
)
from spectrumapp.windows.main_window import BaseMainWindow
from spectrumapp.windows.report_issue_window import ReportIssueWindow


def test_on_report_issue_window_opened_by_menu(
    main_window: BaseMainWindow,
    qtbot: QtBot,
):

    menu = find_menu(main_window, '&Help')
    action = find_action(menu, '&Report Issue')
    action.trigger()

    window = find_window('reportIssueWindow')
    assert isinstance(window, ReportIssueWindow)
    assert window.isVisible()


def test_on_report_issue_window_opened_by_shortcut(
    main_window: BaseMainWindow,
    qtbot: QtBot,
):

    QtTest.QTest.keyClick(
        main_window,
        QtCore.Qt.Key.Key_I,
        QtCore.Qt.KeyboardModifier.ControlModifier | QtCore.Qt.KeyboardModifier.ShiftModifier,
    )

    window = find_window('reportIssueWindow')
    assert isinstance(window, ReportIssueWindow)
    assert window.isVisible()


@pytest.mark.parametrize(
    'counts',
    [1, 2, 10],
)
def test_on_report_issue_window_opened_once(
    counts: int,
    main_window: BaseMainWindow,
    monkeypatch: pytest.MonkeyPatch,
    qtbot: QtBot,
):
    class FakeReportIssueWindow(ReportIssueWindow):
        counts = 0

        def __new__(cls, *args, **kwargs):
            cls.counts += 1
            return super().__new__(cls, *args, **kwargs)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, object_name='reportIssueWindow', **kwargs)

    monkeypatch.setattr('spectrumapp.windows.main_window.ReportIssueWindow', FakeReportIssueWindow)

    for _ in range(counts):
        main_window.on_report_issue_window_opened()

    assert FakeReportIssueWindow.counts == 1
