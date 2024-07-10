"""Template for an any PySide6 (PyQt6) application."""

import os

from spectrumapp.exceptions import eprint

__version__ = '0.2.2'

__author__ = 'Pavel Vaschenko'
__organization__ = 'VMK-Optoelektronika'


__name__ = 'spectrumapp'
__email__ = 'vaschenko@vmk.ru'

__license__ = 'MIT'


# ---------        env        ---------
filepath = os.path.join('.', '.env')
if os.path.isfile(filepath):

    with open(filepath, 'r') as file:
        for line in file.readlines():

            if line == '':
                continue

            try:
                key, value = line.rstrip().split('=', maxsplit=1)
                os.environ[key] = value

            except Exception:
                eprint(msg=f'env: {repr(line)}')
