from unittest.mock import Mock, patch

from PySide6 import QtCore, QtTest
from pytestqt.qtbot import QtBot

from spectrumapp.helpers import (
    find_action,
    find_menu,
)
from spectrumapp.windows.main_window import BaseMainWindow


@patch('spectrumapp.windows.main_window.BaseMainWindow.not_implemented_plug')
def test_on_reset_clicked_by_menu(
    mock: Mock,
    main_window: BaseMainWindow,
    qtbot: QtBot,
):
    menu = find_menu(main_window, '&File')
    action = find_action(menu, '&Reset')

    action.trigger()

    mock.assert_called()


@patch('spectrumapp.windows.main_window.BaseMainWindow.not_implemented_plug')
def test_on_reset_clicked_by_shortcut(
    mock: Mock,
    main_window: BaseMainWindow,
    qtbot: QtBot,
):

    QtTest.QTest.keyClick(
        main_window,
        QtCore.Qt.Key.Key_R,
        QtCore.Qt.KeyboardModifier.ControlModifier | QtCore.Qt.KeyboardModifier.ShiftModifier,
    )

    mock.assert_called()
