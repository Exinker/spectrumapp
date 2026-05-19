import os
import sys
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from spectrumapp.paths import pave


@pytest.fixture(autouse=True, params=['develop', 'deploy'])
def state(request) -> None:

    return request.param


@pytest.fixture
def relative_path() -> Path:
    return Path.cwd()


@pytest.fixture
def expected(
    relative_path: Path,
    state: str,
) -> Path:

    match state:
        case 'develop':
            return relative_path
        case 'deploy':
            return Path('test') / relative_path


def test_pave(
    relative_path: Path,
    state: str,
    expected: Path,
    monkeypatch: MonkeyPatch,
):

    match state:
        case 'develop':
            monkeypatch.delattr(sys, '_MEIPASS', raising=False)
        case 'deploy':
            monkeypatch.setattr(sys, '_MEIPASS', 'test', raising=False)

    assert pave(relative_path) == expected
