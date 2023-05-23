
import dataclasses
import json
import os
from dataclasses import dataclass, field
from typing import Any

from .exceptions import eprint
from .routing import pave


DEBUG = True

# ---------        CONTACTS        ---------
APPLICATION_NAME = 'Spectrum'
APPLICATION_DESCRIPTION = '''Example of a simple PySide6 (PyQt5) application.'''
APPLICATION_VERSION = '0.0.1'

AUTHOR_NAME = 'Pavel Vaschenko'
AUTHOR_EMAIL = 'vaschenko@vmk.ru'

ORGANIZATION_NAME = 'VMK-Optoelektronika'


# ---------        CONFIG        ---------
@dataclass(frozen=True)
class Config():
    '''Config of an application (not GUI)'''
    version: str  # config version (corresponds to the application's version)

    filedir: str
    filename: str | None = field(default=None)

    @property
    def filepath(self) -> str | None:
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
        data = dataclasses.asdict(self)

        filepath = pave(os.path.join('.', 'config.json'))
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file)

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
