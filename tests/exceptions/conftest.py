import pytest


@pytest.fixture(params=['test', ''])
def message(request) -> str:
    return request.param


@pytest.fixture(params=['test', ''])
def info(request) -> str:
    return request.param
