from pathlib import Path
from typing import NewType, TypeAlias

import pandas as pd
from PySide6 import QtCore, QtWidgets
from numpy.typing import NDArray  # noqa: I100


# --------        paths        --------
DirPath: TypeAlias = str | Path
FilePath: TypeAlias = str | Path


# --------        structures        --------
Array: TypeAlias = NDArray

Index: TypeAlias = pd.Index | pd.MultiIndex
Series: TypeAlias = pd.Series
Frame: TypeAlias = pd.DataFrame


# --------        Qt types        --------
TableModel: TypeAlias = QtCore.QAbstractTableModel
TableView: TypeAlias = QtWidgets.QTableView


# --------        spacial units        --------
Inch = NewType('Inch', float)
CentiMeter = NewType('CentiMeter', float)

# --------        graph types        --------
Lim: TypeAlias = tuple[float, float]
Lims: TypeAlias = tuple[Lim, Lim]
