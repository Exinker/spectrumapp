import dataclasses
import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Mapping

from spectrumapp.config import AbstractConfig
from spectrumapp.exceptions import eprint
from spectrumapp.types import DirPath


@dataclass(frozen=True, slots=True)
class File(AbstractConfig):
    version: str
    directory: DirPath

    FILEPATH: ClassVar[str] = field(default=os.path.join(os.getcwd(), 'config.json'))

    def serialize(self) -> Mapping[str, str | int | float | list]:
        """Serialize config to mapping object."""

        data = {}
        for key, value in dataclasses.asdict(self).items():
            if isinstance(value, Enum):
                value = value.value

            data[key] = value

        #
        return data

    # ---------        factory        ---------
    @classmethod
    def default(cls) -> 'File':
        """Get config file by default."""

        config = cls(
            **cls._default(),
        )

        #
        return config

    @classmethod
    def load(cls) -> 'File':
        """Load config from file (json)."""

        # load data
        try:
            data = cls._load()

        except FileNotFoundError as error:
            eprint(msg=f'{cls.__name__}.load: {error}')

            setdefault_config()
            return cls.load()

        # parse data
        try:
            config = File(
                version=data['version'],
                directory=data['directory'],
            )

        except (json.JSONDecodeError, TypeError, ValueError, KeyError) as error:
            eprint(msg=f'{cls.__name__}.load: {error}')

            setdefault_config(force=True)
            return cls.load()

        #
        return config

    # ---------        private        ---------
    @classmethod
    def _default(cls) -> Mapping[str, str | int | float | list]:
        """Get default serialized data."""

        return {
            'version': os.environ['APPLICATION_VERSION'],
            'directory': '',
        }


def setdefault_config(force: bool = False) -> None:
    """Create default config file."""

    filepath = File.FILEPATH
    if (not os.path.exists(filepath)) or force:
        config = File.default()
        config.dump()


if __name__ == '__main__':
    os.environ['APPLICATION_VERSION'] = '0'

    file = File.default()
    print(file.to_dict())
