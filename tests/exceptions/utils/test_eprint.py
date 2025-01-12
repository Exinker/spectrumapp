from pathlib import Path

import pytest

from spectrumapp.exceptions import eprint, format_exception
from spectrumapp.exceptions.utils import _get_text_template


@pytest.fixture()
def expected(
    message: str,
    info: str,
) -> str:

    return _get_text_template(
        message=message,
    ).format(
        message=message,
        info=info or format_exception(),
    ) + '\n'


def test_eprint(
    message: str,
    info: str,
    expected: str,
    tmp_path: Path,
):
    filepath = tmp_path / 'text.txt'

    eprint(
        message=message,
        info=info,
        file=open(filepath, 'w'),
    )

    assert open(filepath, 'r').read() == expected
