from PySide6 import QtCore
from pytestqt.qtbot import QtBot

from spectrumapp.types import Lims
from spectrumapp.widgets.graph_widget import BaseGraphWidget


def test_reset_zoom(
    full_lims: Lims,
    graph_widget: BaseGraphWidget,
    qtbot: QtBot,
    mocker,
):
    xlims, ylims = full_lims
    spy_set_xlim = mocker.spy(graph_widget.canvas.axes, 'set_xlim')
    spy_set_ylim = mocker.spy(graph_widget.canvas.axes, 'set_ylim')
    spy_draw_idle = mocker.spy(graph_widget.canvas, 'draw_idle')

    graph_widget._full_lims = full_lims

    qtbot.mouseDClick(graph_widget.canvas, QtCore.Qt.MouseButton.RightButton)

    assert graph_widget._mouse_event is None
    assert graph_widget._crop_lims is None
    spy_set_xlim.assert_called_once_with(xlims)
    spy_set_ylim.assert_called_once_with(ylims)
    spy_draw_idle.assert_called_once()
