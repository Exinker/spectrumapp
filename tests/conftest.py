import os
import sys

import pytest
from faker import Faker

from spectrumapp.applications import ApplicationABC


if (
    'QT_QPA_PLATFORM' not in os.environ
    and sys.platform.startswith('linux')
    and not os.environ.get('DISPLAY')
    and not os.environ.get('WAYLAND_DISPLAY')
):
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'


@pytest.fixture(scope='session')
def faker_session():
    return Faker()


@pytest.fixture(scope='session')
def application_name(faker_session: Faker):
    return faker_session.word().title()


@pytest.fixture(scope='session')
def application_version(faker_session: Faker):
    return faker_session.numerify('%#.%#.%#')


@pytest.fixture(scope='session')
def organization_name(faker_session: Faker):
    return faker_session.company()


@pytest.fixture(scope='session', autouse=True)
def setup_environ(
    application_name: str,
    application_version: str,
    organization_name: str,
):
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv('APPLICATION_NAME', application_name)
    monkeypatch.setenv('APPLICATION_VERSION', application_version)
    monkeypatch.setenv('ORGANIZATION_NAME', organization_name)

    yield


@pytest.fixture(scope='session')
def qapp_cls():

    class TestApplication(ApplicationABC):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(
                *args,
                application_name=os.environ['APPLICATION_NAME'],
                application_version=os.environ['APPLICATION_VERSION'],
                organization_name=os.environ['ORGANIZATION_NAME'],
                **kwargs,
            )

    return TestApplication
