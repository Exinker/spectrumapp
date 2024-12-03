from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.helpers import getdefault_geometry, getdefault_object_name
from spectrumapp.settings import get_setting, set_setting


class BaseWindow(QtWidgets.QWidget):

    def __init__(self, *args, object_name: str | None = None, flags: QtCore.Qt.WindowType | None = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # object name
        object_name = object_name or getdefault_object_name(self)
        self.setObjectName(object_name)

        # flags
        flags = flags or QtCore.Qt.WindowType.Window
        self.setWindowFlags(flags)

        # actions
        action = QtGui.QAction('&Close', self)
        action.setShortcuts(['Ctrl+W', 'Esc'])
        action.setShortcutContext(QtCore.Qt.WindowShortcut)
        action.setToolTip('Close window')
        action.triggered.connect(self.close)
        self.addAction(action)

        # geometry
        geometry = get_setting(key=f'geometry/{self.objectName()}') or getdefault_geometry(self)
        self.setGeometry(geometry)

    def closeEvent(self, event):

        try:
            set_setting(key=f'geometry/{self.objectName()}', value=self.geometry())
        finally:
            super().closeEvent(event)
