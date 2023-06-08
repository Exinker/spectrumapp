
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.core.config import setdefault_config
from spectrumapp.core.logging import setdefault_logging, log
from spectrumapp.core.setting import setdefault_setting, get_setting, set_setting
from spectrumapp.core.utils import pave
from spectrumapp.utils.find import find_window
from spectrumapp.utils.modifier import wait, attempt, MessageLevel
from spectrumapp.window.splashScreenWindow import splashscreen


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
    def reset(self, refresh: bool = True):
        """Reset the widget all sub widget."""
        pass
    
        if refresh:
            self.refresh()

    @wait
    @attempt()
    def refresh(self):
        """Refresh the widget and all sub widgets."""
        pass


class BaseMainWindow(QtWidgets.QMainWindow):

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
        filepath = ''
        title = f'{APPLICATION_NAME} - [{filepath}]'
        self.setWindowTitle(title)

        # widget
        widget = EmptyCentralWidget(parent=self)
        self.setCentralWidget(widget)

        # menu
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        action = QtGui.QAction('&Open', self)
        action.setShortcut('Ctrl+O')
        action.setStatusTip('Open file...')
        action.triggered.connect(self._onOpenAction)
        fileMenu.addAction(action)
        fileMenu.addSeparator()
        action = QtGui.QAction('&Refresh', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+R'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self._onRefreshAppAction)
        fileMenu.addAction(action)
        action = QtGui.QAction('&Reset', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Shift+R'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self._onResetAppAction)
        fileMenu.addAction(action)
        fileMenu.addSeparator()
        action = QtGui.QAction('&Quit', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Q'))
        action.setStatusTip('Quit')
        action.triggered.connect(self._onQuitAction)
        fileMenu.addAction(action)

        instrumentsMenu = menuBar.addMenu('&Instruments')
        # action = QtGui.QAction('&Filtrate', self)
        # action.setShortcut(QtGui.QKeySequence('Ctrl+F'))
        # action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        # action.setStatusTip('Filtrate probes by condition...')
        # action.triggered.connect(self._onOpenFiltrateWindowAction)
        # instrumentsMenu.addAction(action)

        helpMenu = menuBar.addMenu('&Help')
        action = QtGui.QAction('&Help', self)
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self._onOpenHelpWindowAction)
        helpMenu.addAction(action)
        # action = QtGui.QAction('&Report Issue', self)
        # action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        # action.triggered.connect(self._onOpenReportIssueWindowAction)
        # helpMenu.addAction(action)
        action = QtGui.QAction('&About', self)
        action.triggered.connect(self._onOpenAboutWindowAction)
        helpMenu.addAction(action)

        # geometry
        geometry = get_setting(key=f'geometry/{self.objectName()}')
        if geometry:
            self.setGeometry(geometry)
            self.setWindowState(QtCore.Qt.WindowActive)
        else:
            self.setWindowState(QtCore.Qt.WindowMaximized | QtCore.Qt.WindowActive)

        #
        self.show()

    # --------        slots        --------
    @wait
    def _onOpenAction(self):
        """Open new file action."""

        # settings
        filedir = QtWidgets.QFileDialog().getExistingDirectory(
            parent=self,
            caption='Choose directory with Atom\'s dump file:',
            dir=os.path.join(os.getcwd(), 'data'),
        )

        #
        files = ('dump.pkl', )
        if any([os.path.isfile(os.path.join(filedir, file)) for file in files]):
            filedir = os.path.abspath(filedir)
            head, tail = os.path.split(filedir)

            # update settings
            set_setting(
                key='config/filedir',
                value=filedir,
            )
            set_setting(
                key='config/filename',
                value=tail,
            )
            setdefault_setting()

            # reset app
            self._onResetAppAction()

    @wait
    @splashscreen(delay=5)
    def _onResetAppAction(self, *args, **kwargs):
        '''An action occurs due to change file.'''

        # reset app
        app = QtWidgets.QApplication.instance()
        app.reset()

        # update title
        filedir = ''
        title = f"{APPLICATION_NAME} - [{filedir}]"
        self.setWindowTitle(title)

        # reset windows
        for window in app.topLevelWidgets():
            window_name = window.objectName()

            if window_name in ('mainWindow',):
                pass
            else:
                window.close()

    @wait
    def _onRefreshAppAction(self, *args, **kwargs):
        """Refresh the widgets at the window and refresh all sub windows."""
        app = QtWidgets.QApplication.instance()

        for window in app.topLevelWidgets():
            window_name = window.objectName()

            # update core window
            if window_name in ('mainWindow',):
                window.centralWidget().refresh()

            # update instrument windows
            pass

            # close info windows
            if window_name in ('filtrationWindow', 'helpWindow', 'reportIssueWindow', 'aboutWindow'):
                window.close()

    @wait
    def _onQuitAction(self):
        self.close()

    @wait
    @attempt(level=MessageLevel.error)
    def _onOpenHelpWindowAction(self):
        window_name = 'helpWindow'

        window = find_window(window_name)
        if window is not None:
            window.show()

        else:
            window = HelpWindow(
                parent=self,
                flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
            )

    @wait
    @attempt(level=MessageLevel.error)
    def _onOpenAboutWindowAction(self):
        window_name = 'aboutWindow'

        window = find_window(window_name)
        if window is not None:
            window.show()

        else:
            window = AboutWindow(
                parent=self,
                flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
            )

    # --------        events        --------
    @log(msg='app: close event')
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

    @wait
    @splashscreen()
    @log(msg='app: run')
    def run(self):

        # window
        self.window = BaseMainWindow()

    @wait
    @log(msg='app: refresh')
    def refresh(self):
        """Refresh all windows and widgets of an application."""

        # refresh
        self.window._onRefreshAppAction()

    @wait
    @splashscreen()
    @log(msg='app: reset')
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
