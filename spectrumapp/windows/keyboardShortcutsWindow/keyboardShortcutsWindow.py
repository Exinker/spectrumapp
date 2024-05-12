from typing import Mapping

from PySide6 import QtCore, QtWidgets

from spectrumapp.windows.window import BaseWindow


BASE_CONTENT = {
    'File': {
        'Ctrl+O': 'Open File',
        'Ctrl+Shift+R': 'Reset Application',
        'Ctrl+R': 'Refresh Window',
        'Ctrl+W or Esc': 'Close Window',
        'Ctrl+Q': 'Quit Application',
    },
    'Instruments': {
    },
    'Help': {
        'Ctrl+Shift+I': 'Report Issue Window',
    },
}


# --------        windows        --------
class BaseKeyboardShortcutsWindow(BaseWindow):

    def __init__(self, *args, content: Mapping[str, Mapping[str, str]] | None = None, **kwargs):
        super().__init__(*args, **kwargs)

        content = content or BASE_CONTENT

        # title
        title = 'Keyboard Shortcuts Window'
        self.setWindowTitle(title)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        for title, item in content.items():
            if item:
                layout.addWidget(ContentWidget(
                    title=title,
                    content=item,
                ))

        # geometry
        self.setFixedSize(480, self.sizeHint().height())

        #
        self.show()


class ContentWidget(QtWidgets.QGroupBox):

    def __init__(self, *args, title: str, content: Mapping[str, str], **kwargs):
        super().__init__(title, *args, **kwargs)

        # layout
        layout = ContentLayout(self)

        for shourtcut, description in content.items():
            label = QtWidgets.QLabel(shourtcut, alignment=QtCore.Qt.AlignLeft)
            label.setFixedWidth(120)

            layout.addRow(label, QtWidgets.QLabel(description))


class ContentLayout(QtWidgets.QFormLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.setContentsMargins(5, 5, 5, 5)
        self.setSpacing(5)
