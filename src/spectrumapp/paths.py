import os
import sys
from pathlib import Path


def pave(__relative_path: str) -> Path:
    """Pave the absolute path of relative (regardless of running in develop or deploy)."""

    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / __relative_path

    root_path = os.environ.get('PLUGIN_ROOT')
    if root_path:
        return Path(root_path) / __relative_path

    return Path(__relative_path).resolve()


def static_path(*parts: str) -> Path:
    return pave(os.path.join('.', 'static', *parts))
