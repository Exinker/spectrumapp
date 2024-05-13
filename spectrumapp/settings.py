import json
import os
from typing import Any

from PySide6 import QtCore

from .loggers import log


def load_settings() -> QtCore.QSettings:
    """Load settings object from .ini file."""

    def load(__filepath: str) -> QtCore.QSettings:
        return QtCore.QSettings(__filepath, QtCore.QSettings.IniFormat)

    # load settings from <root>
    filepath = os.path.join(os.getcwd(), 'settings.ini')
    settings = load(filepath)

    #
    return settings


@log('settings: get')
def get_setting(key: str) -> Any:
    """Get setting by key."""
    key_category, key_name = key.split('/')

    # load data
    settings = load_settings()
    value = settings.value(key)

    # parse data
    try:
        value = json.loads(value)
    except Exception:
        pass

    #
    return value


@log('settings: set')
def set_setting(key: str, value: str | int | float | list) -> None:
    """Set setting by key."""

    # update settings
    settings = load_settings()
    settings.setValue(key, value)
    settings.sync()


def setdefault_setting() -> None:

    # setdefault <root> settings
    filepath = os.path.join(os.getcwd(), 'settings.ini')
    if not os.path.exists(filepath):
        settings = QtCore.QSettings(filepath, QtCore.QSettings.IniFormat)
        settings.sync()
