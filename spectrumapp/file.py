import os

from .types import DirPath


class File:

    def __init__(self, filedir: DirPath) -> None:
        filedir = os.path.abspath(filedir)
        _, filename = os.path.split(filedir)

        self._filedir = filedir
        self._filename = filename

    @property
    def filedir(self) -> DirPath:
        return self._filedir

    @property
    def filename(self) -> str:
        return self._filename
