from spectrumapp.helpers import (
    find_action,
    find_menu,
)
from spectrumapp.windows.main_window import BaseMainWindow


def test_on_close_clicked_by_menu(
    main_window: BaseMainWindow,
):
    menu = find_menu(main_window, '&File')
    action = find_action(menu, '&Quit')

    action.trigger()

    assert not main_window.isVisible()


def test_on_close_clicked_by_shortcut(
    main_window: BaseMainWindow,
):
    action = find_action(main_window, '&Quit')

    assert action.shortcut().toString() == 'Ctrl+Q'

    action.trigger()

    assert not main_window.isVisible()
