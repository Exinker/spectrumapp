from dataclasses import dataclass
from typing import Any, Mapping, NewType

from PySide6 import QtCore, QtWidgets
from matplotlib.backend_bases import KeyEvent, MouseEvent, PickEvent

from spectrumapp.helpers import getdefault_object_name
from spectrumapp.types import Lims
from spectrumapp.widgets.graph_widget.canvas import MplCanvas


DEFAULT_SIZE = QtCore.QSize(640, 480)
DEFAULT_LIMS = ((0, 1), (0, 1))


Index = NewType('Index', str)


@dataclass
class AxisLabel:
    xlabel: str
    ylabel: str


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

        self._widget_size = size

        self._data = None
        self._point_labels = None
        self._axis_labels = None
        self._point_annotation = None
        self._zoom_region = None
        self._full_lims = None
        self._cropped_lims = None

        # object name
        object_name = object_name or getdefault_object_name(self)
        self.setObjectName(object_name)

        # focus
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()

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

        # pressed mouse and keys events
        self._mouse_event: MouseEvent | None = None
        self._ctrl_modified = False
        self._shift_modified = False

        # geometry
        self.setFixedSize(self._widget_size)

    @property
    def data(self) -> Mapping[Index, Any] | None:
        return self._data

    @property
    def point_labels(self) -> Mapping[Index, tuple[str, ...]] | None:
        return self._point_labels

    @property
    def axis_labels(self) -> AxisLabel | None:
        return self._axis_labels

    @property
    def default_lims(self) -> Lims:
        return DEFAULT_LIMS

    @property
    def full_lims(self) -> Lims | None:
        return self._full_lims

    @property
    def cropped_lims(self) -> Lims | None:
        return self._cropped_lims

    @property
    def ctrl_modified(self) -> bool:
        return self._ctrl_modified

    @property
    def shift_modified(self) -> bool:
        return self._shift_modified

    def update(
        self,
        data: Mapping[Index, Any] | None = None,
        pattern: Mapping[Index, Any] | None = None,
    ) -> None:
        """Update graph's `data`."""

        data = data or self.data
        if data is None:
            return None

        raise NotImplementedError

    def filtrate(
        self,
        pattern: Mapping[Index, Any] | None = None,
    ) -> None:
        """Filtrate graph's `data` with given `pattern`."""

        self.update(pattern=pattern)

    def update_zoom(self, lims: Lims | None = None) -> None:
        """Update zoom to given `lims`."""

        xlim, ylim = lims or self.full_lims or self.default_lims

        self.canvas.axes.set_xlim(xlim)
        self.canvas.axes.set_ylim(ylim)
        self.canvas.draw_idle()

    def set_full_lims(self, lims: Lims) -> None:
        """Set full lims (maximum) to given `lims`."""

        self._full_lims = lims

    def set_cropped_lims(self, lims: Lims | None) -> None:
        """Set cropped lims to given `lims`."""

        self._cropped_lims = lims

    def set_shift_modified(self, __state: bool) -> None:
        self._shift_modified = __state

    def set_ctrl_modified(self, __state: bool) -> None:
        self._ctrl_modified = __state

    def sizeHint(self) -> QtCore.QSize:  # noqa: N802
        return self._widget_size

    def keyPressEvent(self, event: KeyEvent) -> None:  # noqa: N802

        match event.key():
            case QtCore.Qt.Key.Key_Control:
                self.set_ctrl_modified(True)
            case QtCore.Qt.Key.Key_Shift:
                self.set_shift_modified(True)
            case _:
                return None

    def keyReleaseEvent(self, event: KeyEvent) -> None:  # noqa: N802

        match event.key():
            case QtCore.Qt.Key.Key_Control:
                self.set_ctrl_modified(False)
            case QtCore.Qt.Key.Key_Shift:
                self.set_shift_modified(False)
            case _:
                return None

    def _pick_event(self, event: PickEvent) -> None:  # pragma: no cover
        return None

    def _button_press_event(self, event: MouseEvent) -> None:  # pragma: no cover
        self._mouse_event = event

        # update zoom and pan
        if self.ctrl_modified and self.shift_modified:
            return None

        if self.ctrl_modified:
            return None

        if self.shift_modified:
            return None

        if event.button == 3 and event.dblclick:
            self._mouse_event = None
            self.set_cropped_lims(lims=None)
            self.update_zoom(lims=self.full_lims)

    def _button_release_event(self, event: MouseEvent) -> None:  # pragma: no cover

        # update annotate
        self._point_annotation.set_visible(False)
        self.canvas.draw_idle()

        # update zoom and pan
        if self.ctrl_modified and self.shift_modified:
            return None

        if self.ctrl_modified:
            return None

        if self.shift_modified:
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

    def _motion_notify_event(self, event: MouseEvent) -> None:  # pragma: no cover

        # update zoom and pan
        if self.ctrl_modified and self.shift_modified:
            return None

        if self.ctrl_modified:
            return None

        if self.shift_modified:
            if event.button == 1:
                self._pan_event(
                    self._mouse_event,
                    event,
                )
                return None

    def _zoom_event(self, press_event: MouseEvent, release_event: MouseEvent) -> None:  # pragma: no cover

        # update crop lims
        xlim = tuple(sorted(
            (event.xdata for event in (press_event, release_event)),
        ))
        ylim = tuple(sorted(
            (event.ydata for event in (press_event, release_event)),
        ))
        self.set_cropped_lims(
            lims=(xlim, ylim),
        )

        # update zoom
        self.update_zoom(
            lims=self.cropped_lims,
        )

    def _pan_event(self, press_event: MouseEvent, release_event: MouseEvent) -> None:  # pragma: no cover

        # update crop lims
        xlim, ylim = self.canvas.axes.get_xlim(), self.canvas.axes.get_ylim()
        xshift, yshift = release_event.xdata - press_event.xdata, release_event.ydata - press_event.ydata
        self.set_cropped_lims(
            lims=(
                [value - xshift for value in xlim],
                [value - yshift for value in ylim],
            ),
        )

        # update zoom
        self.update_zoom(
            lims=self._cropped_lims,
        )
