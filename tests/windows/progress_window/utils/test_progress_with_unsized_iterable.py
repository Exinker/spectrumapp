import importlib
from collections.abc import Iterable
from typing import TypeVar
from unittest.mock import call

import pytest

from spectrumapp.windows.progress_window import (
    ProgressState,
    ProgressWindow,
)
from spectrumapp.windows.progress_window.utils.progress import (
    _get_message,
    _get_progress,
    progress,
)


progress_module = importlib.import_module('spectrumapp.windows.progress_window.utils.progress')

T = TypeVar('T')


@pytest.fixture(params=[0, 1])
def n_values(request) -> int:
    return request.param


@pytest.fixture(scope='function')
def source_values(
    n_values: int,
) -> list[T]:
    return list(range(n_values))


@pytest.fixture(scope='function')
def values(
    source_values: list[T],
) -> Iterable[T]:
    return (value for value in source_values)


@pytest.fixture
def expected(
    info: str,
    source_values: list[T],
) -> tuple:
    return tuple(
        call(ProgressState(
            progress=_get_progress(i, total=None),
            info=info,
            message=_get_message(i, value, total=None),
        ))
        for i, value in enumerate(source_values, start=1)
    )


def test_progress(
    info: str,
    values: Iterable[T],
    source_values: list[T],
    expected: tuple,
    progress_window: ProgressWindow,
    monkeypatch: pytest.MonkeyPatch,
    mocker,
):
    monkeypatch.setattr(progress_module, 'find_window', lambda *args, **kwargs: progress_window)
    updated_mock = mocker.Mock()
    progress_window.updated.connect(updated_mock)

    result = list(progress(values, info=info))

    assert result == source_values
    updated_mock.assert_has_calls(expected)
