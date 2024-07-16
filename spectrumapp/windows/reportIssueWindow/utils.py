import os
from typing import Iterator

from spectrumapp.config import File
from spectrumapp.types import FilePath


def walk(file: File) -> Iterator[FilePath]:
    """Walk iterable along folders."""

    # root (app's directory)
    root = '.'
    for filename in ('app.log', 'config.json', 'settings.ini'):
        filepath = os.path.join(root, filename)

        if os.path.exists(filepath):
            yield filepath

    # directory (data's directories)
    for filedir, _, filenames in os.walk(file.directory):
        for filename in filenames:
            filepath = os.path.join(filedir, filename)

            yield filepath
