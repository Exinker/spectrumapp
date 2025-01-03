from collections.abc import Sequence
from enum import Enum
from typing import TypeAlias

from PySide6 import QtGui

from spectrumapp.colors.alpha import DefaultAlphaset, format_alpha


Color: TypeAlias = QtGui.QColor | str | Sequence[float, float, float] | Sequence[float, float, float, float]


def format_color(
    color: Color,
    alpha: float = DefaultAlphaset.DEFAULT,
    is_faded: bool = False,
) -> QtGui.QColor:

    if isinstance(color, QtGui.QColor):
        alpha = format_alpha(alpha, is_faded=is_faded)
        color.setAlpha(alpha)

        return color

    if isinstance(color, str):
        alpha = format_alpha(alpha, is_faded=is_faded)
        color = QtGui.QColor(color)
        color.setAlpha(alpha)

        return color

    if isinstance(color, Sequence):
        if len(color) == 4:
            *color, alpha = color

        alpha = format_alpha(alpha, is_faded=is_faded)
        color = QtGui.QColor(*[int(255*c) for c in color])
        color.setAlpha(alpha)

        return color

    raise NotImplementedError(f'Color {type(color)} is not supported yet!')


class RedOrangeYellowGreenColorset(Enum):
    """https://www.schemecolor.com/red-orange-green-gradient.php"""

    RED = '#FF0D0D'
    ORANGE = '#FF8E15'
    YELLOW = '#FAB733'
    GREEN = '#69B34C'


class BluePinkColorset(Enum):

    BLUE = (0, 0.4470, 0.7410)
    PINK = (1, 0.4470, 0.7410)


class MarkColorset(Enum):

    IS_NOT_ACTIVE = '#707C80'
    SELECTED = (0, 0.37254902, 0.88627451, .5)
