import os

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.helpers import find_action, find_window
from spectrumapp.loggers import log
from spectrumapp.paths import pave
from spectrumapp.settings import get_setting, set_setting
from spectrumapp.windows.exception_window import ExceptionLevel, attempt
from spectrumapp.windows.keyboard_shortcuts_window import BaseKeyboardShortcutsWindow
from spectrumapp.windows.modifiers import wait
from spectrumapp.windows.report_issue_window import ReportIssueWindow


class BaseMainWindow(QtWidgets.QMainWindow):

    refreshed = QtCore.Signal()
    reseted = QtCore.Signal()

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

        # signals
        self.refreshed.connect(self.on_refreshed)
        self.reseted.connect(self.on_resetted)

        # actions
        action = QtGui.QAction('&Open...', self)
        action.setShortcut('Ctrl+O')
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.setToolTip('Open file...')
        action.triggered.connect(self.on_directory_opened)
        self.addAction(action)

        action = QtGui.QAction('&Refresh', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+R'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self.on_refreshed)
        self.addAction(action)

        action = QtGui.QAction('&Reset', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Shift+R'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self.on_resetted)
        self.addAction(action)

        action = QtGui.QAction('&Quit', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Q'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.setStatusTip('Quit')
        action.triggered.connect(self.on_closed)
        self.addAction(action)

        action = QtGui.QAction('&View Help', self)
        action.setEnabled(False)
        action.triggered.connect(self.on_help_window_opened)
        self.addAction(action)

        action = QtGui.QAction('&Report Issue', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Shift+I'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self.on_report_issue_window_opened)
        self.addAction(action)

        action = QtGui.QAction('&Keyboard Shortcuts', self)
        action.triggered.connect(self.on_keyboard_shortcuts_window_opened)
        self.addAction(action)

        action = QtGui.QAction('&About', self)
        action.setEnabled(False)
        action.triggered.connect(self.on_about_window_opened)
        self.addAction(action)

        # menus
        menubar = self.menuBar()
        menubar.setVisible(get_setting(key='mainWindow/menubar') or False)

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

    @log(message='main-window: refresh action')
    @wait
    def on_refreshed(self, *args, **kwargs):
        """Refresh the app."""
        self.not_implemented_plug(*args, **kwargs)

    @log(message='main-window: reset action')
    @wait
    def on_resetted(self, *args, **kwargs):
        """Update settings, config and refresh (optionally) the app."""
        self.not_implemented_plug(*args, **kwargs)

    @log(message='main-window: quit action')
    @wait
    def on_closed(self):
        self.close()

    @log(message='main-window: open action')
    @wait
    def on_directory_opened(self, *args, **kwargs):
        """Open new directory action."""
        self.not_implemented_plug(*args, **kwargs)

    @log(message='main-window: open report-issue-window')
    @wait
    def on_report_issue_window_opened(self, *args, **kwargs):
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
    @wait
    @attempt(level=ExceptionLevel.ERROR)
    def on_help_window_opened(self):
        raise NotImplementedError
        # window_name = 'helpWindow'

        # window = find_window(window_name)
        # if window is not None:
        #     window.show()

        # else:
        #     window = HelpWindow(
        #         parent=self,
        #         flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
        #     )

    @log(message='main-window: open keyboard-shortcuts-window')
    @wait
    @attempt(level=ExceptionLevel.ERROR)
    def on_keyboard_shortcuts_window_opened(self):
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
    @wait
    @attempt(level=ExceptionLevel.ERROR)
    def on_about_window_opened(self):
        raise NotImplementedError
        # window_name = 'aboutWindow'

        # window = find_window(window_name)
        # if window is not None:
        #     window.show()

        # else:
        #     window = AboutWindow(
        #         parent=self,
        #         flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
        #     )

    @log(message='main-window: close event')
    def closeEvent(self, event: QtCore.QEvent):  # noqa: N802

        try:
            set_setting(key=f'geometry/{self.objectName()}', value=self.geometry())

        finally:
            super().closeEvent(event)

    @staticmethod
    def not_implemented_plug(*args, **kwargs):
        raise NotImplementedError
