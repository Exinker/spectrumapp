from PySide6 import QtCore, QtTest
from pytestqt.qtbot import QtBot

from spectrumapp.helpers import (
    find_action,
    find_menu,
)
from spectrumapp.windows.main_window import BaseMainWindow


def test_on_close_clicked_by_menu(
    main_window: BaseMainWindow,
    qtbot: QtBot,
):

    menu = find_menu(main_window, '&File')
    action = find_action(menu, '&Quit')
    action.trigger()

    assert not main_window.isVisible()


def test_on_close_clicked_by_shortcut(
    main_window: BaseMainWindow,
    qtbot: QtBot,
):

    QtTest.QTest.keyClick(
        main_window,
        QtCore.Qt.Key.Key_Q,
        QtCore.Qt.KeyboardModifier.ControlModifier,
    )

    assert not main_window.isVisible()
