
import os
from collections.abc import Mapping

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.core.config import setdefault_config
from spectrumapp.core.logging import setdefault_logging, log
from spectrumapp.core.setting import setdefault_setting, get_setting, set_setting
from spectrumapp.core.utils import pave
from spectrumapp.utils.find import find_window
from spectrumapp.utils.modifier import wait, attempt, MessageLevel
from spectrumapp.window.splashScreenWindow import splashscreen


APPLICATION_NAME = os.environ.get('APPLICATION_NAME', '')


class BaseMainWindow(QtWidgets.QMainWindow):
    _actions: Mapping[str, QtGui.QAction] = dict()
    _menus: Mapping[str, QtWidgets.QMenu] = dict()

    @splashscreen(progress=70, info='<strong>LOADING</strong> user interface...')
    def __init__(self, *args, show: bool = False, **kwargs):
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

        # geometry
        geometry = get_setting(key=f'geometry/{self.objectName()}')
        if geometry:
            self.setGeometry(geometry)
            self.setWindowState(QtCore.Qt.WindowActive)
        else:
            self.setWindowState(QtCore.Qt.WindowMaximized | QtCore.Qt.WindowActive)

        #
        if show:
            self.show()

    # --------        setup        --------
    def _add_action(self, action: QtGui.QAction, key: str) -> None:

        # add action to window 
        self.addAction(action)

        # map action
        self._actions[key] = action

    def _setdefault_actions(self) -> None:

        action = QtGui.QAction('&Open...', self)
        action.setShortcut('Ctrl+O')
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.setToolTip('Open file...')
        action.triggered.connect(self._onOpenAction)
        self._add_action(action, key='open')

        action = QtGui.QAction('&Refresh', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+R'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self._onRefreshAppAction)
        self._add_action(action, key='refresh')

        action = QtGui.QAction('&Reset', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Shift+R'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.triggered.connect(self._onResetAppAction)
        self._add_action(action, key='reset')

        action = QtGui.QAction('&Quit', self)
        action.setShortcut(QtGui.QKeySequence('Ctrl+Q'))
        action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        action.setStatusTip('Quit')
        action.triggered.connect(self._onQuitAction)
        self._add_action(action, key='quit')

        action = QtGui.QAction('&View Help', self)
        action.triggered.connect(self._onOpenHelpWindowAction)
        self._add_action(action, key='help-window')

        action = QtGui.QAction('&About', self)
        action.triggered.connect(self._onOpenAboutWindowAction)
        self._add_action(action, key='about-window')

    def _add_menu(self, menu: QtWidgets.QMenu, key: str) -> None:

        # add menu to menubar
        menubar = self.menuBar()
        menubar.addMenu(menu)

        # map menu
        self._menus[key] = menu

    def _setdefault_menubar(self) -> None:

        menu = QtWidgets.QMenu(title='&File', parent=self)
        menu.addAction(self._actions['open'])
        menu.addSeparator()
        menu.addAction(self._actions['refresh'])
        menu.addAction(self._actions['reset'])
        menu.addSeparator()
        menu.addAction(self._actions['quit'])
        self._add_menu(menu, 'file')

        menu = QtWidgets.QMenu(title='&Instruments', parent=self)
        menu.setEnabled(False)
        self._add_menu(menu, 'instruments')

        menu = QtWidgets.QMenu(title='&Settings', parent=self)
        menu.setEnabled(False)
        self._add_menu(menu, 'settings')

        menu = QtWidgets.QMenu(title='&Help', parent=self)
        menu.addAction(self._actions['help-window'])
        menu.addSeparator()
        menu.addAction(self._actions['about-window'])
        self._add_menu(menu, 'help')

    # --------        slots        --------
    @log(msg='app: open action')
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

    @log(msg='app: reset action')
    @wait
    @splashscreen(delay=1)
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

    @log(msg='app: refresh action')
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

    @log(msg='app: quit action')
    @wait
    def _onQuitAction(self):
        self.close()

    @log(msg='app: open "help" window')
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

    @log(msg='app: open "about" window')
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


class BaseWindow(QtWidgets.QWidget):
    _actions: Mapping[str, QtGui.QAction] = dict()
    _menus: Mapping[str, QtWidgets.QMenu] = dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # geometry
        geometry = get_setting(key=f'geometry/{self.objectName()}')
        if geometry is None:
            app = QtWidgets.QApplication.instance()
            screen_size = app.primaryScreen().size()
            layout = self.layout()

            width = layout.sizeHint().width() if layout else int(screen_size.width() / 4)
            height = int(screen_size.height() / 2)
            geometry = QtCore.QRect(int(screen_size.width()/2 - width/2), int(screen_size.height()/2 - height/2), width, height)

        self.setGeometry(geometry)

    # --------        setup        --------
    def _add_action(self, action: QtGui.QAction, key: str) -> None:

        # add action to window 
        self.addAction(action)

        # map action
        self._actions[key] = action

    def _setdefault_actions(self) -> None:

        action = QtGui.QAction('&Close', self)
        action.setShortcuts(['Ctrl+W', 'Esc'])
        action.setShortcutContext(QtCore.Qt.WindowShortcut)
        action.setToolTip('Close window')
        action.triggered.connect(self.close)
        self._add_action(action, key='close')

    # --------        events        --------
    def closeEvent(self, event):

        # set geometry
        set_setting(key=f'geometry/{self.objectName()}', value=self.geometry())

        # set empty widget
        self.setParent(None)
        return super().closeEvent(event)
