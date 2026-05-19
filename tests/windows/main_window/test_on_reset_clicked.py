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
    action = find_action(main_window, '&Reset')

    assert action.shortcut().toString() == 'Ctrl+Shift+R'

    action.trigger()

    main_window.on_resetted_mock.assert_called()
