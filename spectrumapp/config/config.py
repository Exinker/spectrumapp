import json
from abc import ABC, abstractclassmethod, abstractmethod
from typing import Mapping


ENCODING = 'utf-8'


class AbstractConfig(ABC):
    """Abstract type for application's config (not GUI)."""
    FILEPATH = ''

    def __init__(self, version: str, **data):
        self.version = version  # config's version (have to be corresponded to the application's version)

        if self.__class__.FILEPATH == '':
            raise AttributeError('{name}: setup FILEPATH attribute!'.format(
                name=self.__class__.__name__,
            ))

    def dump(self) -> None:
        """Dump config to file (json)."""

        self._dump(
            data=self.serialize(),
        )

    @abstractmethod
    def serialize(self) -> Mapping[str, str | int | float | list]:
        """Serialize config to mapping object."""
        raise NotImplementedError

    # ---------        factory        ---------
    @classmethod
    def default(cls) -> 'AbstractConfig':
        """Default config."""
        data = cls._default()

        return cls(**data)

    @classmethod
    def update(cls, **kwargs: Mapping[str, str | int | float | list]) -> None:
        """Update config file."""

        # load data
        data = cls._load()

        # update data
        for key, value in kwargs.items():
            data[key] = value

        # dump data
        cls._dump(
            data=data,
        )

    @classmethod
    @abstractclassmethod
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

    # ---------        private        ---------
    @classmethod
    @abstractclassmethod
    def _default(cls) -> Mapping[str, str | int | float | list]:  # noqa: N805
        """Get default serialized data."""
        raise NotImplementedError

    @classmethod
    def _load(cls) -> Mapping[str, str | int | float | list]:
        """Load serialized data."""
        filepath = cls.FILEPATH

        with open(filepath, 'r', encoding=ENCODING) as file:
            data = json.load(file)

        return data

    @classmethod
    def _dump(cls, data: Mapping[str, str | int | float | list]) -> None:
        """Dump serialized data."""
        filepath = cls.FILEPATH

        with open(filepath, 'w', encoding=ENCODING) as file:
            json.dump(data, file)
