import os

from spectrumapp.core.config import APPLICATION_VERSION
from spectrumapp.core.exception import eprint


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

# ---------        others        ---------
__version__ = APPLICATION_VERSION
