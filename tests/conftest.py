import pytest

import spectrumapp
from spectrumapp.application import BaseApplication


@pytest.fixture(autouse=True)
def setup_environ(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv('APPLICATION_NAME', 'Tests')
    monkeypatch.setenv('APPLICATION_VERSION', spectrumapp.__version__)
    monkeypatch.setenv('ORGANIZATION_NAME', spectrumapp.__organization__)

    yield


@pytest.fixture(scope="session")
def qapp_cls():
    return BaseApplication
