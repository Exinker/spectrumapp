
from typing import overload

from PySide6 import QtCore, QtGui, QtWidgets


# ---------        COLOR        ---------
COLOR_ALPHA = .6
COLOR = {
    'selected': [0, 0.37254902, 0.88627451, .5],
    'not_is_active': '#707C80',

    # https://www.schemecolor.com/red-orange-green-gradient.php
    'red': '#FF0D0D',
    'orange': '#FF8E15',
    'yellow': '#FAB733',
    'green': '#69B34C',

    'train': [0.17254902, 0.62745098, 0.17254902, 0.5],  # '#009300'
    'valid': [1., 0.49803922, 0.05490196, 0.5],
    'test': [0.12156863, 0.46666667, 0.70588235, 0.5],  # '#000096'

    'blue': [0, 0.4470, 0.7410],
    'pink': [1, 0.4470, 0.7410],
}


# ---------        handlers        ---------
def format_alpha(alpha: float, is_faded: bool) -> int:
    if is_faded:
        alpha = alpha * 8/10

    return int(255 * alpha)


@overload
def format_color(color: QtGui.QColor, alpha: float = COLOR_ALPHA, is_faded: bool = False) -> QtGui.QColor: ...
@overload
def format_color(color: str, alpha: float = COLOR_ALPHA, is_faded: bool = False) -> QtGui.QColor: ...
@overload
def format_color(color: list[float, float, float], alpha: float = COLOR_ALPHA, is_faded: bool = False) -> QtGui.QColor: ...
def format_color(color, alpha=COLOR_ALPHA, is_faded=False):

    if isinstance(color, list):
        *color, alpha = color

        alpha = format_alpha(alpha, is_faded=is_faded)
        color = QtGui.QColor(*[int(255*c) for c in color])
        color.setAlpha(alpha)

        return color

    if isinstance(color, str):
        alpha = format_alpha(alpha, is_faded=is_faded)
        color = QtGui.QColor(color)
        color.setAlpha(alpha)

        return color

    if isinstance(color, QtGui.QColor):
        alpha = format_alpha(alpha, is_faded=is_faded)
        color.setAlpha(alpha)

        return color

    raise NotImplementedError(f'{type(color)} is not valid type of color!')
