import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path


LOGGER = logging.getLogger('spectrumapp')


class ArchiveManagerABC(ABC):

    def __init__(
        self,
        files: Sequence[tuple[Path, Path]],
        archive_name: str,
        archive_dir: Path | None = None,
    ) -> None:

        self._files = files

        self._archive_name = archive_name
        self._archive_dir = archive_dir or Path.cwd() / 'dumps'

    @property
    def archive_name(self) -> str:
        return self._archive_name

    @property
    def archive_dir(self) -> Path:
        self._archive_dir.mkdir(parents=True, exist_ok=True)

        return self._archive_dir

    @property
    @abstractmethod
    def archive_path(self) -> Path:
        raise NotImplementedError

    @abstractmethod
    def dump(
        self,
        directory: Path | None = None,
    ) -> None:
        raise NotImplementedError
