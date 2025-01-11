import pytest
from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.progress_window import ProgressWindow


@pytest.fixture(params=[True, False])
def parent_widget(
    request,
    qtbot: QtBot,
) -> QtWidgets.QFrame | None:
    is_exists = request.param

    if is_exists:
        parent_widget = QtWidgets.QFrame()
        QtWidgets.QVBoxLayout(parent_widget)

        return parent_widget
    return None


def test_progress_window_with_parent(
    parent_widget: QtWidgets.QFrame | None,
    qtbot: QtBot,
):
    progress_window = ProgressWindow(
        parent=parent_widget,
    )

    progress_window.close()

    assert progress_window.parent() is None
