
import sys
import traceback


def format_exception() -> str:
    return traceback.format_exc(limit=2)


def eprint(msg: str, info: str | None = None) -> None:
    """Print exception traceback to stdout."""
    template = '{info}' if msg is None else '{message}{info}'

    info = format_exception() if info is None else info
    text = template.format(
        msg=msg,
        info=info,
    )

    print(text, file=sys.stdout)
