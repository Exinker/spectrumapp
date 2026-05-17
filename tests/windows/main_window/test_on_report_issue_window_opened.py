import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.helpers import (
    find_action,
    find_menu,
)
from spectrumapp.windows.main_window import BaseMainWindow


def test_on_report_issue_window_opened(
    main_window: BaseMainWindow,
):
    with pytest.raises(NotImplementedError):
        main_window.on_report_issue_window_opened()


def test_report_issue_action_exists(
    main_window: BaseMainWindow,
):
    menu = find_menu(main_window, '&Help')
    action = find_action(menu, '&Report Issue')

    assert action is not None
    assert action.shortcut().toString() == 'Ctrl+Shift+I'
