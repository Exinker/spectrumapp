import os
from abc import ABC, abstractmethod
from typing import Sequence

from PySide6 import QtWidgets

from spectrumapp.types import DirPath


# --------        validators        --------
class AbstractDirectoryValidator(ABC):

    @abstractmethod
    def check(self, directory: DirPath) -> bool:
        raise NotImplementedError


class NoneDirectoryValidator(AbstractDirectoryValidator):

    def check(self, directory: DirPath) -> bool:
        return True


class ContainAnyFileDirectoryValidator(AbstractDirectoryValidator):

    def __init__(self, filenames: Sequence[str]):
        self.filenames = filenames

    def check(self, directory: DirPath) -> bool:
        return any(os.path.isfile(os.path.join(directory, filename)) for filename in self.filenames)


class ContainAllFileDirectoryValidator(AbstractDirectoryValidator):

    def __init__(self, filenames: Sequence[str]):
        self.filenames = filenames

    def check(self, directory: DirPath) -> bool:
        return all(os.path.isfile(os.path.join(directory, filename)) for filename in self.filenames)


# --------        handlers        --------
def choose_directory(__dir: DirPath, caption: str = 'Choose Directory', parent: QtWidgets.QWidget | None = None, validator: AbstractDirectoryValidator | None = None) -> DirPath | None:
    validator = validator or NoneDirectoryValidator()

    while True:

        directory = QtWidgets.QFileDialog().getExistingDirectory(
            caption=caption,
            dir=__dir,
            parent=parent,
        )
        directory = os.sep.join(directory.split('/'))

        # cancel button is pressed
        if directory == '':
            return None

        # choosen the same directory
        if directory == __dir:
            return None

        # validate directory
        if validator.check(directory):
            return directory
