from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.splash_screen_window import (
    SplashScreenState,
    SplashScreenWindow,
)


def test_on_updated(
    splash_screen_window: SplashScreenWindow,
    qtbot: QtBot,
):
    progress = 42
    info = 'info'
    message = 'message'

    splash_screen_window.updated.emit(SplashScreenState(
        progress=progress,
        info=info,
        message=message,
    ))

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == progress
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == info
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == message


def test_on_updated_progress(
    splash_screen_window: SplashScreenWindow,
    default_info: str,
    default_message: str,
    qtbot: QtBot,
):
    progress = 42

    splash_screen_window.updated.emit(SplashScreenState(
        progress=progress,
    ))

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == progress
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == default_info
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == default_message


def test_on_updated_info(
    splash_screen_window: SplashScreenWindow,
    default_progress: int,
    default_message: str,
    qtbot: QtBot,
):
    info = 'info'

    splash_screen_window.updated.emit(SplashScreenState(
        info=info,
    ))

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == default_progress
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == 'info'
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == default_message


def test_on_updated_message(
    splash_screen_window: SplashScreenWindow,
    default_progress: int,
    default_info: str,
    qtbot: QtBot,
):
    message = 'message'

    splash_screen_window.updated.emit(SplashScreenState(
        message=message,
    ))

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == default_progress
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == default_info
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == 'message'
