
import sys
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, TypeAlias

import numpy as np
from numpy.typing import NDArray

from matplotlib.widgets import RectangleSelector
from matplotlib.backend_bases import MouseEvent, KeyEvent, PickEvent

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.widget.canvas import MplCanvas


Data: TypeAlias = Any
Array: TypeAlias = NDArray
Lims: TypeAlias = tuple[tuple[float, float], tuple[float, float]]


# ----------------    Graph Widget    ----------------
class BaseGraphWidget(QtWidgets.QWidget):
    """
    Base class for graph widgets.

    Events:
        reset zoom and pan - double click of rigth mouse button;
        update pan - left mouse button with shift modifier;
        update zoom - right mouse button;
    """

    def __init__(self, *args, name: str, size: tuple[int, int] = (640, 480), tight_layout: bool = True, **kwargs):
        super().__init__(*args, **kwargs)

        self._size = size

        #
        self._data: Data | None = None
        self._labels: Mapping[str, str] = {}
        self._params = {
            'xlabel': None,
            'ylabel': None,
        }
        self.annotate = None
        self.zoom_line = None

        # 
        self.setObjectName(name)

        # focus
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()

        # pressed mouse and keys events
        self._pressed_event: MouseEvent | None = None
        self._pressed_shift = False  # shift event modifier
        self._pressed_ctrl = False  # ctrl event modifier

        # graph limits
        self._default_lims: Lims = ((0, 1), (0, 1))
        self._full_lims: Lims | None = None
        self._crop_lims: Lims | None = None

        # layout and canvas
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.canvas = MplCanvas(tight_layout=tight_layout)
        self.canvas.mpl_connect('pick_event', self._pick_event)
        self.canvas.mpl_connect('button_press_event', self._button_press_event)
        self.canvas.mpl_connect('button_release_event', self._button_release_event)
        self.canvas.mpl_connect('motion_notify_event', self._motion_notify_event)
        layout.addWidget(self.canvas)

        # geometry
        width, height = self._size
        self.setFixedSize(width, height)

        #
        self.show()

    def sizeHint(self):
        width, height = self._size
        return QtCore.QSize(width, height)

    def keyPressEvent(self, event: KeyEvent):

        if event.key() == QtCore.Qt.Key_Control:
            self._pressed_ctrl = True
        if event.key() == QtCore.Qt.Key_Shift:
            self._pressed_shift = True

    def keyReleaseEvent(self, event: KeyEvent):

        if event.key() == QtCore.Qt.Key_Control:
            self._pressed_ctrl = False
        if event.key() == QtCore.Qt.Key_Shift:
            self._pressed_shift = False

    # --------        handlers        --------
    def _pick_event(self, event: PickEvent) -> None:
        raise NotImplementedError

    def _button_press_event(self, event: MouseEvent):
        self._pressed_event = event


        # update zoom and pan
        if self._pressed_ctrl and self._pressed_shift:
            pass

        elif self._pressed_ctrl:
            pass

        elif self._pressed_shift:
            pass

        else:
            if event.button == 3 and event.dblclick:
                self._pressed_event = None
                self._crop_lims = None
                self._update_zoom(lims=self._full_lims)

    def _button_release_event(self, event: MouseEvent):

        # update annotate
        self.annotate.set_visible(False)
        self.canvas.draw_idle()

        # update zoom and pan
        if self._pressed_ctrl and self._pressed_shift:
            pass

        elif self._pressed_ctrl:
            pass

        elif self._pressed_shift:
            if event.button == 1:
                self._pan_event(
                    self._pressed_event,
                    event,
                )

        else:
            if event.button == 3:
                self._zoom_event(
                    self._pressed_event,
                    event,
                )

    def _motion_notify_event(self, event: MouseEvent):

        # update zoom and pan
        if self._pressed_ctrl and self._pressed_shift:
            pass

        elif self._pressed_ctrl:
            pass

        elif self._pressed_shift:
            if event.button == 1:
                self._pan_event(
                    self._pressed_event,
                    event,
                )

        else:
            pass

    def _zoom_event(self, press_event: MouseEvent, release_event: MouseEvent) -> None:
        xlim = tuple(sorted(
            (event.xdata for event in (press_event, release_event))
        ))
        ylim = tuple(sorted(
            (event.ydata for event in (press_event, release_event))
        ))
        lims = xlim, ylim

        # set crop lims
        self._crop_lims = lims

        # update zoom
        self._update_zoom(
            lims=self._crop_lims
        )

    def _pan_event(self, press_event: MouseEvent, release_event: MouseEvent) -> None:
        xlim, ylim = self.canvas.axes.get_xlim(), self.canvas.axes.get_ylim()
        xshift, yshift = release_event.xdata - press_event.xdata, release_event.ydata - press_event.ydata
        lims=(
            [value - xshift for value in xlim],
            [value - yshift for value in ylim],
        )

        # update crop lims
        self._crop_lims = lims

        # update zoom
        self._update_zoom(
            lims=self._crop_lims
        )

    def _set_full_lims(self, data: Data) -> None:
        raise NotImplementedError

    def _set_crop_lims(self, lims: Lims) -> None:
        self._crop_lims = lims

    def _update_zoom(self, lims: Lims | None = None) -> None:
        if lims is None:
            lims = self._full_lims if self._full_lims else self._default_lims

        xlim, ylim = lims

        #
        self.canvas.axes.set_xlim(xlim)
        self.canvas.axes.set_ylim(ylim)
        self.canvas.draw_idle()

    # --------        handlers        --------
    def update(self, data: Data | None = None, pattern: Mapping[str, Any] | None = None) -> None:
        """Update graph's data."""
        raise NotImplementedError

    def filtrate(self, pattern: Mapping[str, Any] | None = None):
        """Filtrate graph's data with given pattern."""
        self._update(pattern=pattern)


if __name__ == '__main__':
    from dataclasses import dataclass


    @dataclass
    class MyDatum:
        x: Array[float]
        y: Array[float]


    class MyData(dict):
        pass


    class MyGraphWidget(BaseGraphWidget):

        def __init__(self, *args, name: str, size: tuple[int, int] = (640, 480), tight_layout: bool = True, **kwargs):
            super().__init__(*args, name=name, size=size, tight_layout=tight_layout, **kwargs)

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
            xlim = tuple(
                [min(data['y'].x), max(data['y'].x)]
            )
            ylim = tuple(
                [min(data['y'].y), max(data['y'].y)]
            )
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


    #
    n_points = 100

    x = np.linspace(-2*np.pi, +2*np.pi, n_points)
    y = np.sin(x)
    y_hat = y + 0.1*np.random.randn(n_points,)
    data = MyData(y=MyDatum(x=x, y=y), y_hat=MyDatum(x=x, y=y_hat))

    #
    app = QtWidgets.QApplication()

    window = MyGraphWidget(
        name='my_graph',
    )
    window.update(
        data=data,
    )
    window.show()

    sys.exit(app.exec())
