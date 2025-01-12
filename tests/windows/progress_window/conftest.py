import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.windows.progress_window import ProgressWindow
from spectrumapp.windows.progress_window.progress_window import ContentWidget


@pytest.fixture
def progress_window(
    qtbot: QtBot,
) -> ProgressWindow:

    progress_window = ProgressWindow()

    return progress_window


@pytest.fixture
def default_logging_text(
    progress_window: ProgressWindow,
) -> ProgressWindow:

    return progress_window.findChild(ContentWidget, 'contentWidget').DEFAULT_LOGGING_TEXT


@pytest.fixture
def default_progress(
    progress_window: ProgressWindow,
) -> ProgressWindow:

    return progress_window.findChild(ContentWidget, 'contentWidget').DEFAULT_PROGRESS


@pytest.fixture
def default_info(
    progress_window: ProgressWindow,
) -> ProgressWindow:

    return progress_window.findChild(ContentWidget, 'contentWidget').DEFAULT_INFO


@pytest.fixture
def default_message(
    progress_window: ProgressWindow,
) -> ProgressWindow:

    return progress_window.findChild(ContentWidget, 'contentWidget').DEFAULT_MESSAGE
