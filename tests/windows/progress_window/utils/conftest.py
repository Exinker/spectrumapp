import pytest


@pytest.fixture
def info(
    faker,
) -> str:
    return faker.sentence()
