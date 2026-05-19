import os
import sys

import pytest
from faker import Faker
from PySide6 import QtWidgets

from spectrumapp.applications import BaseApplication


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


@pytest.fixture(scope='session')
def qapp_cls(
    application_name: str,
    application_version: str,
    organization_name: str,
):

    class TestApplication(BaseApplication):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(
                *args,
                application_name=application_name,
                application_version=application_version,
                organization_name=organization_name,
                **kwargs,
            )

    return TestApplication
