from PySide6 import QtWidgets
import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.windows.modifiers import refresh


class CustomException(Exception):
    pass


def test_refresh_success(
    object_name: str,
    window: QtWidgets.QWidget,
    monkeypatch: pytest.MonkeyPatch,
    mocker,
    qtbot: QtBot,
):
    monkeypatch.setattr('spectrumapp.windows.modifiers.find_window', lambda *args, **kwargs: window)

    wrapped = mocker.Mock()
    decorated = refresh(object_name)(wrapped)

    with qtbot.waitSignal(window.refreshed):
        decorated()

    wrapped.assert_called_once_with()


def test_refresh_exception_raised(
    object_name: str,
    window: QtWidgets.QWidget,
    monkeypatch: pytest.MonkeyPatch,
    mocker,
    qtbot: QtBot,
):
    monkeypatch.setattr('spectrumapp.windows.modifiers.find_window', lambda *args, **kwargs: window)

    wrapped = mocker.Mock(side_effect=CustomException)
    decorated = refresh(object_name)(wrapped)

    with qtbot.waitSignal(window.refreshed):
        with pytest.raises(CustomException):
            decorated()

    wrapped.assert_called_once_with()
