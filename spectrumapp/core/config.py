
import dataclasses
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any

from .exception import eprint
from .logging import log


# ---------        CONFIG        ---------
@dataclass(frozen=True)
class Config():
    """Config of an application (not GUI)"""
    version: str  # config version (corresponds to the application's version)

    filedir: str
    filename: str | None = field(default=None)

    @property
    def filepath(self) -> str:
        if self.filename is None:
            return None

        return os.path.join(self.filedir, self.filename) 

    # ---------        handlers        ---------
    @classmethod
    def default(cls) -> 'Config':
        return Config(
            version=os.environ['APPLICATION_VERSION'],
            filedir=os.getcwd(),
        )

    def to_json(self) -> None:
        filepath = os.path.join('.', 'config.json')
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(self.to_dict(), file)

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls) -> 'Config':
        try:
            # load data
            filepath = os.path.join('.', 'config.json')
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # validate data
            pass

            # init config
            config = Config(**data)

        except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError, KeyError) as error:
            eprint(error)
            config = cls.default()

        return config

    @classmethod
    @log('update config', level=logging.INFO)
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


def setdefault_config() -> None:

    if not os.path.exists('config.json'):
        config = Config.default()
        config.to_json()
