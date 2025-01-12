from typing import Any, Mapping

import pytest

from spectrumapp.widgets.graph_widget import BaseGraphWidget
from spectrumapp.widgets.graph_widget.graph_widget import Index


@pytest.fixture(params=[None])
def pattern(request) -> Mapping[Index, Any] | None:
    return request.param


def test_reset_zoom(
    pattern: Mapping[Index, Any] | None,
    graph_widget: BaseGraphWidget,
    mocker,
):
    spy = mocker.spy(graph_widget, 'update')

    graph_widget.filtrate(
        pattern=pattern,
    )

    spy.assert_called_once_with(pattern=pattern)
