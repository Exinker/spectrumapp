import logging
import logging.config
import os

from PySide6 import QtCore

import spectrumapp
from spectrumapp.configs import LOGGING_LEVEL


def setdefault_environ() -> None:
    os.environ['APPLICATION_NAME'] = 'Demo'
    os.environ['APPLICATION_VERSION'] = spectrumapp.__version__
    os.environ['ORGANIZATION_NAME'] = spectrumapp.__organization__


def setdefault_logger():

    config = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'file_formatter': {
                'format': '[%(asctime)s.%(msecs)04d] %(levelname)-8s %(module)s - %(message)s',
            },
            'progress_window_formatter': {
                'format': '%(message)s',
            },
        },

        'handlers': {
            'file_handler': {
                'class': 'logging.FileHandler',
                'level': logging.NOTSET,
                'filename': os.path.join('.', 'app.log'),
                'mode': 'a',
                'formatter': 'file_formatter',
                'encoding': 'utf-8',
            },
            'stream_handler': {
                'class': 'logging.StreamHandler',
                'level': logging.NOTSET,
                'formatter': 'file_formatter',
            },
        },

        'loggers': {
            'spectrumapp': {
                'level': LOGGING_LEVEL,
                'handlers': [
                    'file_handler',
                    'stream_handler',
                ],
                'propagate': False,
            },
        },
    }
    logging.config.dictConfig(config)


def setdefault_setting() -> None:

    filepath = os.path.join(os.getcwd(), 'settings.ini')
    if not os.path.exists(filepath):
        settings = QtCore.QSettings(filepath, QtCore.QSettings.IniFormat)
        settings.sync()
