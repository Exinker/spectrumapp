import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.windows.splash_screen_window import SplashScreenWindow
from spectrumapp.windows.splash_screen_window.splash_screen_window import ContentWidget


@pytest.fixture
def splash_screen_window(
    qtbot: QtBot,
) -> SplashScreenWindow:

    splash_screen_window = SplashScreenWindow()

    return splash_screen_window


@pytest.fixture
def default_progress(
    splash_screen_window: SplashScreenWindow,
) -> SplashScreenWindow:

    return splash_screen_window.findChild(ContentWidget, 'contentWidget').DEFAULT_PROGRESS


@pytest.fixture
def default_info(
    splash_screen_window: SplashScreenWindow,
) -> SplashScreenWindow:

    return splash_screen_window.findChild(ContentWidget, 'contentWidget').DEFAULT_INFO


@pytest.fixture
def default_message(
    splash_screen_window: SplashScreenWindow,
) -> SplashScreenWindow:

    return splash_screen_window.findChild(ContentWidget, 'contentWidget').DEFAULT_MESSAGE
