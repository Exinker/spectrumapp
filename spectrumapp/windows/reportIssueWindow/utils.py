import logging
import os
from typing import Iterator

from spectrumapp.config import File
from spectrumapp.types import DirPath, FilePath


LOGGER = logging.getLogger('spectrumapp')


def walk(__directory: DirPath) -> Iterator[FilePath]:
    """Walk iterable along folders."""

    # root (app's directory)
    root = '.'
    for filename in ('app.log', 'config.json', 'settings.ini'):
        filepath = os.path.join(root, filename)

        if os.path.exists(filepath):
            yield filepath

    # directory (data's directory)
    for filedir, _, filenames in os.walk(__directory):
        for filename in filenames:
            filepath = os.path.join(filedir, filename)

            yield filepath


def explore(__file: File) -> tuple[FilePath]:

    files = [file for file in walk(__file.directory)]

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            '%s files were found: %s',
            len(files),
            ', '.join(map(repr, files)),
        )

    return tuple(files)
