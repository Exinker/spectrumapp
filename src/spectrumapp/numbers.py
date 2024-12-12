import numpy as np

from spectrumapp.types import Array


def format_number(__value: float, precision: int = 4) -> str:
    """Format the value for clear representaion in TableView."""

    try:
        value = np.format_float_positional(__value)
    except Exception:
        raise ValueError(f'The value {__value} could not be formatted!')

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


def restrict_number(__value: float, lims: tuple[float, float], verbose: bool = False) -> str:
    """Restrict the value with the given limits.

    Params:
        lims - range of restriction limits;
        verbose - show formatted value in brackets.
    """
    c_min, c_max = lims

    # restrict cases
    template = '{sign} {lim} ({verbose})' if verbose else '{sign} {lim}'

    if __value < c_min:
        sign = '<'
        lim = format_number(c_min)

        return template.format(sign=sign, lim=lim, verbose={format_number(__value, precision=4)})

    if __value > c_max:
        sign = '>'
        lim = format_number(c_max)

        return template.format(sign=sign, lim=lim, verbose={format_number(__value, precision=4)})

    # otherwise
    return format_number(__value)


def restrict_numbers(__values: Array, lims: tuple[float, float], tolerance: int = 0, verbose: bool = False) -> Array:
    """Restrict the values with the given limits and tolerance (допуск). Values out of the limits are formated only.

    Params:
        lims - range of restriction limits;
        tolerance - tolerance (in percent);
        verbose - show formatted value in brackets.
    """
    c_min, c_max = lims

    result = __values.copy()
    result = result.astype(str)

    # restrict numbers
    cond = __values < c_min*(1 - tolerance/100)
    result[cond] = [
        restrict_number(value, lims=lims, verbose=verbose)
        for value in __values[cond]
    ]

    cond = __values > c_max*(1 + tolerance/100)
    result[cond] = [
        restrict_number(value, lims=lims, verbose=verbose)
        for value in __values[cond]
    ]

    #
    return result


def truncate_number(value: float, n=4) -> str:
    """Truncate number for clear representaion in TableView."""

    try:
        value = f'{float(value):.12f}'

        if value[:4] == '0.00':
            value = f'{float(value):.2e}'

        else:
            integer, fractional = value.split('.')

            if len(integer) > 3:
                n -= len(integer) - 3
            if n < 0:
                n = 0

            value = '.'.join([integer, fractional[:n]])
            value = value.rstrip('0').rstrip('.')  # strip excess sep and zeros

        return value

    except (ValueError, TypeError):
        return ''
