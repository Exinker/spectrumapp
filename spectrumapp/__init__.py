__version__ = '0.2.2'


import os

from spectrumapp.exceptions import eprint


# ---------        meta        ---------
NAME = 'spectrumapp'
DESCRIPTION = """Template for an any PySide6 (PyQt6) application."""
VERSION = __version__

AUTHOR_NAME = 'Pavel Vaschenko'
AUTHOR_EMAIL = 'vaschenko@vmk.ru'

ORGANIZATION_NAME = 'VMK-Optoelektronika'


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
