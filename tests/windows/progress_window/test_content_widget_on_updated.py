from PySide6 import QtWidgets

from spectrumapp.windows.progress_window import (
    ProgressState,
    ProgressWindow,
)


def test_content_widget_on_updated(
    progress_window: ProgressWindow,
):
    progress = 42
    info = 'info'
    message = 'message'

    progress_window.updated.emit(ProgressState(
        progress=progress,
        info=info,
        message=message,
    ))

    assert progress_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == progress
    assert progress_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == info
    assert progress_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == message


def test_content_widget_on_updated_progress_only(
    progress_window: ProgressWindow,
    default_info: str,
    default_message: str,
):
    value = 42

    progress_window.updated.emit(ProgressState(
        progress=value,
    ))

    assert progress_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == value
    assert progress_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == default_info
    assert progress_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == default_message


def test_content_widget_on_updated_info_only(
    progress_window: ProgressWindow,
    default_progress: int,
    default_message: str,
):
    text = 'test'

    progress_window.updated.emit(ProgressState(
        info=text,
    ))

    assert progress_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == default_progress
    assert progress_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == text
    assert progress_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == default_message


def test_content_widget_on_updated_message_only(
    progress_window: ProgressWindow,
    default_progress: int,
    default_info: str,
):
    text = 'test'

    progress_window.updated.emit(ProgressState(
        message=text,
    ))

    assert progress_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == default_progress
    assert progress_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == default_info
    assert progress_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == text
