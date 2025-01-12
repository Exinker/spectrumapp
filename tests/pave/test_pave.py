import os
import sys

import pytest
from pytest import MonkeyPatch

from spectrumapp.paths import pave


@pytest.fixture(autouse=True, params=['develop', 'deploy'])
def state(request) -> None:

    return request.param


@pytest.fixture
def relative_path() -> str:
    return os.getcwd()


@pytest.fixture
def expected(
    relative_path: str,
    state: str,
) -> str:

    match state:
        case 'develop':
            return relative_path
        case 'deploy':
            return os.path.join('test', relative_path)


def test_pave(
    relative_path: str,
    state: str,
    expected: str,
    monkeypatch: MonkeyPatch,
):

    match state:
        case 'develop':
            monkeypatch.delattr(sys, '_MEIPASS', raising=False)
        case 'deploy':
            monkeypatch.setattr(sys, '_MEIPASS', 'test', raising=False)

    assert pave(relative_path) == expected
