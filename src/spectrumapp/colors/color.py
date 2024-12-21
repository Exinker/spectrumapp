from collections.abc import Sequence
from typing import TypeAlias

from PySide6 import QtGui

from spectrumapp.colors.alpha import format_alpha
from spectrumapp.colors.alphasets import DefaultAlphaset


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
