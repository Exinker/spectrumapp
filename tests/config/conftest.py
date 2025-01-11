import os
from pathlib import Path

import pytest

from spectrumapp.config import BaseConfig
from spectrumapp.types import FilePath


@pytest.fixture()
def filepath(
    tmp_path: Path,
) -> FilePath:
    return tmp_path / 'config.json'


@pytest.fixture(autouse=True)
def cleanup_files(
    filepath: FilePath,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(BaseConfig, 'FILEPATH', filepath)

    yield

    if os.path.isfile(filepath):
        os.remove(filepath)
