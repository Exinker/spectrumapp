from PySide6 import QtCore, QtTest

from spectrumapp.helpers import (
    find_action,
    find_menu,
)
from spectrumapp.windows.main_window import BaseMainWindow


def test_on_reset_clicked_by_menu(
    main_window: BaseMainWindow,
):
    menu = find_menu(main_window, '&File')
    action = find_action(menu, '&Reset')

    action.trigger()

    main_window.on_resetted_mock.assert_called()


def test_on_reset_clicked_by_shortcut(
    main_window: BaseMainWindow,
):
    QtTest.QTest.keyClick(
        main_window,
        QtCore.Qt.Key.Key_R,
        QtCore.Qt.KeyboardModifier.ControlModifier | QtCore.Qt.KeyboardModifier.ShiftModifier,
    )

    main_window.on_resetted_mock.assert_called()
