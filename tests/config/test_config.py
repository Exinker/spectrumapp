import os

import pytest

from spectrumapp.config import BaseConfig, setdefault_config
from spectrumapp.types import DirPath, FilePath


def test_setdefault_config(
    filepath: FilePath,
):
    setdefault_config()

    config = BaseConfig.load()
    assert config.FILEPATH == filepath
    assert config.version == os.environ['APPLICATION_VERSION']
    assert config.directory == ''


def test_load_config(
    filepath: FilePath,
):
    setdefault_config()

    config = BaseConfig.load()
    assert config.FILEPATH == filepath
    assert config.version == os.environ['APPLICATION_VERSION']
    assert config.directory == ''


@pytest.mark.parametrize(
    'directory', [
        os.path.join(os.getcwd(), 'tests'),
    ],
)
def test_config_update_directory(directory: DirPath):
    setdefault_config()

    config = BaseConfig.load()
    config.update(
        directory=directory,
    )

    config = BaseConfig.load()
    assert config.directory == directory
