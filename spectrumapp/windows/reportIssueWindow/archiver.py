import os
from abc import ABC, abstractmethod
from typing import Iterator

from zipfile import ZipFile

from spectrumapp.types import DirPath, FilePath


class AbstractArchiver(ABC):

    @property
    def filedir(self) -> DirPath:
        filedir = os.path.join('.', 'dumps')
        if not os.path.isdir(filedir):
            os.mkdir(filedir)

        return filedir

    def get_filename(self, timestamp: str) -> str:
        return timestamp.replace('.', '').replace(':', '').replace(' ', '_')

    @abstractmethod
    def get_filepath(self, timestamp: str) -> FilePath:
        raise NotImplementedError

    @abstractmethod
    def dump(self, filepath: FilePath, files: Iterator[FilePath]) -> None:
        raise NotImplementedError


class ZipArchiver(AbstractArchiver):

    def get_filepath(self, timestamp: str) -> FilePath:
        filename = '{filename}.{extension}'.format(
            filename=self.get_filename(timestamp),
            extension='zip',
        )

        return os.path.join(self.filedir, filename)

    def dump(self, files: Iterator[FilePath], timestamp: str) -> None:
        """Archive files to .zip archive."""

        filepath = self.get_filepath(
            timestamp=timestamp,
        )

        with ZipFile(filepath, 'w') as zip:
            for file in files:
                zip.write(file)
