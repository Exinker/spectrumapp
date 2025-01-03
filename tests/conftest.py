import os

import pytest

import spectrumapp


@pytest.fixture(autouse=True)
def setup_environ():
    os.environ['APPLICATION_NAME'] = 'Tests'
    os.environ['APPLICATION_VERSION'] = spectrumapp.__version__
    os.environ['ORGANIZATION_NAME'] = spectrumapp.__organization__

    yield
