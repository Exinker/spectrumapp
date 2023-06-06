"""

TODO:
    - pluging for `Read Mode` control (read by timetable)
    - alerts for `Read Dark Signal` control (update signal)

    - logging device operations
"""

import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.core.config import setdefault_config
from spectrumapp.core.logging import setdefault_logging, log
from spectrumapp.core.setting import setdefault_setting, get_setting, set_setting
from spectrumapp.core.utils import pave
from spectrumapp.windows.splashScreenWindow import splashscreen


APPLICATION_NAME = os.environ.get('APPLICATION_NAME', '')
APPLICATION_VERSION = os.environ.get('APPLICATION_VERSION', '')
ORGANIZATION_NAME = os.environ.get('ORGANIZATION_NAME', '')


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


class CentralWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        layout.addWidget(
            EmptyFrame(parent=self)
        )


class MainWindow(QtWidgets.QMainWindow):

    @splashscreen(progress=70, info='<strong>LOADING</strong> user interface...')
    def __init__(self, *args, **kwargs):
        super().__init__(objectName='mainWindow', *args, **kwargs)

        # style
        filepath = pave(os.path.join('.', 'static', 'app.css'))
        style = open(filepath, 'r').read()
        self.setStyleSheet(style)

        # icon
        filepath = pave(os.path.join('.', 'static', 'icon.ico'))
        icon = QtGui.QIcon(filepath)
        self.setWindowIcon(icon)

        # title
        filepath = get_setting(key='config/filepath')
        title = f'{APPLICATION_NAME} - [{filepath}]'
        self.setWindowTitle(title)

        # widget
        widget = CentralWidget(parent=self)
        self.setCentralWidget(widget)

        # geometry
        geometry = get_setting(key=f'geometry/{self.objectName()}')
        if geometry:
            self.setGeometry(geometry)
            self.setWindowState(QtCore.Qt.WindowActive)
        else:
            self.setWindowState(QtCore.Qt.WindowMaximized | QtCore.Qt.WindowActive)

        #
        self.show()

    def _onRefreshAction(self):
        """Refresh the widgets at the window and refresh all sub windows."""
        pass

    @log(msg='close app')
    def closeEvent(self, event: QtCore.QEvent):

        # geometry
        set_setting(key=f'geometry/{self.objectName()}', value=self.geometry())

        #
        return super().closeEvent(event)


class Application(QtWidgets.QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setOrganizationName(ORGANIZATION_NAME)
        self.setApplicationName(APPLICATION_NAME)
        self.setApplicationVersion(APPLICATION_VERSION)

        #
        self.window = None

    @splashscreen()
    @log(msg='run app')
    def run(self):

        # window
        self.window = MainWindow()

    @log(msg='refresh app')
    def refresh(self):
        """Refresh all windows and widgets of an application."""

        # refresh
        self.window._onRefreshAction()

    @splashscreen()
    @log(msg='reset app')
    def reset(self, refresh: bool = True):
        """Update setting, config and refresh the app."""

        # reset 
        pass

        # refresh (windows and widgets)
        if refresh:
            self.window._onRefreshAction()


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
