import os

from PySide6 import QtCore, QtGui, QtWidgets
from pytestqt.qtbot import QtBot

from spectrumapp.windows.splash_screen_window import SplashScreenWindow


def test_splash_screen_window(
    splash_screen_window: SplashScreenWindow,
    qtbot: QtBot,
):

    assert splash_screen_window.objectName() == 'splashScreenWindow'
    assert splash_screen_window.windowFlags() == SplashScreenWindow.DAFAULT_FLAGS
    assert_style(
        window=splash_screen_window,
        style=open(os.path.join('.', 'static', 'splash-screen-window.css'), 'r').read(),
    )
    # assert_icon(
    #     window=splash_screen_window,
    #     icon=QtGui.QIcon(os.path.join('.', 'static', 'icon.ico')),
    # )
    assert_size(
        window=splash_screen_window,
        size=QtCore.QSize(680, 400),
    )


def assert_style(
    window: QtWidgets.QWidget,
    style: str,
):
    assert window.styleSheet() == style


def assert_icon(
    window: QtWidgets.QWidget,
    icon: QtGui.QIcon,
):
    assert window.windowIcon() == icon


def assert_size(
    window: QtWidgets.QWidget,
    size: QtCore.QSize,
):
    assert window.size() == size
