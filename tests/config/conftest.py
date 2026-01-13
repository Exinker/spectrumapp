import os
from pathlib import Path

import pytest

from spectrumapp.config import BaseConfig


@pytest.fixture()
def filepath(
    tmp_path: Path,
) -> Path:
    return tmp_path / 'config.json'


@pytest.fixture(autouse=True)
def cleanup_files(
    filepath: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(BaseConfig, 'FILEPATH', filepath)

    yield

    if os.path.isfile(filepath):
        os.remove(filepath)
