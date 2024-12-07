import logging
import os
import time
from abc import ABC, abstractmethod
from zipfile import ZipFile

from spectrumapp.types import DirPath, FilePath


LOGGER = logging.getLogger('spectrumapp')


class AbstractArchiver(ABC):

    def __init__(
        self,
        filename: str,
        filedir: DirPath | None = None,
    ) -> None:
        self._filename = filename
        self._filedir = filedir or os.path.join('.', 'dumps')

    @property
    def filename(self) -> str:
        return self._filename.replace('.', '').replace(':', '')

    @property
    def filedir(self) -> DirPath:
        if not os.path.isdir(self._filedir):
            os.mkdir(self._filedir)

        return self._filedir

    @property
    @abstractmethod
    def filepath(self) -> FilePath:
        raise NotImplementedError

    @abstractmethod
    def dump(
        self,
        files: tuple[FilePath],
        prefix: DirPath | None = None,
    ) -> None:
        raise NotImplementedError


class ZipArchiver(AbstractArchiver):
    TIMEOUT = 1  # timeout to realistic

    def dump(
        self,
        files: tuple[FilePath],
        directory: DirPath | None = None,
    ) -> None:
        """Archive selected `files` to .zip archive."""

        n_dumped = 0
        with ZipFile(self.filepath, 'w') as archive:
            for file in files:
                try:
                    archive.write(file, arcname=_get_arcname(file, directory=directory))
                except Exception as error:
                    LOGGER.warning(
                        'Write file %r failed with %s: %s',
                        file,
                        type(error).__name__,
                        error,
                    )
                else:
                    n_dumped += 1

        time.sleep(self.TIMEOUT)
        LOGGER.debug('%s files were dumped successfully.', n_dumped)

    @property
    def filepath(self) -> FilePath:
        filename = '{filename}.{extension}'.format(
            filename=self.filename,
            extension='zip',
        )

        return os.path.join(self.filedir, filename)


def _get_arcname(__file: FilePath, directory: DirPath | None = None) -> str:

    if directory:
        prefix, _ = os.path.split(directory)

        if __file.startswith(prefix):

            arcname = __file[len(prefix):]
            return arcname

    return __file
