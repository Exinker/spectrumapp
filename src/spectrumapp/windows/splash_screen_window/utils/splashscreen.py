import time
from functools import wraps
from typing import Callable

from spectrumapp.helpers import find_window
from spectrumapp.windows.splash_screen_window.splash_screen_window import (
    SplashScreenState,
    SplashScreenWindow,
)


def splashscreen(
    progress: int | None = None,
    info: str | None = None,
    message: str | None = None,
    delay: float = 0,
) -> Callable:
    """Splash screen decorator for Qt applications."""
    window_name = 'splashScreenWindow'

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # window
            window = find_window(window_name) or SplashScreenWindow()
            window.show()
            window.updated.emit(SplashScreenState(
                progress=progress,
                info=info,
                message=message,
            ))

            # delay
            time.sleep(delay)

            #
            return func(*args, **kwargs)

        return wrapper
    return decorator
