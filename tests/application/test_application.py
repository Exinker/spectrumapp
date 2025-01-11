import os

from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot


def test_application(
    qtbot: QtBot,
):
    app = QtWidgets.QApplication.instance()

    assert app.applicationName() == os.environ['APPLICATION_NAME']
    assert app.applicationVersion() == os.environ['APPLICATION_VERSION']
    assert app.organizationName() == os.environ['ORGANIZATION_NAME']
