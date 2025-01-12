from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.modifiers import refresh


def test_wait(
    object_name: str,
    window: QtWidgets.QWidget,
    mocker,
    qtbot: QtBot,
):
    spy_on_refreshed = mocker.spy(window, 'on_refreshed')

    @refresh(object_name)
    def func() -> None:
        pass

    func()

    spy_on_refreshed.assert_called_once_with()
