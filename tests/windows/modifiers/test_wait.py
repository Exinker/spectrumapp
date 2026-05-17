from PySide6 import QtCore, QtWidgets
import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.windows.modifiers import wait


class CustomException(Exception):
    pass


def test_wait_success(
    mocker,
):
    spy_set_override_cursor = mocker.spy(QtWidgets.QApplication, 'setOverrideCursor')
    spy_restore_override_cursor = mocker.spy(QtWidgets.QApplication, 'restoreOverrideCursor')

    wrapped = mocker.Mock()
    decorated = wait(wrapped)

    decorated()

    wrapped.assert_called_once_with()
    spy_set_override_cursor.assert_called_once_with(QtCore.Qt.WaitCursor)
    spy_restore_override_cursor.assert_called_once_with()


def test_wait_exception_raised(
    mocker,
):
    spy_set_override_cursor = mocker.spy(QtWidgets.QApplication, 'setOverrideCursor')
    spy_restore_override_cursor = mocker.spy(QtWidgets.QApplication, 'restoreOverrideCursor')

    wrapped = mocker.Mock(side_effect=CustomException)
    decorated = wait(wrapped)

    with pytest.raises(CustomException):
        decorated()

    wrapped.assert_called_once_with()
    spy_set_override_cursor.assert_called_once_with(QtCore.Qt.WaitCursor)
    spy_restore_override_cursor.assert_called_once_with()


def test_wait_nested(
    mocker,
):
    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

    try:
        spy_set_override_cursor = mocker.spy(QtWidgets.QApplication, 'setOverrideCursor')
        spy_restore_override_cursor = mocker.spy(QtWidgets.QApplication, 'restoreOverrideCursor')

        wrapped = mocker.Mock()
        decorated = wait(wrapped)

        decorated()

        wrapped.assert_called_once_with()
        spy_set_override_cursor.assert_not_called()
        spy_restore_override_cursor.assert_not_called()

    finally:
        QtWidgets.QApplication.restoreOverrideCursor()
