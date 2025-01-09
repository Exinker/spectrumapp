import numpy as np
import pytest
from PySide6 import QtGui

from spectrumapp.colors.alpha import DefaultAlphaset
from spectrumapp.colors.color import Color, format_color


@pytest.mark.parametrize(
    ['color', 'expected'],
    [
        (QtGui.QColorConstants.Gray, 255*DefaultAlphaset.DEFAULT.value),
        ('grey', 255*DefaultAlphaset.DEFAULT.value),
        ([0.627451, 0.627451, 0.643137], 255*DefaultAlphaset.DEFAULT.value),
        ([0.627451, 0.627451, 0.643137, DefaultAlphaset.DEFAULT.value], 255*DefaultAlphaset.DEFAULT.value),
    ],
)
def test_format_color(
    color: Color,
    expected: int,
):
    result = format_color(color, is_faded=False)

    assert np.isclose(result.alpha(), expected)
