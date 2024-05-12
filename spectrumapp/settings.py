import json
import os
from typing import Any

from PySide6 import QtCore

from .config import BaseConfig
from .loggers import log


def load_setting() -> QtCore.QSettings:

    def inner(filepath: str) -> QtCore.QSettings:
        settings = QtCore.QSettings(filepath, QtCore.QSettings.IniFormat)
        return settings

    # fetch: setting.ini
    filedir = os.getcwd()
    filepath = os.path.join(filedir, 'settings.ini')

    return inner(filepath)


@log('settings: get')
def get_setting(key: str) -> Any:
    key_category, key_name = key.split('/')

    if key_category == 'config':
        config = BaseConfig.from_json()

        if hasattr(config, key_name):
            return getattr(config, key_name)

        raise ValueError(f'key {key} is not supported!')

    settings = load_setting()
    value = settings.value(key)
    try:
        value = json.loads(value)
    except Exception:
        pass

    return value


@log('settings: set')
def set_setting(key: str, value: str | int | float | list) -> None:
    key_category, key_name = key.split('/')

    if key_category == 'config':
        BaseConfig.update(
            key=key_name,
            value=value,
        )
        return None

    settings = load_setting()
    settings.setValue(key, value)
    settings.sync()


def setdefault_setting() -> None:

    if not os.path.exists('settings.ini'):
        settings = QtCore.QSettings('settings.ini', QtCore.QSettings.IniFormat)
        settings.sync()
