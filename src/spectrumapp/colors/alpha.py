from typing import TypeAlias


Alpha: TypeAlias = float


ALPHA = {
    'default': .6,
    'is_not_active': .2,

    'probe': .5,
    'parallel': .2,
}


def format_alpha(alpha: Alpha, is_faded: bool) -> int:
    if is_faded:
        alpha = alpha * 8/10

    return int(255 * alpha)
