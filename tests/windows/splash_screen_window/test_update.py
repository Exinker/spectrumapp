import pytest
from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.splash_screen_window import SplashScreenWindow


def test_update(
    splash_screen_window: SplashScreenWindow,
    qtbot: QtBot,
):
    progress = 42
    info = 'info'
    message = 'message'

    splash_screen_window.update(
        progress=progress,
        info=info,
        message=message,
    )

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == progress
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == info
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == message


def test_update_progress(
    splash_screen_window: SplashScreenWindow,
    qtbot: QtBot,
):
    progress = 42

    splash_screen_window.update(
        progress=progress,
    )

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == progress
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == '<strong>LOADING</strong>...'
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == ''


def test_update_info(
    splash_screen_window: SplashScreenWindow,
    qtbot: QtBot,
):
    info = 'info'

    splash_screen_window.update(
        info=info,
    )

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == 0
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == 'info'
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == ''


def test_update_message(
    splash_screen_window: SplashScreenWindow,
    qtbot: QtBot,
):
    message = 'message'

    splash_screen_window.update(
        message=message,
    )

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == 0
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == '<strong>LOADING</strong>...'
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == 'message'
