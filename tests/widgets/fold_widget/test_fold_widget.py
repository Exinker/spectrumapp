from PySide6 import QtWidgets

from spectrumapp.widgets.fold_widget import FoldWidget
from spectrumapp.widgets.fold_widget.fold_widget import (
    ToggleWidget,
    WrappedWidget,
)


def test_fold_widget(
    wrapped_widget: QtWidgets.QWidget,
    title: str,
    is_folded: bool,
    fold_widget: FoldWidget,
):

    assert isinstance(fold_widget.findChild(QtWidgets.QWidget, wrapped_widget.objectName()), type(wrapped_widget))
    assert fold_widget.findChild(ToggleWidget, 'toggleWidget').isChecked() is is_folded
    assert fold_widget.findChild(ToggleWidget, 'toggleWidget').text() == ToggleWidget.TEXT_TEMPLATE.format(
        icon=ToggleWidget.ICONS[is_folded],
        title=title,
    )
    assert fold_widget.findChild(WrappedWidget, 'wrappedWidget').height() == {
        True: 0,
    }[is_folded]
