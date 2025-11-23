from typing import Any

import numpy as np

from spectrumapp.types import Array


def format_number(
    number: str | int | float,
    precision: int = 4,
) -> str:
    """Format `number` for clear representaion in QTableView."""

    # str
    if isinstance(number, str):
        return number

    # int number
    if isinstance(number, int):
        return str(number)

    # float number
    if np.isclose(number, 0):
        return '0'

    if np.isnan(number) or np.isinf(number):
        return ''

    n_digits = len(f'{number}'.split('.')[-1])
    if n_digits <= precision:
        result = f'{number:0.{n_digits}f}'
        result = result.rstrip('0').rstrip('.')
        return result

    if round(number, precision) == round(number, precision + 5):
        result = f'{round(number, precision)}'
        result = result.rstrip('0').rstrip('.')
        return result

    result = f'{number:0.{precision}f}'
    return result


def restrict_number(
    number: float,
    lims: tuple[float, float],
    verbose: bool = False,
) -> str:
    """Restrict `number` with the given 'lims'.

    Params:
        lims - range of restriction limits;
        verbose - show formatted value in brackets.
    """
    c_min, c_max = lims
    template = '{sign} {lim} ({verbose})' if verbose else '{sign} {lim}'

    if number < c_min:
        return template.format(
            sign='<',
            lim=format_number(c_min),
            verbose={format_number(number, precision=4)},
        )

    if number > c_max:
        return template.format(
            sign='>',
            lim=format_number(c_max),
            verbose={format_number(number, precision=4)},
        )

    return format_number(number)


def restrict_numbers(
    numbers: Array,
    lims: tuple[float, float],
    tolerance: int = 0,
    verbose: bool = False,
) -> Array:
    """Restrict `numbers` with the given `lims` and `tolerance` (допуск). Values out of the limits are formated only.

    Params:
        lims - range of restriction limits;
        tolerance - tolerance (in percent);
        verbose - show formatted value in brackets.
    """
    c_min, c_max = lims

    result = numbers.copy()
    result = result.astype(str)

    # restrict numbers
    cond = numbers < c_min*(1 - tolerance/100)
    result[cond] = [
        restrict_number(number, lims=lims, verbose=verbose)
        for number in numbers[cond]
    ]

    cond = numbers > c_max*(1 + tolerance/100)
    result[cond] = [
        restrict_number(number, lims=lims, verbose=verbose)
        for number in numbers[cond]
    ]

    return result


def truncate_number(
    number: Any,
    n: int = 4,
) -> str:
    """Truncate `number` for clear representaion in QTableView."""

    try:
        number = f'{float(number):.12f}'
    except (ValueError, TypeError):
        return ''

    if number[:4] == '0.00':
        number = f'{float(number):.2e}'

    else:
        integer, fractional = number.split('.')

        if len(integer) > 3:
            n -= len(integer) - 3
        if n < 0:
            n = 0

        number = '.'.join([integer, fractional[:n]])
        number = number.rstrip('0').rstrip('.')  # strip excess sep and zeros

    return number
