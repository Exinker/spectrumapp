import time
from collections.abc import Sequence
from typing import TypeVar
from unittest.mock import call

import pytest

from spectrumapp.windows.progress_window import (
    ProgressState,
    ProgressWindow,
    utils,
)
from spectrumapp.windows.progress_window.utils.progress import (
    _get_message,
    _get_progress,
)


T = TypeVar('T')


@pytest.fixture(params=[0, 1])
def n_values(request) -> int:
    return request.param


@pytest.fixture
def values(
    n_values: int,
) -> list[T]:
    return list(range(n_values))


@pytest.fixture
def expected(
    n_values: int,
    values: Sequence[T],
    default_info: str,
) -> tuple:

    calls = []
    for i, value in enumerate(values, start=1):
        state = ProgressState(
            progress=_get_progress(i, total=n_values),
            info=default_info,
            message=_get_message(i, value, total=n_values),
        )
        calls.append(call(state))

    return tuple(calls)


# @pytest.mark.skip(reason='Flaky test')
def test_progress(
    values: Sequence[T],
    default_info: str,
    expected: tuple,
    progress_window: ProgressWindow,
    mocker,
):
    spy_on_updated = mocker.spy(progress_window, 'on_updated')
    # mock_close = mocker.patch.object(progress_window, 'close')

    for _ in utils.progress(values, info=default_info):
        time.sleep(0.0)

    spy_on_updated.assert_has_calls(expected)
    # mock_close.assert_called_once()
