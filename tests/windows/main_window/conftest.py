import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.windows.main_window import BaseMainWindow


@pytest.fixture
def main_window(
    monkeypatch: pytest.MonkeyPatch,
    qtbot: QtBot,
) -> BaseMainWindow:
    monkeypatch.setattr('time.sleep', lambda *args, **kwargs: ...)

    main_window = BaseMainWindow(
        show=True,
    )
    qtbot.wait_until(main_window.isVisible)

    return main_window
