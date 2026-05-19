import dataclasses
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, Mapping

from spectrumapp.configs import ConfigABC


LOGGER = logging.getLogger('spectrumapp')


@dataclass(frozen=True, slots=True)
class BaseConfig(ConfigABC):

    version: str
    directory: Path | None

    FILEPATH: ClassVar[str] = field(default=Path.cwd() / 'config.json')

    def dumps(self) -> Mapping[str, str | None]:
        """Serialize config to mapping object."""

        data = {}
        for key, value in dataclasses.asdict(self).items():
            data[key] = str(value) if isinstance(value, Path) else value

        return data

    def update(self, /, **kwargs: Mapping[str, Any]) -> None:
        """Update config file."""

        data = self._load()
        for key, value in kwargs.items():
            data[key] = str(value) if isinstance(value, Path) else value

        self._dump(
            data=data,
        )

    @classmethod
    def load(cls, *, version: str) -> 'BaseConfig':
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
            setdefault_config(version=version)
            return cls.load(version=version)

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
            setdefault_config(version=version)
            return cls.load(version=version)

        return config

    @classmethod
    def _default(cls, *, version: str) -> Mapping[str, str | int | float | list]:
        """Get default serialized data."""

        return {
            'version': version,
            'directory': None,
        }


def setdefault_config(version: str) -> None:
    """Create default config file."""

    config = BaseConfig.default(
        version=version,
    )
    config.dump()


if __name__ == '__main__':
    config = BaseConfig.default(
        version='0.0.0',
    )
    print(config.to_dict())
