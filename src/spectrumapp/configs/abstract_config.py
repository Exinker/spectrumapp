import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Mapping


ENCODING = 'utf-8'

LOGGING_LEVEL_MAP = {
    'NOTSET': logging.NOTSET,
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'FATAL': logging.FATAL,
    'CRITICAL': logging.CRITICAL,
}
LOGGING_LEVEL = LOGGING_LEVEL_MAP.get(os.environ.get('LOGGING_LEVEL'), logging.DEBUG)


class AbstractConfig(ABC):
    """Abstract type for application's config (not GUI)."""
    FILEPATH = ''

    def __init__(self, version: str, **data):
        self.version = version  # config's version (have to be corresponded to the application's version)

        if self.__class__.FILEPATH == '':
            raise AttributeError('{name}: setup FILEPATH attribute!'.format(
                name=self.__class__.__name__,
            ))

    def update(self, /, **kwargs: Mapping[str, Any]) -> None:
        """Update config file."""

        # load data
        data = self._load()

        # update data
        for key, value in kwargs.items():
            data[key] = value

        # dump data
        self._dump(
            data=data,
        )

    @abstractmethod
    def dumps(self) -> Mapping[str, Any]:
        """Serialize config to mapping object."""
        raise NotImplementedError

    def dump(self) -> None:
        """Dump config to file (json)."""

        self._dump(
            data=self.dumps(),
        )

    @classmethod
    def default(cls) -> 'AbstractConfig':
        """Default config."""
        data = cls._default()

        return cls(**data)

    @classmethod
    @abstractmethod
    def load(cls) -> 'AbstractConfig':
        """Load config from file (json)."""

        # load data
        try:
            data = cls._load()

        except FileNotFoundError:
            raise NotImplementedError

        # parse data
        try:
            config = cls(**data)

        except (json.JSONDecodeError, TypeError, ValueError, KeyError):
            raise NotImplementedError

        #
        return config

    @classmethod
    @abstractmethod
    def _default(cls) -> Mapping[str, Any]:  # noqa: N805
        """Get default serialized data."""
        raise NotImplementedError

    @classmethod
    def _load(cls) -> Mapping[str, Any]:
        """Load serialized data."""

        with open(cls.FILEPATH, 'r', encoding=ENCODING) as file:
            data = json.load(file)

        return data

    def _dump(self, data: Mapping[str, Any]) -> None:
        """Dump serialized data."""

        with open(self.FILEPATH, 'w', encoding=ENCODING) as file:
            json.dump(data, file)
