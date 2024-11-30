import matplotlib
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self, tight_layout: bool = True):

        matplotlib_axes_logger.setLevel('ERROR')
        matplotlib.use('Qt5Agg')  # Make sure that we are using QT5

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
