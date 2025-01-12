import os

from spectrumapp.windows.progress_window import ProgressWindow


def test_progress_window(
    progress_window: ProgressWindow,
):

    assert progress_window.objectName() == 'progressWindow'
    assert progress_window.windowFlags() == ProgressWindow.DEFAULT_FLAGS
    assert progress_window.styleSheet() == open(
        file=os.path.join('.', 'static', 'progress-window.css'),
        mode='r',
    ).read()
    # assert progress_window.windowIcon() == QtGui.QIcon(
    #     fileName=os.path.join('.', 'static', 'icon.ico'),
    # )  # как сравнить иконки?
    assert progress_window.size() == progress_window.DEFAULT_SIZE
