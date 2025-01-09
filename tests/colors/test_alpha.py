import pytest

from spectrumapp.colors.alpha import Alpha, format_alpha


@pytest.mark.parametrize(
    ['alpha', 'expected'],
    [
        (1, 255),
        (0, 0),
    ],
)
def test_format_alpha(
    alpha: Alpha,
    expected: int,
):
    result = format_alpha(alpha)

    assert result == expected


@pytest.mark.parametrize(
    ['alpha', 'expected'],
    [
        (1, 204),
        (0, 0),
    ],
)
def test_format_alpha_faded(
    alpha: Alpha,
    expected: int,
):
    result = format_alpha(alpha, is_faded=True)

    assert result == expected
