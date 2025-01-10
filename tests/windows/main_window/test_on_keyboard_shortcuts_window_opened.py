import platform

import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.helpers import (
    find_action,
    find_menu,
    find_window,
)
from spectrumapp.windows.keyboard_shortcuts_window import BaseKeyboardShortcutsWindow
from spectrumapp.windows.main_window import BaseMainWindow


@pytest.mark.skipif(
    condition=platform.system() in ['Darwin'],
    reason='Only Windows is supported!',
)
def test_on_report_issue_window_opened_by_menu(
    main_window: BaseMainWindow,
    qtbot: QtBot,
):

    menu = find_menu(main_window, '&Help')
    action = find_action(menu, '&Keyboard Shortcuts')
    action.trigger()

    window = find_window('baseKeyboardShortcutsWindow')
    assert isinstance(window, BaseKeyboardShortcutsWindow)
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
    class FakeBaseKeyboardShortcutsWindow(BaseKeyboardShortcutsWindow):
        counts = 0

        def __new__(cls, *args, **kwargs):
            cls.counts += 1
            return super().__new__(cls, *args, **kwargs)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, object_name='keyboardShortcutsWindow', **kwargs)

    monkeypatch.setattr('spectrumapp.windows.main_window.BaseKeyboardShortcutsWindow', FakeBaseKeyboardShortcutsWindow)

    for _ in range(counts):
        main_window.on_keyboard_shortcuts_window_opened()

    assert FakeBaseKeyboardShortcutsWindow.counts == 1
