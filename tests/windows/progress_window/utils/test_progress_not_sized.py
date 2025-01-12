import time
from collections.abc import Iterable
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


@pytest.fixture(scope='function')
def values(
    n_values: int,
) -> Iterable[T]:
    return (
        i for i in range(n_values)
    )


@pytest.fixture
def expected(
    n_values: int,
    values: Iterable[T],
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


def test_progress(
    values: Iterable[T],
    default_info: str,
    expected: tuple,
    progress_window: ProgressWindow,
    mocker,
):
    spy = mocker.spy(progress_window, 'on_updated')

    for _ in utils.progress(values, info=default_info):
        time.sleep(0.001)

    try:
        spy.assert_has_calls(expected)
    except AssertionError:
        print()
