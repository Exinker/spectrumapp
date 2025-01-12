import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.types import Lims
from spectrumapp.widgets.graph_widget import BaseGraphWidget


@pytest.fixture(params=['test'])
def object_name(request) -> str:
    return request.param


@pytest.fixture(params=[((0, 10), (0, 20))])
def full_lims(request) -> Lims:
    return request.param


@pytest.fixture(params=[((0, 1), (0, 2))])
def croped_lims(request) -> Lims:
    return request.param


@pytest.fixture()
def graph_widget(
    object_name: str,
    full_lims: Lims,
    croped_lims: Lims,
    qtbot: QtBot,
) -> BaseGraphWidget:

    graph_widget = BaseGraphWidget(
        object_name=object_name,
    )
    graph_widget.set_cropped_lims(
        lims=croped_lims,
    )
    graph_widget.set_full_lims(
        lims=full_lims,
    )

    return graph_widget
