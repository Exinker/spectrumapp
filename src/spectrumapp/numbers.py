from typing import Any

import numpy as np

from spectrumapp.types import Array


def format_number(number: float, precision: int = 4) -> str:
    """Format the value for clear representaion in TableView."""

    try:
        value = np.format_float_positional(number)
    except Exception:
        raise ValueError(f'The value {number} could not be formatted!')

    # int value
    if value.endswith('.'):
        result = value.rstrip('.')

        return result

    # float value
    value = float(value)

    # float value / check: zero value
    if value == 0:
        return '0'

    # float value / check: missing values
    if np.isnan(value) or np.isinf(value):
        return ''

    # float value / check: n_digits
    n_digits = len(f'{value}'.split('.')[-1])
    if n_digits <= precision:
        result = f'{value:0.{n_digits}f}'
        result = result.rstrip('0').rstrip('.')
        return result

    # float value / check: floating point error
    if round(value, precision) == round(value, precision + 5):
        result = f'{round(value, precision)}'
        result = result.rstrip('0').rstrip('.')
        return result

    # float value / check: otherwise
    result = f'{value:0.{precision}f}'
    return result


def restrict_number(number: float, lims: tuple[float, float], verbose: bool = False) -> str:
    """Restrict the value with the given limits.

    Params:
        lims - range of restriction limits;
        verbose - show formatted value in brackets.
    """
    c_min, c_max = lims

    # restrict cases
    template = '{sign} {lim} ({verbose})' if verbose else '{sign} {lim}'

    if number < c_min:
        sign = '<'
        lim = format_number(c_min)

        return template.format(sign=sign, lim=lim, verbose={format_number(number, precision=4)})

    if number > c_max:
        sign = '>'
        lim = format_number(c_max)

        return template.format(sign=sign, lim=lim, verbose={format_number(number, precision=4)})

    # otherwise
    return format_number(number)


def restrict_numbers(numbers: Array, lims: tuple[float, float], tolerance: int = 0, verbose: bool = False) -> Array:
    """Restrict the values with the given limits and tolerance (допуск). Values out of the limits are formated only.

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


def truncate_number(number: Any, n=4) -> str:
    """Truncate number for clear representaion in TableView."""

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
