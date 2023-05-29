
from PySide6 import QtCore, QtGui, QtWidgets

from spectrumapp.core.settings import get_setting, set_setting


class Window(QtWidgets.QWidget):

    def __init__(self, *args, shortcuts: dict[str, str] | None = None, **kwargs):
        super().__init__(*args, **kwargs)

        #
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # shortcut
        QtGui.QShortcut('Ctrl+W', self).activated.connect(self.close)
        QtGui.QShortcut('Esc', self).activated.connect(self.close)

        if shortcuts:
            for key, value in shortcuts.items():
                QtGui.QShortcut(key, self).activated.connect(value)

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

    def closeEvent(self, event):

        # set geometry
        set_setting(key=f'geometry/{self.objectName()}', value=self.geometry())

        # set empty widget
        self.setParent(None)
        return super().closeEvent(event)
