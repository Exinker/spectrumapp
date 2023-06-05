
import json
import os
from typing import Any

from PySide6 import QtCore, QtGui, QtWidgets

from .config import Config
from .logging import log


# ---------        settings        ---------
def fetch_setting() -> QtCore.QSettings:

    def inner(filepath: str) -> QtCore.QSettings:
        settings = QtCore.QSettings(filepath, QtCore.QSettings.IniFormat)
        return settings

    # fetch: setting.ini
    filedir = os.getcwd()
    filepath = os.path.join(filedir, 'setting.ini')

    return inner(filepath)


@log('get setting')
def get_setting(key: str) -> Any:
    key_category, key_name = key.split('/')

    if key_category == 'config':
        config = Config.from_json()

        if hasattr(config, key_name):
            return getattr(config, key_name)

        raise ValueError(f'key {key} is not supported!')

    settings = fetch_setting()
    value = settings.value(key)
    try:
        value = json.loads(value)
    finally:
        return value


@log('set setting')
def set_setting(key: str, value: str | int | float | list) -> None:
    key_category, key_name = key.split('/')

    if key_category == 'config':
        Config.update(
            key=key_name,
            value=value,
        )
        return None

    settings = fetch_setting()
    settings.setValue(key, value)
    settings.sync()


def setdefault_setting() -> None:

    if not os.path.exists('setting.ini'):
        settings = QtCore.QSettings('setting.ini', QtCore.QSettings.IniFormat)
        settings.sync()
