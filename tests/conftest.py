import os
import sys

import pytest

import spectrumapp
from spectrumapp.application import BaseApplication


if (
    'QT_QPA_PLATFORM' not in os.environ
    and sys.platform.startswith('linux')
    and not os.environ.get('DISPLAY')
    and not os.environ.get('WAYLAND_DISPLAY')
):
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'


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
