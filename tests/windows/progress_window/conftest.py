import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.windows.progress_window import ProgressWindow


@pytest.fixture
def progress_window(
    qtbot: QtBot,
) -> ProgressWindow:

    progress_window = ProgressWindow()
    qtbot.addWidget(progress_window)

    return progress_window
