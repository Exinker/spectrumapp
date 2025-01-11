import sys
import traceback
from typing import TextIO


def format_exception(limit: int = 2) -> str:
    return traceback.format_exc(limit=limit)


def eprint(
    message: str | None = None,
    info: str | None = None,
    file: TextIO = sys.stdout,
) -> None:
    """Print exception traceback to file."""
    template = '{info}' if message is None else '{msg}{info}'

    info = info or format_exception()
    text = template.format(
        msg=message,
        info=info,
    )

    print(text, file=file)
