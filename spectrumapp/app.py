
import sys

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.core.config import setdefault_config, APPLICATION_NAME, APPLICATION_VERSION, ORGANIZATION_NAME, DEBUG
from spectrumapp.core.logging import setdefault_logging, log
from spectrumapp.core.setting import setdefault_setting
from spectrumapp.utils.modifier import wait, attempt
from spectrumapp.window.window import BaseMainWindow
from spectrumapp.window.splashScreenWindow import splashscreen


class EmptyWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedHeight(200)


class EmptyFrame(QtWidgets.QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedWidth(320)
        self.setFixedHeight(480)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)


class EmptyCentralWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        layout.addWidget(
            EmptyFrame(parent=self)
        )

    @wait
    @attempt()
    def _onResetAction(self, refresh: bool = True):
        """Reset the widget all sub widget."""
        pass
    
        if refresh:
            self._onRefreshAction()

    @wait
    @attempt()
    def _onRefreshAction(self):
        """Refresh the widget and all sub widgets."""
        pass


class Window(BaseMainWindow):

    def __init__(self, *args, show: bool = False, **kwargs):
        super().__init__(*args, show=show, **kwargs)

        # actions
        self._setdefault_actions()

        # menubar
        self._setdefault_menubar()

        # widget
        widget = EmptyCentralWidget(parent=self)
        self.setCentralWidget(widget)

        #
        self.show()


class Application(QtWidgets.QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setOrganizationName(ORGANIZATION_NAME)
        self.setApplicationName(APPLICATION_NAME)
        self.setApplicationVersion(APPLICATION_VERSION)

        #
        self.window = None

    @wait
    @splashscreen()
    @log(msg='app: run', debug=DEBUG)
    def run(self):
        self.window = Window()

    @wait
    @log(msg='app: refresh', debug=DEBUG)
    def refresh(self):
        """Refresh all windows and widgets of an application."""

        # refresh
        self.window._onRefreshAppAction()

    @wait
    @splashscreen()
    @log(msg='app: reset', debug=DEBUG)
    def reset(self, refresh: bool = True):
        """Update setting, config and refresh the app."""

        # reset 
        pass

        # refresh (windows and widgets)
        if refresh:
            self.window._onRefreshAppAction()


if __name__ == '__main__':

    # config
    setdefault_config()

    # setting
    setdefault_setting()

    # logging
    setdefault_logging()

    # app
    app = Application(sys.argv)
    app.run()

    # exit
    sys.exit(app.exec())
