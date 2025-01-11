from PySide6 import QtWidgets

from spectrumapp.windows.splash_screen_window import (
    SplashScreenState,
    SplashScreenWindow,
)


def test_content_widget_on_updated(
    splash_screen_window: SplashScreenWindow,
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


def test_content_widget_on_updated_progress_only(
    splash_screen_window: SplashScreenWindow,
    default_info: str,
    default_message: str,
):
    value = 42

    splash_screen_window.updated.emit(SplashScreenState(
        progress=value,
    ))

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == value
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == default_info
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == default_message


def test_content_widget_on_updated_info_only(
    splash_screen_window: SplashScreenWindow,
    default_progress: int,
    default_message: str,
):
    text = 'test'

    splash_screen_window.updated.emit(SplashScreenState(
        info=text,
    ))

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == default_progress
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == text
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == default_message


def test_content_widget_on_updated_message_only(
    splash_screen_window: SplashScreenWindow,
    default_progress: int,
    default_info: str,
):
    text = 'test'

    splash_screen_window.updated.emit(SplashScreenState(
        message=text,
    ))

    assert splash_screen_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == default_progress
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == default_info
    assert splash_screen_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == text
