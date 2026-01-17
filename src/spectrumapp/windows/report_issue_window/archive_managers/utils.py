import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Generator, Iterator


LOGGER = logging.getLogger('spectrumapp')


def walk(
    files: Sequence[Path],
    directory: Path | None,
) -> Iterator[Path]:
    """Walk iterable along files and directory's files."""

    for file in files:
        if file.exists():
            yield file

    if directory:
        for filedir, _, filenames in directory.walk():
            for filename in filenames:
                yield filedir / filename


def explore(
    files: Sequence[Path],
    prefix: Path | None = None,
) -> Generator[tuple[Path, Path], None, None]:

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            '%s files were found: %s',
            len(files),
            ', '.join(map(repr, files)),
        )

    for file in files:
        yield prefix, file
