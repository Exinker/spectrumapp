import matplotlib as mpl
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    RC_PARAMS = {
        'font.family': 'sans-serif',
        'font.sans-serif': 'Arial',
        'font.size': 9,

        'axes.labelsize': 9,
        'axes.linewidth': 1,
        'axes.spines.bottom': True,
        'axes.spines.left': True,
        'axes.spines.right': False,
        'axes.spines.top': False,

        'xtick.labelsize': 8,
        'xtick.major.size': 2.5,
        'xtick.major.width': 1,

        'ytick.labelsize': 8,
        'ytick.major.size': 2.5,
        'ytick.major.width': 1,
    }
    DEFAULT_SIZE = (360, 240)

    def __init__(self, tight_layout: bool = True):

        matplotlib_axes_logger.setLevel('ERROR')
        mpl.use('Qt5Agg')  # Make sure that we are using QT5
        mpl.rcParams.update(self.RC_PARAMS)

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
