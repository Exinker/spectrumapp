from typing import Any, Generator, Iterable

from spectrumapp.helpers import find_window
from spectrumapp.windows.progress_window.progress_window import (
    ProgressState,
    ProgressWindow,
)


def progress(items: Iterable[Any], info: str | None = '') -> Generator:
    """Progress wrapper for long time processes."""
    window_name = 'splashScreenWindow'

    try:
        n_items = len(items)
    except (TypeError, AttributeError):
        n_items = None

    window = find_window(window_name) or ProgressWindow()
    window.show()

    try:
        for i, item in enumerate(items, start=1):
            window.updated.emit(ProgressState(
                progress=_get_progress(i, total=n_items),
                info=info,
                message=_get_message(i, item, total=n_items),
            ))

            yield item
    finally:
        window.setParent(None)
        window.close()


def _get_progress(__i: int, total: int | None) -> int | None:

    if total is None:
        return None
    return int(__i*100/total)


def _get_message(__i: int, __item: Any, total: int | None) -> str:

    if total is None:
        return f'<strong>{__item}</strong> ({__i})'
    return f'<strong>{__item}</strong> ({__i}/{total})'
