import dataclasses
import json
import os
from abc import ABC, abstractclassmethod, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping

from spectrumapp.exceptions import eprint
from spectrumapp.types import DirPath, FilePath


class AbstractConfig(ABC):
    """Abstract type for application's config (not GUI)."""

    def __init__(self, version: str, filedir: DirPath, filename: str):
        self.version = version  # config's version (have to be corresponded to the application's version)

    def to_json(self, filepath: FilePath) -> None:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(self.to_dict(), file)

    @abstractmethod
    def to_dict(self) -> Mapping[str, Any]:
        raise NotImplementedError

    @classmethod
    def update(cls, key: str, value: Any, filepath: FilePath) -> None:

        # load data
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # update data
        data[key] = value

        # dump data
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    # ---------        factory        ---------
    @abstractclassmethod
    def default(cls) -> 'AbstractConfig':
        raise NotImplementedError

    @classmethod
    def from_json(cls, filepath: FilePath) -> 'AbstractConfig':

        # load data
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)

        except FileNotFoundError as error:
            eprint(msg=f'{cls.__name__}.from_json: {error}')
            config = cls.default()

        # validate data
            pass

        # parse data
        try:
            config = cls(**data)

        except (json.JSONDecodeError, TypeError, ValueError, KeyError) as error:
            eprint(msg=f'{cls.__name__}.from_json: {error}')
            config = cls.default()

        #
        return config
