from collections.abc import Mapping
from typing import Any

import matplotlib as mpl
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


matplotlib_axes_logger.setLevel('ERROR')


class MplCanvas(FigureCanvas):

    DEFAULT_RC_PARAMS = {
        'font.family': 'sans-serif',
        'font.sans-serif': [
            'Segoe UI',
            'Microsoft Sans Serif',
            'MS Sans Serif',
            'Arial',
            'DejaVu Sans',
        ],
        'font.size': 9,
        'font.weight': '300',

        'figure.facecolor': '#FDFDFD',

        'axes.facecolor': '#FDFDFD',
        'axes.labelsize': 9,
        'axes.linewidth': 1,
        'axes.spines.bottom': True,
        'axes.spines.left': True,
        'axes.spines.right': False,
        'axes.spines.top': False,

        'xtick.labelsize': 9,
        'xtick.major.size': 3,
        'xtick.major.width': 1,

        'ytick.labelsize': 9,
        'ytick.major.size': 3,
        'ytick.major.width': 1,
    }
    DEFAULT_SIZE = (360, 240)

    def __init__(
        self,
        rc_params: Mapping[str, Any] | None = None,
        tight_layout: bool = True,
    ):
        rc_params = rc_params or {}

        mpl.use('Qt5Agg')  # Make sure that we are using QT5

        params = self.DEFAULT_RC_PARAMS
        params.update(**rc_params)
        mpl.rcParams.update(params)

        self.fig = Figure()
        self.fig.set_tight_layout(tight_layout)
        self.fig.subplots_adjust(
            bottom=.12,
            top=.95,
            left=.12,
            right=.95,
        )

        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
