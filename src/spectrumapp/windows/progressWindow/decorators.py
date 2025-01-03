from typing import Iterable

from spectrumapp.helpers import find_window
from spectrumapp.windows.progressWindow.progressWindow import ProgressWindow


def progress(iterable: Iterable, info: str | None = ''):
    """Progress decorator for long time processes."""
    window_name = 'processWindow'

    try:
        n_items = len(iterable)
    except (TypeError, AttributeError):
        n_items = None

    window = find_window(window_name)
    if window is not None:
        window.show()
    else:
        window = ProgressWindow()

    try:
        for i, item in enumerate(iterable):
            window.update(
                progress='' if n_items is None else int(100*(i + 1) / n_items),
                info=info,
                message='' if n_items is None else f'<strong>{item}</strong> ({i + 1}/{n_items})',
            )

            yield item

    finally:
        window.setParent(None)
        window.close()
