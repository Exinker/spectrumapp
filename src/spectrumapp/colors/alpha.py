from enum import Enum
from typing import TypeAlias


Alpha: TypeAlias = float


class DefaultAlphaset(Enum):
    DEFAULT = 0.6
    FADED = 0.8
    SHADOW = 0.2


def format_alpha(alpha: Alpha, is_faded: bool = False) -> int:
    return int(255 * _fade_alpha(alpha, is_faded=is_faded))


def _fade_alpha(__alpha: Alpha, is_faded: bool) -> float:

    if is_faded:
        return __alpha * DefaultAlphaset.FADED.value
    return __alpha
