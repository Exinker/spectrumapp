from PySide6 import QtCore, QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.modifiers import wait


def test_wait(
    mocker,
    qtbot: QtBot,
):
    spy_set_override_cursor = mocker.spy(QtWidgets.QApplication, 'setOverrideCursor')
    spy_restore_override_cursor = mocker.spy(QtWidgets.QApplication, 'restoreOverrideCursor')

    @wait
    def func() -> None:
        pass

    func()

    spy_set_override_cursor.assert_called_once_with(QtCore.Qt.WaitCursor)
    spy_restore_override_cursor.assert_called_once_with()
