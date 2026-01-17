import dataclasses
import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Mapping

from spectrumapp.config import AbstractConfig


LOGGER = logging.getLogger('spectrumapp')


@dataclass(frozen=True, slots=True)
class BaseConfig(AbstractConfig):

    version: str
    directory: Path | None

    FILEPATH: ClassVar[str] = field(default=Path.cwd() / 'config.json')

    def dumps(self) -> Mapping[str, str]:
        """Serialize config to mapping object."""

        data = {}
        for key, value in dataclasses.asdict(self).items():

            if value is None:
                continue
            data[key] = value

        return data

    @classmethod
    def load(cls) -> 'BaseConfig':
        """Load config from json file."""

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
            directory = data.get('directory', None)
            config = cls(
                version=data['version'],
                directory=Path(directory) if directory else None,
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
            'directory': None,
        }


def setdefault_config() -> None:
    """Create default config file."""

    config = BaseConfig.default()
    config.dump()


if __name__ == '__main__':
    os.environ['APPLICATION_VERSION'] = '0'

    config = BaseConfig.default()
    print(config.to_dict())
