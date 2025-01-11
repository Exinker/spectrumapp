import pytest
from PySide6 import QtCore
from pytestqt.qtbot import QtBot

from spectrumapp.widgets.graph_widget import BaseGraphWidget
from spectrumapp.widgets.graph_widget.graph_widget import (
    DEFAULT_LIMS,
    DEFAULT_SIZE,
)


def test_graph_widget(
    object_name: str,
    graph_widget: BaseGraphWidget,
):

    assert graph_widget.objectName() == object_name
    assert graph_widget.size() == DEFAULT_SIZE
    assert graph_widget._default_lims == DEFAULT_LIMS


@pytest.mark.parametrize(
    'key', [
        QtCore.Qt.Key.Key_Control,
        QtCore.Qt.Key.Key_Shift,
    ],
)
def test_key_press_event(
    key: QtCore.Qt.Key,
    graph_widget: BaseGraphWidget,
    qtbot: QtBot,
):

    qtbot.keyPress(graph_widget, key)

    assert getattr(graph_widget, {
        QtCore.Qt.Key.Key_Control: '_ctrl_modified',
        QtCore.Qt.Key.Key_Shift: '_shift_modified',
    }[key]) is True


@pytest.mark.parametrize(
    'key', [
        QtCore.Qt.Key.Key_Control,
        QtCore.Qt.Key.Key_Shift,
    ],
)
def test_key_release_event(
    key: QtCore.Qt.Key,
    graph_widget: BaseGraphWidget,
    qtbot: QtBot,
):

    qtbot.keyPress(graph_widget, key)
    qtbot.keyRelease(graph_widget, key)

    assert getattr(graph_widget, {
        QtCore.Qt.Key.Key_Control: '_ctrl_modified',
        QtCore.Qt.Key.Key_Shift: '_shift_modified',
    }[key]) is False
