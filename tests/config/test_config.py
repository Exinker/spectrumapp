import os
from pathlib import Path

import pytest

from spectrumapp.configs import BaseConfig, setdefault_config


def test_setdefault_config(
    filepath: Path,
):
    setdefault_config()

    config = BaseConfig.load()
    assert config.FILEPATH == filepath
    assert config.version == os.environ['APPLICATION_VERSION']
    assert config.directory is None


def test_load_config(
    filepath: Path,
):
    setdefault_config()

    config = BaseConfig.load()
    assert config.FILEPATH == filepath
    assert config.version == os.environ['APPLICATION_VERSION']
    assert config.directory is None


@pytest.mark.parametrize(
    'directory', [
        Path(os.getcwd()) / 'tests',
    ],
)
def test_config_update_directory(directory: Path):
    setdefault_config()

    config = BaseConfig.load()
    config.update(
        directory=directory,
    )

    config = BaseConfig.load()
    assert config.directory == directory
