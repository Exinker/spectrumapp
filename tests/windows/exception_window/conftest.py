import pytest

from spectrumapp.windows.exception_window import ExceptionLevel


@pytest.fixture(params=['test', ''])
def message(request) -> str:
    return request.param


@pytest.fixture(params=['test', ''])
def info(request) -> str:
    return request.param


@pytest.fixture(params=ExceptionLevel)
def level(request) -> ExceptionLevel:
    return request.param
