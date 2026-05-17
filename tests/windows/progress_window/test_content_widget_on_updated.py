from PySide6 import QtWidgets

from spectrumapp.windows.progress_window import (
    ProgressState,
    ProgressWindow,
)
from spectrumapp.windows.progress_window.progress_window import ContentWidget


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
):
    value = 42

    progress_window.updated.emit(ProgressState(
        progress=value,
    ))

    assert progress_window.findChild(QtWidgets.QProgressBar, 'progressBar').value() == value
    assert progress_window.findChild(QtWidgets.QLabel, 'infoLabel').text() == ContentWidget.DEFAULT_INFO
    assert progress_window.findChild(QtWidgets.QLabel, 'messageLabel').text() == ContentWidget.DEFAULT_MESSAGE
