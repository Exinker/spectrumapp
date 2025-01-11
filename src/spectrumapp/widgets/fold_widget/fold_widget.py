import sys

from PySide6 import QtCore, QtWidgets


class ToggleWidget(QtWidgets.QPushButton):

    ICONS = {
        True: b'\xE2\x8F\xB5'.decode(),
        False: b'\xE2\x8F\xB7'.decode(),
    }
    TEXT_TEMPLATE = ' {icon}\t{title}'
    STYLESHEET = """
    QPushButton {
        text-align: left;

        padding: 5px;
        border: none;
    }
    """

    def __init__(
        self,
        title: str,
        is_folded: bool,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.setObjectName('toggleWidget')
        self.setCheckable(True)
        self.setChecked(is_folded)
        self.setStyleSheet(self.STYLESHEET)
        self.clicked.connect(self.on_clicked)

        # setup title
        self._title = title
        self._update_title(
            is_folded=is_folded,
        )

    def on_clicked(self):
        self._update_height(
            is_folded=self.isChecked(),
        )
        self._update_title(
            is_folded=self.isChecked(),
        )

    def _update_height(self, is_folded: bool):
        widget = self.parent().findChild(QtWidgets.QFrame, 'wrappedWidget')
        widget._update_height(
            is_folded=is_folded,
        )

        widget = self.parent()
        widget._update_height()

    def _update_title(self, is_folded: bool):
        self.setText(self.TEXT_TEMPLATE.format(
            icon=self.ICONS[is_folded],
            title=self._title,
        ))


class WrappedWidget(QtWidgets.QFrame):

    def __init__(
        self,
        __widget: QtWidgets.QWidget,
        *args,
        is_folded: bool,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.setObjectName('wrappedWidget')

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(__widget)

        # setup height
        self._update_height(
            is_folded=is_folded,
        )

    def _update_height(self, is_folded: bool):

        height = {
            False: self.sizeHint().height(),
            True: 0,
        }[is_folded]
        self.setFixedHeight(height)


class FoldWidget(QtWidgets.QWidget):

    def __init__(
        self,
        __widget: QtWidgets.QWidget,
        *args,
        title: str,
        is_folded: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(ToggleWidget(
            title=title,
            is_folded=is_folded,
            parent=self,
        ))
        layout.addWidget(WrappedWidget(
            __widget,
            is_folded=is_folded,
            parent=self,
        ))

    def sizeHint(self) -> QtCore.QSize:  # noqa: N802
        children = [
            self.findChild(QtCore.QObject, object_name)
            for object_name in ('wrappedWidget', 'toggleWidget')
        ]

        return QtCore.QSize(
            max([child.width() for child in children]),
            sum([child.height() for child in children]),
        )

    def _update_height(self):

        height = self.sizeHint().height()
        self.setFixedHeight(height)
        self.adjustSize()

        parent = self.parent()
        if parent:
            height = parent.sizeHint().height()
            parent.setMaximumHeight(height)
            parent.adjustSize()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QFrame()
    layout = QtWidgets.QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    for i in range(1, 10+1):
        button = QtWidgets.QPushButton(f'Button #{i}', widget)
        button.setFixedSize(250, 30)
        button.clicked.connect(lambda state, text=f'clicked: #{i}': print(text))
        layout.addWidget(button)
    window = FoldWidget(widget, title='Title', is_folded=True)
    window.show()

    sys.exit(app.exec_())
