from typing import TypeAlias


# ---------        constants        ---------
ALPHA = {
    'default': .6,
    'is_not_active': .2,

    'probe': .5,
    'parallel': .2,
}


# ---------        types        ---------
Alpha: TypeAlias = float


# ---------        handlers        ---------
def format_alpha(alpha: Alpha, is_faded: bool) -> int:
    if is_faded:
        alpha = alpha * 8/10

    return int(255 * alpha)
