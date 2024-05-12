import dataclasses
import json
import os
from abc import ABC, abstractclassmethod, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Mapping

from spectrumapp.exceptions import eprint
from spectrumapp.types import DirPath, FilePath


class AbstractConfig(ABC):
    """Abstract type for application's config (not GUI)"""

    def __init__(self, version: str, filedir: DirPath | None = None, filename: str | None = None):
        self.version = version  # config version (have to be corresponded to the application's version)
        self.filedir = filedir or os.getcwd()
        self.filename = filename or 'config.json'

    @property
    def filepath(self) -> str:
        return os.path.join(self.filedir, self.filename)

    # ---------        handlers        ---------
    def to_json(self, filepath: FilePath | None = None) -> None:
        filepath = filepath or os.path.join('.', 'config.json')

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(self.to_dict(), file)

    @abstractmethod
    def to_dict(self) -> Mapping[str, Any]:
        raise NotImplementedError

    # ---------        factory        ---------
    @abstractclassmethod
    def default(cls) -> 'AbstractConfig':
        raise NotImplementedError

    @classmethod
    def from_json(cls, filepath: FilePath | None = None) -> 'AbstractConfig':
        filepath = filepath or os.path.join('.', 'config.json')

        try:

            # load data
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # validate data
            pass

            # init config
            config = cls(**data)

        except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError, KeyError) as error:
            eprint(msg=f'{cls.__name__}.from_json: {error}')
            config = cls.default()

        return config

    @classmethod
    def update(cls, key: str, value: Any, filepath: str | None = None) -> None:

        # load data
        filepath = os.path.join('.', 'config.json')
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # update data
        data[key] = value

        # dump data
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file)


@dataclass(frozen=True, slots=True)
class BaseConfig(AbstractConfig):
    version: str
    filedir: DirPath | None = field(default=None)
    filename: str | None = field(default=None)

    # ---------        handlers        ---------
    def to_dict(self) -> Mapping[str, Any]:
        return dataclasses.asdict(self)

    # ---------        factory        ---------
    @classmethod
    def default(cls) -> 'BaseConfig':
        return cls(
            version=os.environ['APPLICATION_VERSION'],
        )


def setdefault_config(cls: type[AbstractConfig]) -> None:

    if not os.path.exists('config.json'):
        config = cls.default()
        config.to_json()
