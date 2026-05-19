import os

from spectrumapp.paths import read_static
from spectrumapp.windows.progress_window import ProgressWindow


def test_progress_window(
    progress_window: ProgressWindow,
):
    filepath = os.path.join('.', 'static', 'progress-window.css')
    style = read_static(filepath)

    assert progress_window.objectName() == 'progressWindow'
    assert progress_window.windowFlags() == ProgressWindow.DEFAULT_FLAGS
    assert progress_window.styleSheet() == style
    # assert progress_window.windowIcon() == QtGui.QIcon(
    #     fileName=os.path.join('.', 'static', 'icon.ico'),
    # )  # как сравнить иконки?
    assert progress_window.size() == progress_window.DEFAULT_SIZE
