import logging
import logging.config
import os

from spectrumapp.config import LOGGING_LEVEL


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
