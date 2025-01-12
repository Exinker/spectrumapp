from dataclasses import dataclass
from unittest.mock import Mock

import pytest
from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.exceptions import format_exception
from spectrumapp.windows.exception_window import (
    ExceptionDialog,
    ExceptionLevel,
)
from spectrumapp.windows.exception_window.exception_window import _get_text_template


@dataclass
class Expected:
    parent: QtWidgets.QWidget | None
    title: str
    text: str
    buttons: list[QtWidgets.QMessageBox.StandardButton]
    defaultButton: QtWidgets.QMessageBox.StandardButton  # noqa: N815


@pytest.fixture()
def mock(
    level: ExceptionLevel,
    mocker,
) -> Mock:
    mock = mocker.patch({
        ExceptionLevel.ERROR: 'PySide6.QtWidgets.QMessageBox.critical',
        ExceptionLevel.WARNING: 'PySide6.QtWidgets.QMessageBox.warning',
        ExceptionLevel.INFO: 'PySide6.QtWidgets.QMessageBox.information',
    }[level])

    return mock


@pytest.fixture()
def expected(
    message: str,
    info: str,
    level: ExceptionLevel,
) -> Expected:
    return Expected(
        parent=None,
        title={
            ExceptionLevel.ERROR: 'Error',
            ExceptionLevel.WARNING: 'Warning',
            ExceptionLevel.INFO: 'Info',
        }[level],
        text=_get_text_template(
            message=message,
        ).format(
            message=message,
            info=info or format_exception(),
        ),
        buttons=QtWidgets.QMessageBox.Close,
        defaultButton=QtWidgets.QMessageBox.Close,
    )


def test_exception_window(
    message: str,
    info: str,
    level: ExceptionLevel,
    mock: Mock,
    expected: Expected,
    qtbot: QtBot,
):
    dialog = ExceptionDialog(
        message=message,
        info=info,
        level=level,
    )
    dialog.show()

    mock.assert_called_once_with(
        expected.parent,
        expected.title,
        expected.text,
        buttons=expected.buttons,
        defaultButton=expected.defaultButton,
    )


def test_exception_window_level_invalid(
    qtbot: QtBot,
):
    message = ''
    info = ''
    level = 'invalid'

    dialog = ExceptionDialog(
        message=message,
        info=info,
        level=level,
    )

    with pytest.raises(AssertionError):
        dialog.title
    with pytest.raises(AssertionError):
        dialog.dialog
