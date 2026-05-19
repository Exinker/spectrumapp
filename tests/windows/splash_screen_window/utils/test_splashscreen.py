import importlib

from spectrumapp.windows.splash_screen_window import (
    SplashScreenState,
    SplashScreenWindow,
)
from spectrumapp.windows.splash_screen_window import utils


splashscreen_module = importlib.import_module('spectrumapp.windows.splash_screen_window.utils.splashscreen')


def test_splashscreen(
    default_progress: int,
    default_info: str,
    default_message: str,
    splash_screen_window: SplashScreenWindow,
    mocker,
):
    mocker.patch.object(splashscreen_module, 'find_window', return_value=splash_screen_window)

    spy_on_updated = mocker.spy(splash_screen_window, 'on_updated')
    spy_close = mocker.spy(splash_screen_window, 'close')

    @utils.splashscreen(progress=default_progress, info=default_info, message=default_message)
    def func() -> None:
        pass

    func()

    spy_on_updated.assert_called_once_with(SplashScreenState(
        progress=default_progress,
        info=default_info,
        message=default_message,
    ))
    spy_close.assert_not_called()
