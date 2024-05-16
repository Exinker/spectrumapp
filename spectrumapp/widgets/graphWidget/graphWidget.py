from typing import Any, Mapping, TypeAlias

from matplotlib.backend_bases import KeyEvent, MouseEvent, PickEvent
from PySide6 import QtCore, QtWidgets

from spectrumapp.types import Lims
from spectrumapp.utils.getter import getdefault_object_name

from .canvas import MplCanvas


Data: TypeAlias = Any


class BaseGraphWidget(QtWidgets.QWidget):
    """
    Base class for graph widgets.

    Events:
        reset zoom and pan - double click of rigth mouse button;
        update pan - left mouse button with shift modifier;
        update zoom - right mouse button;
    """

    def __init__(self, *args, object_name: str | None = None, size: tuple[int, int] = (640, 480), tight_layout: bool = True, **kwargs):
        super().__init__(*args, **kwargs)

        # object name
        object_name = object_name or getdefault_object_name(self)
        self.setObjectName(object_name)

        #
        self._data: Data | None = None
        self._labels: Mapping[str, str] = {}
        self._params = {
            'xlabel': None,
            'ylabel': None,
        }
        self.annotate = None
        self.zoom_line = None

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
        self._size = size
        self.setFixedSize(*self._size)

        #
        self.show()

    def sizeHint(self):
        return QtCore.QSize(*self._size)

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
            (event.xdata for event in (press_event, release_event)),
        ))
        ylim = tuple(sorted(
            (event.ydata for event in (press_event, release_event)),
        ))
        lims = xlim, ylim

        # set crop lims
        self._crop_lims = lims

        # update zoom
        self._update_zoom(
            lims=self._crop_lims,
        )

    def _pan_event(self, press_event: MouseEvent, release_event: MouseEvent) -> None:
        xlim, ylim = self.canvas.axes.get_xlim(), self.canvas.axes.get_ylim()
        xshift, yshift = release_event.xdata - press_event.xdata, release_event.ydata - press_event.ydata
        lims = (
            [value - xshift for value in xlim],
            [value - yshift for value in ylim],
        )

        # update crop lims
        self._crop_lims = lims

        # update zoom
        self._update_zoom(
            lims=self._crop_lims,
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
