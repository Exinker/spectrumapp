from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.modifiers import close


def test_close(
    object_name: str,
    window: QtWidgets.QWidget,
    mocker,
    qtbot: QtBot,
):
    spy_close = mocker.spy(window, 'close')

    @close(object_name)
    def func() -> None:
        pass

    func()

    spy_close.assert_called_once_with()
