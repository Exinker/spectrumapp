from collections.abc import Sequence
from typing import TypeAlias

from PySide6 import QtGui

from spectrumapp.colors.alpha import ALPHA, format_alpha


Color: TypeAlias = QtGui.QColor | str | Sequence[float, float, float] | Sequence[float, float, float, float]


COLOR = {
    'selected': (0, 0.37254902, 0.88627451, .5),
    'is_not_active': '#707C80',

    # https://www.schemecolor.com/red-orange-green-gradient.php
    'red': '#FF0D0D',
    'orange': '#FF8E15',
    'yellow': '#FAB733',
    'green': '#69B34C',

    'blue': (0, 0.4470, 0.7410),
    'pink': (1, 0.4470, 0.7410),
}

COLOR_DATASET = {
    'train': (0.17254902, 0.62745098, 0.17254902, 0.5),  # '#009300'
    'valid': (1., 0.49803922, 0.05490196, 0.5),
    'test': (0.12156863, 0.46666667, 0.70588235, 0.5),  # '#000096'
}

COLOR_INFLUENCE = {
    'analytical': '#FFE1CC',
    'macrocomponent': '#FFFACC',
    'interfering': '#EBFFCC',
}

COLOR_INTENSITY = {
    'amplitude': '#2ca02c',
    'nearest': '#1f77b4',
    'linear': '#ff7f0e',
    'shape': '#9467bd',
}


def format_color(
    color: Color,
    alpha: float = ALPHA['default'],
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
