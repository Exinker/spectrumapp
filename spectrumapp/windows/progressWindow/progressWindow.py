import os
from typing import Iterable, Sequence

from PySide6 import QtWidgets, QtCore, QtGui

from spectrumapp.paths import pave
from spectrumapp.utils import find_window


# --------        windows        --------
class ProgressWindow(QtWidgets.QWidget):

    def __init__(self, *args, flags: Sequence[QtCore.Qt.WindowType] | None = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('progressWindow')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # flags
        flags = flags or (QtCore.Qt.WindowType.Window, QtCore.Qt.WindowType.WindowStaysOnTopHint)
        for flag in flags:
            self.setWindowFlag(flag, True)

        # style
        filepath = pave(os.path.join('.', 'static', 'progress-window.css'))
        style = open(filepath, 'r').read()
        self.setStyleSheet(style)

        # icon
        filepath = pave(os.path.join('.', 'static', 'icon.ico'))
        icon = QtGui.QIcon(filepath)
        self.setWindowIcon(icon)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(ContentWidget(
            parent=self,
        ))

        # geometry
        self.setFixedSize(QtCore.QSize(680, 200))

        # show window
        self.show()

        # move window
        window = find_window('splashScreenWindow')
        if window:
            self.move(
                window.geometry().left(),
                window.geometry().bottom(),
            )

    def update(self, progress: int | None = None, info: str | None = None, message: str | None = None):

        if progress:
            widget = self.findChild(QtWidgets.QProgressBar, 'progressBar')
            widget.setValue(progress)
        if info:
            widget = self.findChild(QtWidgets.QLabel, 'infoLabel')
            widget.setText(info)
        if message:
            widget = self.findChild(QtWidgets.QLabel, 'messageLabel')
            widget.setText(message)

        #
        app = QtWidgets.QApplication.instance()
        app.processEvents()

    def closeEvent(self, event):

        # set empty widget
        self.setParent(None)
        event.accept()


class ContentWidget(QtWidgets.QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('contentWidget')

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addSpacing(50)
        layout.addWidget(LoggingPlainTextEditWidget(
            '',
            parent=self,
        ))
        layout.addWidget(ProgressBarWidget(
            objectName='progressBar',
            parent=self,
        ))
        layout.addWidget(LabelWidget(
            objectName='infoLabel',
            text='<strong>LOADING</strong>...',
            parent=self,
        ))
        layout.addWidget(LabelWidget(
            objectName='messageLabel',
            text='',
            parent=self,
        ))
        layout.addSpacing(50)


class LoggingPlainTextEditWidget(QtWidgets.QPlainTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('loggingPlainText')
        self.setPlaceholderText('')
        self.setEnabled(False)

        # geometry
        self.setFixedHeight(100)


class ProgressBarWidget(QtWidgets.QProgressBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setValue(0)


class LabelWidget(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


# --------        decorators        --------
def progress(iterable: Iterable, info: str | None = ''):
    """Progress decorator for long time processes."""
    window_name = 'processWindow'

    #
    try:
        n_items = len(iterable)
    except (TypeError, AttributeError):
        n_items = None

    # window
    window = find_window(window_name)
    if window is not None:
        window.show()

    else:
        window = ProgressWindow()

    # iterate
    try:
        for i, item in enumerate(iterable):
            window.update(
                progress='' if n_items is None else int(100*(i + 1) / n_items),
                info=info,
                message='' if n_items is None else f'<strong>{item}</strong> ({i + 1}/{n_items})',
            )

            yield item

    finally:
        window.setParent(None)
        window.close()
