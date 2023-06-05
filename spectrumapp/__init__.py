import os

from spectrumapp.core.exception import eprint

# ---------        env        ---------
filepath = os.path.join('.', '.env')
if os.path.isfile(filepath):

    with open(filepath, 'r') as file:
        for line in file.readlines():
            try:
                key, value = line.rstrip().split('=')
                os.environ[key] = value

            except Exception as error:
                print(f'line: {repr(line)}')
                eprint(error)

# ---------        others        ---------
__version__ = os.environ['APPLICATION_VERSION']
