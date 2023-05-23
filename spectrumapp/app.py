'''

TODO:
    - pluging for `Read Mode` control (read by timetable)
    - alerts for `Read Dark Signal` control (update signal)

    - logging device operations
'''

import logging
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

from core.configs import ORGANIZATION_NAME, APPLICATION_NAME, APPLICATION_VERSION
from core.configs import Config
from core.loggings import setdefault_logging, log
from core.routing import pave



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

        layout.addStretch()
        layout.addWidget(EmptyWidget())


class CentralWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        layout.addWidget(
            EmptyFrame(parent=self)
        )


class Window(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        config = Config.from_json()

        # style        
        filepath = pave(os.path.join('.', 'static', 'app.css'))
        style = open(filepath, 'r').read()
        self.setStyleSheet(style)

        # icon
        filepath = pave(os.path.join('.', 'static', 'icon.ico'))
        icon = QtGui.QIcon(filepath)
        self.setWindowIcon(icon)

        # title
        title = f'{APPLICATION_NAME} - [{config.filepath}]'
        self.setWindowTitle(title)

        # widget
        widget = CentralWidget(parent=self)
        self.setCentralWidget(widget)

        #
        self.show()

    @log(msg='close app')
    def closeEvent(self, event: QtCore.QEvent):
        return super().closeEvent(event)


class Application(QtWidgets.QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setOrganizationName(ORGANIZATION_NAME)
        self.setApplicationName(APPLICATION_NAME)
        self.setApplicationVersion(APPLICATION_VERSION)

        #
        self.window = None

    @log(msg='run app')
    def run(self):

        # config
        config = Config.default()
        config.to_json()

        # window
        self.window = Window()

    @log(msg='refresh app')
    def refresh(self):
        '''Refresh all windows and widgets of an application.'''

        # refresh
        self.window._onRefreshAction()

    @log(msg='reset app')
    def reset(self, refresh: bool = True):
        '''Update setting, config and refresh the app.'''

        # reset 
        pass

        # refresh (windows and widgets)
        if refresh:
            self.window._onRefreshAction()


if __name__ == '__main__':

    # logging
    setdefault_logging()

    # app
    app = Application(sys.argv)
    app.run()

    # exit
    sys.exit(app.exec())
