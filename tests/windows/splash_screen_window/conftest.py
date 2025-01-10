import pytest

from spectrumapp.windows.splash_screen_window import SplashScreenWindow


@pytest.fixture
def splash_screen_window() -> SplashScreenWindow:

    splash_screen_window = SplashScreenWindow()

    return splash_screen_window
