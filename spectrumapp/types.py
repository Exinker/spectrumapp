from enum import Enum
from pathlib import Path
from typing import NewType, TypeAlias

from numpy.typing import NDArray  # noqa: I100
import pandas as pd
from PySide6 import QtCore, QtWidgets

from spectrumapp.colors import COLOR_DATASET, Color


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


# --------        datasets        --------
class Dataset(Enum):
    train = 'train'
    valid = 'valid'
    test = 'test'

    @property
    def color(self) -> Color:
        return COLOR_DATASET[self.name]


# --------        spacial units        --------
Inch = NewType('Inch', float)
CentiMeter = NewType('CentiMeter', float)

# --------        graph types        --------
Lim: TypeAlias = tuple[float, float]
Lims: TypeAlias = tuple[Lim, Lim]
