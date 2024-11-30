import time
from typing import Any, Callable, Generator, Iterable

from spectrumapp.helpers import find_window
from spectrumapp.windows.splashScreenWindow.splashScreenWindow import SplashScreenWindow


def splashscreen(progress: int | None = None, info: str | None = None, message: str | None = None, delay: float = 0) -> Callable:
    """Splash screen decorator for Qt applications."""
    window_name = 'splashScreenWindow'

    def decorator(func):
        def wrapper(*args, **kwargs):

            # window
            window = find_window(window_name) or SplashScreenWindow()
            window.show()
            window.update(
                progress=progress,
                info=info,
                message=message,
            )

            # delay
            time.sleep(delay)

            #
            return func(*args, **kwargs)

        return wrapper
    return decorator


def iterate(items: Iterable[Any], info: str | None = '') -> Generator:
    """Iterate decorator with a progress window."""
    window_name = 'splashScreenWindow'

    # n_items
    try:
        n_items = len(items)
    except (TypeError, AttributeError):
        n_items = None

    # window
    window = find_window(window_name) or SplashScreenWindow()
    window.show()

    try:
        for i, item in enumerate(items):
            window.update(
                progress='' if n_items is None else int((i + 1)*100/n_items),
                info=info,
                message='' if n_items is None else f'<strong>{item}</strong> ({i + 1}/{n_items})',
            )

            yield item
    finally:
        window.close()
