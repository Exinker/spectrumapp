from unittest.mock import Mock

import pytest
from pytestqt.qtbot import QtBot

from spectrumapp.windows.main_window import BaseMainWindow


class FakeMainWindow(BaseMainWindow):

    def __init__(self, *args, **kwargs):

        self.on_refreshed_mock = Mock()
        self.on_resetted_mock = Mock()
        self.on_directory_opened_mock = Mock()

        super().__init__(*args, **kwargs)

    def on_refreshed(self, *args, **kwargs):  # noqa: N802
        self.on_refreshed_mock(*args, **kwargs)

    def on_resetted(self, *args, **kwargs):  # noqa: N802
        self.on_resetted_mock(*args, **kwargs)

    def on_directory_opened(self, *args, **kwargs):  # noqa: N802
        self.on_directory_opened_mock(*args, **kwargs)


@pytest.fixture
def main_window(
    monkeypatch: pytest.MonkeyPatch,
    qtbot: QtBot,
) -> FakeMainWindow:
    monkeypatch.setattr('time.sleep', lambda *args, **kwargs: ...)

    main_window = FakeMainWindow(
        show=True,
    )
    qtbot.addWidget(main_window)
    qtbot.wait_until(main_window.isVisible)
    main_window.activateWindow()
    main_window.setFocus()
    qtbot.wait(100)

    yield main_window

    main_window.close()
