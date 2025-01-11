import pytest

from spectrumapp.windows.exception_window import get_text_template


@pytest.fixture
def expected(
    message: str,
) -> str:
    if message:
        return '{message}\n\n{info}'
    return '{info}'


def test_text_template(
    message: str,
    expected: str,
):
    result = get_text_template(
        message=message,
    )

    assert result == expected
