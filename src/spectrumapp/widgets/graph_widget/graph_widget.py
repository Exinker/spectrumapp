from typing import Any, Mapping, TypeAlias

from PySide6 import QtCore, QtWidgets
from matplotlib.backend_bases import KeyEvent, MouseEvent, PickEvent

from spectrumapp.helpers import getdefault_object_name
from spectrumapp.types import Lims
from spectrumapp.widgets.graph_widget.canvas import MplCanvas


Data: TypeAlias = Any


DEFAULT_SIZE = QtCore.QSize(640, 480)
DEFAULT_LIMS = ((0, 1), (0, 1))


class BaseGraphWidget(QtWidgets.QWidget):
    """Base class for graph widgets.

    Events:
        reset zoom and pan - double click of rigth mouse button;
        update pan - left mouse button with shift modifier;
        update zoom - right mouse button;
    """

    def __init__(
        self,
        *args,
        object_name: str | None = None,
        size: QtCore.QSize = DEFAULT_SIZE,
        tight_layout: bool = True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._data: Data | None = None
        self._labels: Mapping[str, str] = {}
        self._params = {
            'xlabel': None,
            'ylabel': None,
        }
        self._size = size

        self.annotate = None
        self.zoom_line = None

        # object name
        object_name = object_name or getdefault_object_name(self)
        self.setObjectName(object_name)

        # focus
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()

        # pressed mouse and keys events
        self._mouse_event: MouseEvent | None = None
        self._ctrl_modified = False
        self._shift_modified = False

        # graph limits
        self._default_lims = DEFAULT_LIMS
        self._full_lims = None
        self._crop_lims = None

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
        self.setFixedSize(self._size)

    def sizeHint(self) -> QtCore.QSize:  # noqa: N802
        return self._size

    def keyPressEvent(self, event: KeyEvent) -> None:  # noqa: N802

        match event.key():
            case QtCore.Qt.Key.Key_Control:
                self._ctrl_modified = True
            case QtCore.Qt.Key.Key_Shift:
                self._shift_modified = True

    def keyReleaseEvent(self, event: KeyEvent) -> None:  # noqa: N802

        match event.key():
            case QtCore.Qt.Key.Key_Control:
                self._ctrl_modified = False
            case QtCore.Qt.Key.Key_Shift:
                self._shift_modified = False

    def update(
        self,
        data: Data | None = None,
        pattern: Mapping[str, Any] | None = None,
    ) -> None:
        """Update graph's data."""

        return None

    def filtrate(
        self,
        pattern: Mapping[str, Any] | None = None,
    ) -> None:
        """Filtrate graph's data with given pattern."""
        self._update(pattern=pattern)

    def _pick_event(self, event: PickEvent) -> None:
        return None

    def _button_press_event(self, event: MouseEvent) -> None:
        self._mouse_event = event

        # update zoom and pan
        if self._ctrl_modified and self._shift_modified:
            return None

        if self._ctrl_modified:
            return None

        if self._shift_modified:
            return None

        if event.button == 3 and event.dblclick:
            self._mouse_event = None
            self._crop_lims = None
            self._update_zoom(lims=self._full_lims)

    def _button_release_event(self, event: MouseEvent) -> None:

        # update annotate
        self.annotate.set_visible(False)
        self.canvas.draw_idle()

        # update zoom and pan
        if self._ctrl_modified and self._shift_modified:
            return None

        if self._ctrl_modified:
            return None

        if self._shift_modified:
            if event.button == 1:
                self._pan_event(
                    self._mouse_event,
                    event,
                )
            return None

        if event.button == 3:
            self._zoom_event(
                self._mouse_event,
                event,
            )

    def _motion_notify_event(self, event: MouseEvent) -> None:

        # update zoom and pan
        if self._ctrl_modified and self._shift_modified:
            pass

        if self._ctrl_modified:
            return None

        if self._shift_modified:
            if event.button == 1:
                self._pan_event(
                    self._mouse_event,
                    event,
                )
                return None

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

    def set_full_lims(self, lims: Lims) -> None:

        self._full_lims = lims

    def set_crop_lims(self, lims: Lims) -> None:

        self._crop_lims = lims

    def _update_zoom(self, lims: Lims | None = None) -> None:

        xlim, ylim = lims or self._full_lims or self._default_lims

        self.canvas.axes.set_xlim(xlim)
        self.canvas.axes.set_ylim(ylim)
        self.canvas.draw_idle()
