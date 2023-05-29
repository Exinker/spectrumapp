
import dataclasses
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any

from .exceptions import eprint
from .loggings import log
from .utils import pave


# ---------        env        ---------
filepath = pave(os.path.join('.', '.env'))
if os.path.isfile(filepath):

    with open(filepath, 'r') as file:
        for line in file.readlines():
            try:
                key, value = line.rstrip().split('=')
                os.environ[key] = value

            except Exception as error:
                eprint(error)


# ---------        CONTACTS        ---------
APPLICATION_NAME = 'Spectrum'
APPLICATION_DESCRIPTION = """Example of a simple PySide6 (PyQt5) application."""
APPLICATION_VERSION = '0.0.1'

AUTHOR_NAME = 'Pavel Vaschenko'
AUTHOR_EMAIL = 'vaschenko@vmk.ru'

ORGANIZATION_NAME = 'VMK-Optoelektronika'


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
            version=APPLICATION_VERSION,
            filedir=os.getcwd(),
        )

    def to_json(self) -> None:
        filepath = pave(os.path.join('.', 'config.json'))
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(self.to_dict(), file)

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls) -> 'Config':
        try:
            # load data
            filepath = pave(os.path.join('.', 'config.json'))
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
        filepath = pave(os.path.join('.', 'config.json'))
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
