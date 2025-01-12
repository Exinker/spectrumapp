import sys
import traceback
from typing import TextIO


def format_exception(limit: int = 2) -> str:
    return traceback.format_exc(limit=limit)


def eprint(
    message: str = '',
    info: str = '',
    file: TextIO = sys.stdout,
) -> None:
    """Print exception traceback to file."""

    template = _get_text_template(
        message=message,
    )
    text = template.format(
        message=message,
        info=info or format_exception(),
    )

    print(text, file=file)


def _get_text_template(message: str) -> str:

    if message:
        return '{message}{info}'
    return '{info}'
