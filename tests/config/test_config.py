from pathlib import Path

import pytest

from spectrumapp.configs import BaseConfig, setdefault_config


def test_setdefault_config(
    application_version: str,
    filepath: Path,
):
    setdefault_config(
        version=application_version,
    )

    config = BaseConfig.load(version=application_version)
    assert config.FILEPATH == filepath
    assert config.version == application_version
    assert config.directory is None


def test_load_config(
    application_version: str,
    filepath: Path,
):
    setdefault_config(
        version=application_version,
    )

    config = BaseConfig.load(version=application_version)
    assert config.FILEPATH == filepath
    assert config.version == application_version
    assert config.directory is None


@pytest.mark.parametrize(
    'directory', [
        Path.cwd() / 'tests',
    ],
)
def test_config_update_directory(
    application_version: str,
    directory: Path,
):
    setdefault_config(
        version=application_version,
    )

    config = BaseConfig.load(version=application_version)
    config.update(
        directory=directory,
    )

    config = BaseConfig.load(version=application_version)
    assert config.directory == directory
