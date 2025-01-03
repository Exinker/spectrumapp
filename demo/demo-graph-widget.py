import sys
from dataclasses import dataclass
from typing import Any, Mapping

import numpy as np
from matplotlib.backend_bases import PickEvent
from matplotlib.widgets import RectangleSelector
from PySide6 import QtWidgets  # noqa: I100

from spectrumapp.types import Array
from spectrumapp.widgets.graphWidget import BaseGraphWidget


@dataclass
class MyDatum:
    x: Array[float]
    y: Array[float]


class MyGraphWidget(BaseGraphWidget):

    def __init__(self, *args, size: tuple[int, int] = (640, 480), tight_layout: bool = True, **kwargs):
        super().__init__(*args, size=size, tight_layout=tight_layout, **kwargs)

    def _pick_event(self, event: PickEvent) -> None:

        if event.mouseevent.button == 1:

            # fetch index
            ind = event.ind

            if len(ind) == 1:
                ind = ind[0]
            else:
                return

            # update annotate
            label = event.artist.get_label()
            datum = self._data['y_hat']

            x, y = datum.x[ind], datum.y[ind]
            text = '\n'.join([
                fr'{ind:<8} ({label})',
                fr'x={x:.4f}',
                fr'y={y:.4f}',
            ])
            self.annotate.set_text(text)

            x, y = event.artist.get_offsets()[ind]
            ylim = self.canvas.axes.get_ylim()
            yrange = (max(ylim) - min(ylim))
            self.annotate.set_position((
                x,
                y + yrange/40,
            ))

            # color = event.artist.get_facecolors()[0]
            color = 'black'
            self.annotate.set_color(color)
            self.annotate.set_ha('center')
            self.annotate.set_visible(True)

            #
            self.canvas.draw()

    def _set_full_lims(self, data: Mapping[str, MyDatum]):
        xlim = (min(data['y'].x), max(data['y'].x))
        ylim = (min(data['y'].y), max(data['y'].y))
        lims = xlim, ylim

        self._full_lims = lims

    def update(self, data: Mapping[str, MyDatum] = None, pattern: Mapping[str, Any] | None = None) -> None:
        """Update graph's data."""

        if data is None:
            self.canvas.axes.clear()
            self.canvas.draw_idle()

            return None

        # update data
        self._data = data

        # update labels
        self._labels = {
            'y': r'$y$',
            'y_hat': r'$\hat{y}$',
        }

        # update full lims
        self._set_full_lims(data)

        # update graphs
        self.canvas.axes.clear()

        # draw data
        for key, datum in data.items():
            x, y = datum.x, datum.y
            label = self._labels.get(key, '')

            if key == 'y':
                self.canvas.axes.plot(
                    x, y,
                    color='black', linestyle='-', linewidth=1,
                    label=label,
                    picker=True,
                )
            if key == 'y_hat':
                self.canvas.axes.scatter(
                    x, y,
                    color='red',
                    label=label,
                    picker=True,
                )

        # draw annotate
        self.annotate = self.canvas.axes.text(
            x=0, y=0,
            s='',
            fontdict=dict(
                size=8,
                ha='left',
            ),
        )
        self.annotate.set_visible(False)

        # draw zoom line
        self.zoom_line = RectangleSelector(
            self.canvas.axes,
            lambda a, b: print('RectangleSelector callback'),
            useblit=True,
            props={
                'facecolor': None,
                'edgecolor': 'grey',
                'linestyle': ':',
                'alpha': 1,
                'fill': False,
            },
            button=[3],
            spancoords='pixels',
            minspanx=10, minspany=10,
            interactive=False,
        )

        # set lims
        lims = self._crop_lims if self._crop_lims else self._full_lims
        xlim, ylim = lims
        self.canvas.axes.set_xlim(xlim)
        self.canvas.axes.set_ylim(ylim)

        # set axes
        self.canvas.axes.set_xlabel(self._params['xlabel'])
        self.canvas.axes.set_ylabel(self._params['ylabel'])

        self.canvas.axes.legend()
        self.canvas.axes.grid(
            color='black', linestyle=':',
        )

        self.canvas.draw_idle()


if __name__ == '__main__':
    n_points = 100

    x = np.linspace(-2*np.pi, +2*np.pi, n_points)
    y = np.sin(x)
    y_hat = y + 0.1*np.random.randn(n_points)
    data = dict(y=MyDatum(x=x, y=y), y_hat=MyDatum(x=x, y=y_hat))

    #
    app = QtWidgets.QApplication()

    window = MyGraphWidget(
        objectName='myGraphWidget',
    )
    window.update(
        data=data,
    )
    window.show()

    sys.exit(app.exec())
