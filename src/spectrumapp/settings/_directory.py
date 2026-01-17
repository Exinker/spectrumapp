import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

from PySide6 import QtWidgets


class AbstractDirectoryValidator(ABC):

    @abstractmethod
    def check(self, directory: Path) -> bool:
        raise NotImplementedError


class NoneDirectoryValidator(AbstractDirectoryValidator):

    def check(self, directory: Path) -> bool:
        return True


class ContainAnyFileDirectoryValidator(AbstractDirectoryValidator):

    def __init__(self, filenames: Sequence[str]):
        self.filenames = filenames

    def check(self, directory: Path) -> bool:
        return any(os.path.isfile(os.path.join(directory, filename)) for filename in self.filenames)


class ContainAllFileDirectoryValidator(AbstractDirectoryValidator):

    def __init__(self, filenames: Sequence[str]):
        self.filenames = filenames

    def check(self, directory: Path) -> bool:
        return all(os.path.isfile(os.path.join(directory, filename)) for filename in self.filenames)


def choose_directory(
    __dir: Path,
    caption: str = 'Choose Directory',
    parent: QtWidgets.QWidget | None = None,
    validator: AbstractDirectoryValidator | None = None,
) -> Path | None:
    validator = validator or NoneDirectoryValidator()

    while True:

        directory = QtWidgets.QFileDialog().getExistingDirectory(
            caption=caption,
            dir=__dir,
            parent=parent,
        )
        directory = os.sep.join(directory.split('/'))
        if directory == '':
            return None  # cancel button was pressed
        if directory == __dir:
            return None  # choosen the same directory

        if validator.check(directory):
            return directory
