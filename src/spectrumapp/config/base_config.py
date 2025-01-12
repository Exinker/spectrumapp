import dataclasses
import json
import logging
import os
from dataclasses import dataclass, field
from typing import ClassVar, Mapping

from spectrumapp.config import AbstractConfig
from spectrumapp.types import DirPath


LOGGER = logging.getLogger('spectrumapp')


@dataclass(frozen=True, slots=True)
class BaseConfig(AbstractConfig):
    version: str
    directory: DirPath

    FILEPATH: ClassVar[str] = field(default=os.path.join(os.getcwd(), 'config.json'))

    def dumps(self) -> Mapping[str, str]:
        """Serialize config to mapping object."""

        data = {}
        for key, value in dataclasses.asdict(self).items():
            data[key] = value

        return data

    @classmethod
    def load(cls) -> 'BaseConfig':
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
            setdefault_config()
            return cls.load()

        try:
            config = cls(
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
            setdefault_config()
            return cls.load()

        return config

    @classmethod
    def _default(cls) -> Mapping[str, str | int | float | list]:
        """Get default serialized data."""

        return {
            'version': os.environ['APPLICATION_VERSION'],
            'directory': '',
        }


def setdefault_config() -> None:
    """Create default config file."""

    config = BaseConfig.default()
    config.dump()


if __name__ == '__main__':
    os.environ['APPLICATION_VERSION'] = '0'

    config = BaseConfig.default()
    print(config.to_dict())
