import os

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.loggers import log
from spectrumapp.paths import pave
from spectrumapp.settings import get_setting, set_setting
from spectrumapp.utils.finder import find_action, find_window
from spectrumapp.utils import handler
from spectrumapp.windows.exceptionWindow import ExceptionLevel
from spectrumapp.windows.keyboardShortcutsWindow import BaseKeyboardShortcutsWindow
from spectrumapp.windows.reportIssueWindow import ReportIssueWindow


class BaseMainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, maximize: bool = False, object_name: str | None = None, show: bool = False, **kwargs):
        object_name = object_name or 'mainWindow'

        super().__init__(*args, objectName=object_name, **kwargs)

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
        title = '{name} - [{filepath}]'.format(
            name=os.environ['APPLICATION_NAME'],
            filepath=filepath,
        )
        self.setWindowTitle(title)

        # actions
        action = QtGui.QAction('&Open...', self)
        action.setShortcut('Ctrl+O')
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.setToolTip('Open file...')
        action.triggered.connect(self._onOpenTriggered)
        self.addAction(action)

        action = QtGui.QAction('&Refresh', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+R'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self._onRefreshTriggered)
        self.addAction(action)

        action = QtGui.QAction('&Reset', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Shift+R'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self._onResetTriggered)
        self.addAction(action)

        action = QtGui.QAction('&Quit', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Q'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.setStatusTip('Quit')
        action.triggered.connect(self._onQuitTriggered)
        self.addAction(action)

        action = QtGui.QAction('&View Help', self)
        action.setEnabled(False)
        action.triggered.connect(self._onOpenHelpWindowTriggered)
        self.addAction(action)

        action = QtGui.QAction('&Report Issue', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Shift+I'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self._onOpenReportIssueWindowTriggered)
        self.addAction(action)

        action = QtGui.QAction('&Keyboard Shortcuts', self)
        action.triggered.connect(self._onOpenKeyboardShortcutsWindowTriggered)
        self.addAction(action)

        action = QtGui.QAction('&About', self)
        action.setEnabled(False)
        action.triggered.connect(self._onOpenAboutWindowTriggered)
        self.addAction(action)

        # menus
        menubar = self.menuBar()
        menubar.setVisible(get_setting(key='mainWindow/menubar') or True)

        menu = QtWidgets.QMenu(title='&File', parent=self)
        menu.addAction(find_action(self, '&Open...'))
        menu.addSeparator()
        menu.addAction(find_action(self, '&Refresh'))
        menu.addAction(find_action(self, '&Reset'))
        menu.addSeparator()
        menu.addAction(find_action(self, '&Quit'))
        menubar.addMenu(menu)

        menu = QtWidgets.QMenu(title='&Instruments', parent=self)
        menu.setEnabled(False)
        menubar.addMenu(menu)

        menu = QtWidgets.QMenu(title='&Settings', parent=self)
        menu.setEnabled(False)
        menubar.addMenu(menu)

        menu = QtWidgets.QMenu(title='&Help', parent=self)
        menu.addAction(find_action(self, '&View Help'))
        menu.addAction(find_action(self, '&Report Issue'))
        menu.addSeparator()
        menu.addAction(find_action(self, '&Keyboard Shortcuts'))
        menu.addAction(find_action(self, '&About'))
        menubar.addMenu(menu)

        # geometry
        geometry = get_setting(key=f'geometry/{self.objectName()}')
        state = QtCore.Qt.WindowActive
        if geometry:
            self.setGeometry(geometry)
            self.setWindowState(state)
        else:
            if maximize:
                state = state | QtCore.Qt.WindowMaximized
            self.setWindowState(state)

        #
        if show:
            self.show()

    # --------        slots        --------
    @log(message='main-window: open action')
    @handler.wait
    def _onOpenTriggered(self):
        """Open new file action."""
        pass

    @log(message='main-window: reset action')
    @handler.wait
    def _onRefreshTriggered(self, *args, **kwargs):
        """Refresh the app."""
        pass

    @log(message='main-window: reset action')
    @handler.wait
    def _onResetTriggered(self, *args, **kwargs):
        """Update settings, config and refresh (optionally) the app."""
        pass

    @log(message='main-window: quit action')
    @handler.wait
    def _onQuitTriggered(self):
        self.close()

    @log(message='main-window: report issue')
    @handler.wait
    def _onOpenReportIssueWindowTriggered(self, *args, **kwargs):
        """Report an issue."""

        window = find_window('reportIssueWindow')
        if window is not None:
            window.show()
        else:
            window = ReportIssueWindow(
                parent=self,
                flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
            )

    @log(message='main-window: open help-window')
    @handler.wait
    @handler.attempt(level=ExceptionLevel.error)
    def _onOpenHelpWindowTriggered(self):
        window_name = 'helpWindow'

        window = find_window(window_name)
        if window is not None:
            window.show()

        else:
            raise NotImplementedError
            # window = HelpWindow(
            #     parent=self,
            #     flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
            # )

    @log(message='main-window: open keyboard-shortcuts-window')
    @handler.wait
    @handler.attempt(level=ExceptionLevel.error)
    def _onOpenKeyboardShortcutsWindowTriggered(self):
        window_name = 'keyboardShortcutsWindow'

        window = find_window(window_name)
        if window is not None:
            window.show()

        else:
            window = BaseKeyboardShortcutsWindow(
                parent=self,
                flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
            )

    @log(message='main-window: open about-window')
    @handler.wait
    @handler.attempt(level=ExceptionLevel.error)
    def _onOpenAboutWindowTriggered(self):
        window_name = 'aboutWindow'

        window = find_window(window_name)
        if window is not None:
            window.show()

        else:
            raise NotImplementedError
            # window = AboutWindow(
            #     parent=self,
            #     flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
            # )

    # --------        events        --------
    @log(message='main-window: close event')
    def closeEvent(self, event: QtCore.QEvent):

        # geometry
        set_setting(key=f'geometry/{self.objectName()}', value=self.geometry())

        #
        super().closeEvent(event)
