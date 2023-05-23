'''
TODO:
    - add logging of eprint
'''

import sys
import traceback


def eprint(error: Exception) -> None:
    '''Print exception traceback to stdout.'''
    traceback.print_exception(error, limit=2, file=sys.stdout)
