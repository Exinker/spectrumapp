import os

from spectrumapp.windows.splash_screen_window import SplashScreenWindow


def test_splash_screen_window(
    splash_screen_window: SplashScreenWindow,
):

    assert splash_screen_window.objectName() == 'splashScreenWindow'
    assert splash_screen_window.windowFlags() == SplashScreenWindow.DEFAULT_FLAGS
    assert splash_screen_window.styleSheet() == open(
        file=os.path.join('.', 'static', 'splash-screen-window.css'),
        mode='r',
    ).read()
    # assert splash_screen_window.windowIcon() == QtGui.QIcon(
    #     fileName=os.path.join('.', 'static', 'icon.ico'),
    # )  # как сравнить иконки?
    assert splash_screen_window.size() == splash_screen_window.DEFAULT_SIZE
