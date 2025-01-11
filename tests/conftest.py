import pytest

import spectrumapp


@pytest.fixture(autouse=True)
def setup_environ(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv('APPLICATION_NAME', 'Tests')
    monkeypatch.setenv('APPLICATION_VERSION', spectrumapp.__version__)
    monkeypatch.setenv('ORGANIZATION_NAME', spectrumapp.__organization__)

    yield
