from PySide6 import QtCore, QtTest

from spectrumapp.helpers import (
    find_action,
    find_menu,
)
from spectrumapp.windows.main_window import BaseMainWindow


def test_on_directory_open_clicked_by_menu(
    main_window: BaseMainWindow,
):
    menu = find_menu(main_window, '&File')
    action = find_action(menu, '&Open...')

    action.trigger()

    main_window.on_directory_opened_mock.assert_called()


def test_on_directory_open_clicked_by_shortcut(
    main_window: BaseMainWindow,
):
    QtTest.QTest.keyClick(
        main_window,
        QtCore.Qt.Key.Key_O,
        QtCore.Qt.KeyboardModifier.ControlModifier,
    )

    main_window.on_directory_opened_mock.assert_called()
