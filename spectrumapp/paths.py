import os
import sys
from importlib import resources

import spectrumapp


LIBDIR = resources.files(spectrumapp)


def pave(relative_path: str) -> str:
    """Pave the absolute path of relative (regardless of running in develop or deploy)."""

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.abspath(relative_path)
