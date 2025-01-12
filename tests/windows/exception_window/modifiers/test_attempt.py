from typing import Never, Type

import pytest

from spectrumapp.windows.exception_window import ExceptionLevel, attempt


@pytest.fixture(params=[ZeroDivisionError])
def exception(request) -> Exception:
    return request.param


@attempt()
def func(__exception: Type[Exception]) -> Never:
    raise __exception


def test_attempt(
    exception: Exception,
    mocker,
):
    mock = mocker.patch('spectrumapp.windows.exception_window.modifiers.ExceptionDialog')

    func(exception)

    mock.assert_called_once_with(
        message=f'The attempt to complete {func.__name__} failed.',
        level=ExceptionLevel.ERROR,
    )
