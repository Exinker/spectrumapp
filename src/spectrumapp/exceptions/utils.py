import sys
import traceback


def format_exception(limit: int = 2) -> str:
    return traceback.format_exc(limit=limit)


def eprint(msg: str | None = None, info: str | None = None) -> None:
    """Print exception traceback to stdout."""
    template = '{info}' if msg is None else '{msg}{info}'

    info = info or format_exception()
    text = template.format(
        msg=msg,
        info=info,
    )

    print(text, file=sys.stdout)
