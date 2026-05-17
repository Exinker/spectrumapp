from unittest.mock import Mock

import pytest
from PySide6 import QtCore, QtWidgets
from pytestqt.qtbot import QtBot


@pytest.fixture(params=['window'])
def object_name(request) -> str:
    return request.param


class FakeWindow(QtWidgets.QWidget):

    refreshed = QtCore.Signal()

    def __init__(self, *args, objectName: str, **kwargs):  # noqa: N803
        self.close_mock = Mock()
        self.on_refreshed_mock = Mock()

        super().__init__(*args, **kwargs)

        self.setObjectName(objectName)

        self.refreshed.connect(self.on_refreshed)

    def on_refreshed(self) -> None:
        self.on_refreshed_mock()

    def close(self) -> bool:
        self.close_mock()
        return super().close()


@pytest.fixture(scope='function')
def window(
    object_name: str,
    qtbot: QtBot,
) -> FakeWindow:
    window = FakeWindow(
        objectName=object_name,
    )
    qtbot.addWidget(window)

    return window
