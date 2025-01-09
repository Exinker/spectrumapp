import numpy as np
import pytest

from spectrumapp.numbers import format_number


@pytest.mark.parametrize(
    ['number', 'expected'],
    [
        (0, '0'),
        (0., '0'),
        (np.nan, ''),
        (+np.inf, ''),
        (-np.inf, ''),
        (3.1415927, '3.1416'),
        (3.1415000001, '3.1415'),
        (3.1415, '3.1415'),
    ],
)
def test_format_number(
    number: float,
    expected: str,
):
    result = format_number(number)

    assert result == expected
