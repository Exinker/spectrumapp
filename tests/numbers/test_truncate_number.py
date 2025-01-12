import pytest

from spectrumapp.numbers import truncate_number


@pytest.mark.parametrize(
    ['number', 'expected'],
    [
        # (0, '0.00'),
        (1/1, '1'),
        (1/2, '0.5'),
        (1/4, '0.25'),
        (1/8, '0.125'),
        (1/3, '0.3333'),
    ],
)
def test_truncate_number(
    number: float,
    expected: str,
):
    result = truncate_number(number)

    assert result == expected
