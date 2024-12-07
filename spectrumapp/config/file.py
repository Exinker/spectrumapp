import dataclasses
import json
import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Mapping

from spectrumapp.config import AbstractConfig
from spectrumapp.types import DirPath


LOGGER = logging.getLogger('spectrumapp')


@dataclass(frozen=True, slots=True)
class File(AbstractConfig):
    version: str
    directory: DirPath

    FILEPATH: ClassVar[str] = field(default=os.path.join(os.getcwd(), 'config.json'))

    def dumps(self) -> Mapping[str, str | int | float | list]:
        """Serialize config to mapping object."""

        data = {}
        for key, value in dataclasses.asdict(self).items():
            if isinstance(value, Enum):
                value = value.value
            data[key] = value

        return data

    @classmethod
    def load(cls) -> 'File':
        """Load config from file (json)."""

        try:
            data = cls._load()
        except (
            FileNotFoundError,
            PermissionError,
        ) as error:
            LOGGER.warning(
                'Loading %s is failed!', cls.FILEPATH,
                extra=dict(
                    error=error,
                ),
            )
            setdefault_file()
            return cls.load()

        try:
            config = File(
                version=data['version'],
                directory=data['directory'],
            )
        except (json.JSONDecodeError, TypeError, ValueError, KeyError) as error:
            LOGGER.warning(
                'Parsing %s is failed!', cls.FILEPATH,
                extra=dict(
                    error=error,
                ),
            )
            setdefault_file()
            return cls.load()

        return config

    @classmethod
    def _default(cls) -> Mapping[str, str | int | float | list]:
        """Get default serialized data."""

        return {
            'version': os.environ['APPLICATION_VERSION'],
            'directory': '',
        }


def setdefault_file() -> None:
    """Create default config file."""

    config = File.default()
    config.dump()


if __name__ == '__main__':
    os.environ['APPLICATION_VERSION'] = '0'

    config = File.default()
    print(config.to_dict())
