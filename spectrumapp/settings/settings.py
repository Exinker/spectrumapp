import json
import logging
import os
from typing import Any

from PySide6 import QtCore

from spectrumapp.loggers import log
from spectrumapp.types import DirPath


def load_settings(filedir: DirPath | None = None) -> QtCore.QSettings:
    """Load settings (GUI only) object from `settings.ini` file."""
    filedir = filedir or os.getcwd()

    filepath = os.path.join(filedir, 'settings.ini')
    return QtCore.QSettings(filepath, QtCore.QSettings.IniFormat)


@log('settings: get', level=logging.NOTSET)
def get_setting(key: str) -> Any:
    """Get setting by key from `settings.ini` file."""
    settings = load_settings()
    value = settings.value(key)

    try:
        return json.loads(value)
    except Exception:
        return value


@log('settings: set')
def set_setting(key: str, value: str | int | float | list) -> None:
    """Set setting by key to `settings.ini` file."""

    settings = load_settings()
    settings.setValue(key, value)
    settings.sync()
