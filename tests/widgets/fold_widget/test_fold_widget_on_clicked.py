from spectrumapp.widgets.fold_widget import FoldWidget
from spectrumapp.widgets.fold_widget.fold_widget import (
    ToggleWidget,
    WrappedWidget,
)


def test_fold_widget_on_clicked(
    title: str,
    is_folded: bool,
    fold_widget: FoldWidget,
):
    toggle_widget = fold_widget.findChild(ToggleWidget, 'toggleWidget')

    toggle_widget.click()

    assert toggle_widget.isChecked() is not is_folded
    assert fold_widget.findChild(ToggleWidget, 'toggleWidget').text() == ToggleWidget.TEXT_TEMPLATE.format(
        icon=ToggleWidget.ICONS[not is_folded],
        title=title,
    )
    assert fold_widget.findChild(WrappedWidget, 'wrappedWidget').height() > 0
