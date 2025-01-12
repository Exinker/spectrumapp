import pytest
from PySide6 import QtCore
from pytestqt.qtbot import QtBot

from spectrumapp.types import Lims
from spectrumapp.widgets.graph_widget import BaseGraphWidget
from spectrumapp.widgets.graph_widget.graph_widget import (
    DEFAULT_LIMS,
    DEFAULT_SIZE,
)


def test_graph_widget(
    object_name: str,
    full_lims: Lims,
    croped_lims: Lims,
    graph_widget: BaseGraphWidget,
):

    assert graph_widget.objectName() == object_name
    assert graph_widget.size() == DEFAULT_SIZE
    assert graph_widget.sizeHint() == DEFAULT_SIZE
    assert graph_widget.data is None
    assert graph_widget.point_labels is None
    assert graph_widget.axis_labels is None
    assert graph_widget.default_lims == DEFAULT_LIMS
    assert graph_widget.full_lims == full_lims
    assert graph_widget.cropped_lims == croped_lims


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
def test_key_press_and_release_event(
    key: QtCore.Qt.Key,
    graph_widget: BaseGraphWidget,
    mocker,
    qtbot: QtBot,
):

    qtbot.keyPress(graph_widget, key)
    qtbot.keyRelease(graph_widget, key)

    assert getattr(graph_widget, {
        QtCore.Qt.Key.Key_Control: '_ctrl_modified',
        QtCore.Qt.Key.Key_Shift: '_shift_modified',
    }[key]) is False


@pytest.mark.parametrize(
    'key', [
        QtCore.Qt.Key.Key_Space,
    ],
)
def test_key_press_and_release_event_other_keys(  # added to full coverage
    key: QtCore.Qt.Key,
    graph_widget: BaseGraphWidget,
    mocker,
    qtbot: QtBot,
):
    spy_ctrl_modified = mocker.spy(graph_widget, 'set_ctrl_modified')
    spy_shift_modified = mocker.spy(graph_widget, 'set_shift_modified')

    qtbot.keyPress(graph_widget, key)
    qtbot.keyRelease(graph_widget, key)

    spy_ctrl_modified.assert_not_called()
    spy_shift_modified.assert_not_called()
