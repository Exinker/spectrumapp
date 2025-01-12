import os
import sys


def pave(__relative_path: str) -> str:
    """Pave the absolute path of relative (regardless of running in develop or deploy)."""

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, __relative_path)

    return os.path.abspath(__relative_path)
