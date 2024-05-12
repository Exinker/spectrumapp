from pathlib import Path
from typing import TypeAlias

from numpy.typing import NDArray
from PySide6 import QtCore


# --------        paths        --------
DirPath: TypeAlias = str | Path
FilePath: TypeAlias = str | Path


# --------        numbers        --------
Array: TypeAlias = NDArray


# --------        Qt types        --------
TableModel: TypeAlias = QtCore.QAbstractTableModel


# --------        graph types        --------
Lims: TypeAlias = tuple[tuple[float, float], tuple[float, float]]
