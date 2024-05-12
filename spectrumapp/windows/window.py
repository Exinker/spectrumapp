from collections.abc import Sequence

from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.settings import get_setting, set_setting


class BaseWindow(QtWidgets.QWidget):

    def __init__(self, *args, object_name: str | None = None, flags: Sequence[QtCore.Qt.WindowType] | None = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # object name
        object_name = object_name or self._getgefault_object_name()
        self.setObjectName(object_name)

        # flags
        flags = flags or (QtCore.Qt.WindowType.Window, )
        for flag in flags:
            self.setWindowFlag(flag, True)

        # actions
        action = QtGui.QAction('&Close', self)
        action.setShortcuts(['Ctrl+W', 'Esc'])
        action.setShortcutContext(QtCore.Qt.WindowShortcut)
        action.setToolTip('Close window')
        action.triggered.connect(self.close)
        self.addAction(action)

        # geometry
        geometry = get_setting(key=f'geometry/{self.objectName()}') or self._getdefault_geometry()
        self.setGeometry(geometry)

    # --------        setup        --------
    def _getgefault_object_name(self) -> str:
        """Get a default object name for given class."""
        cls = self.__class__

        name = cls.__name__
        name = name[0].lower() + name[1:]

        return name

    def _getdefault_geometry(self) -> QtCore.QRect:
        screen_width, screen_height = get_screen_size()

        window_width = self.layout().sizeHint().width() if self.layout() else int(screen_width / 4)
        window_height = int(screen_height / 2)
        geometry = QtCore.QRect(int(screen_width/2 - window_width/2), int(screen_height/2 - window_height/2), window_width, window_height)

        return geometry

    # --------        events        --------
    def closeEvent(self, event):

        # set geometry
        set_setting(key=f'geometry/{self.objectName()}', value=self.geometry())

        #
        event.accept()


# --------        utils        --------
def get_screen_size() -> tuple[int, int]:
    from tkinter import Tk
    root = Tk()
    root.withdraw()

    return root.winfo_screenwidth(), root.winfo_screenheight()
