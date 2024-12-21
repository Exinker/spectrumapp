from typing import TypeAlias

from spectrumapp.colors.alphasets import DefaultAlphaset


Alpha: TypeAlias = float


def format_alpha(alpha: Alpha, is_faded: bool) -> int:
    if is_faded:
        alpha = alpha * DefaultAlphaset.FADED

    return int(255 * alpha)
