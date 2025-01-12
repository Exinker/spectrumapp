import pytest
from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.widgets.fold_widget import FoldWidget


@pytest.fixture
def title() -> str:
    return 'test'


@pytest.fixture
def is_folded() -> bool:
    return True


@pytest.fixture
def wrapped_widget(
    qtbot: QtBot,
) -> QtWidgets.QLabel:
    return QtWidgets.QLabel(
        text='test',
        objectName='widget',
    )


@pytest.fixture(params=[True, False])
def parent_widget(
    request,
    qtbot: QtBot,
) -> QtWidgets.QWidget:
    is_exists = request.param

    if is_exists:
        parent_widget = QtWidgets.QFrame()
        QtWidgets.QVBoxLayout(parent_widget)

        return parent_widget
    return None


@pytest.fixture
def fold_widget(
    wrapped_widget: QtWidgets.QWidget,
    parent_widget: QtWidgets.QWidget | None,
    title: str,
    is_folded: bool,
    qtbot: QtBot,
) -> FoldWidget:

    fold_widget = FoldWidget(
        wrapped_widget,
        title=title,
        is_folded=is_folded,
    )

    if parent_widget:
        layout = parent_widget.layout()
        layout.addWidget(fold_widget)

    return fold_widget
