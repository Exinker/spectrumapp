from enum import Enum
from typing import TypeAlias


Alpha: TypeAlias = float


def format_alpha(alpha: Alpha, is_faded: bool) -> int:
    if is_faded:
        alpha = alpha * DefaultAlphaset.FADED

    return int(255 * alpha)


class DefaultAlphaset(Enum):

    DEFAULT = 0.6
    FADED = 0.8
    IS_NOT_ACTIVE = 0.2
