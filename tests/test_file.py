import os
import pytest

from spectrumapp import ORGANIZATION_NAME, VERSION
from spectrumapp.config import File, setdefault_file
from spectrumapp.types import DirPath, FilePath


@pytest.fixture()
def filepath() -> FilePath:
    return os.path.join(os.getcwd(), 'config.json')


@pytest.fixture(autouse=True)
def setup_environ() -> None:
    os.environ['APPLICATION_NAME'] = 'Tests'
    os.environ['APPLICATION_VERSION'] = VERSION
    os.environ['ORGANIZATION_NAME'] = ORGANIZATION_NAME

    os.environ['DEBUG'] = str(True)

    yield


@pytest.fixture(autouse=True)
def cleanup_files(filepath: FilePath) -> None:
    yield

    if os.path.isfile(filepath):
        os.remove(filepath)


def test_setdefault_file(filepath: FilePath):
    setdefault_file()

    file = File.load()
    assert file.FILEPATH == filepath
    assert file.version == os.environ['APPLICATION_VERSION']
    assert file.directory == ''


@pytest.mark.parametrize('directory', [
    os.path.join(os.getcwd(), 'tests'),
])
def test_update_directory(directory: DirPath):
    setdefault_file()

    file = File.load()
    file.update({
        'directory': directory,
    })

    file = File.load()
    assert file.directory == directory
