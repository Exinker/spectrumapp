import pytest
from PySide6 import QtCore, QtWidgets
from pytestqt.qtbot import QtBot



@pytest.fixture(params=['window'])
def object_name(request) -> str:
    return request.param


class TestedWindow(QtWidgets.QWidget):

    refreshed = QtCore.Signal()

    def __init__(self, *args, objectName: str, **kwargs):  # noqa: N803
        super().__init__(*args, **kwargs)

        self.setObjectName(objectName)

        self.refreshed.connect(self.on_refreshed)

    def on_refreshed(self) -> None:
        pass


@pytest.fixture(scope='function')
def window(
    object_name: str,
    qtbot: QtBot,
) -> TestedWindow:

    window = TestedWindow(
        objectName=object_name,
    )
    return window
