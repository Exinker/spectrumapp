from spectrumapp.windows.progress_window import ProgressWindow
from spectrumapp.windows.progress_window.progress_window import (
    ContentWidget,
    LabelWidget,
    LoggingPlainTextEditWidget,
    ProgressBarWidget,
)


def test_content_widget_default(
    progress_window: ProgressWindow,
):
    content_widget = progress_window.findChild(ContentWidget, 'contentWidget')

    assert isinstance(content_widget, ContentWidget)
    assert content_widget.findChild(
        LoggingPlainTextEditWidget,
        'loggingPlainText',
    ).toPlainText() == ContentWidget.DEFAULT_LOGGING_TEXT
    assert content_widget.findChild(ProgressBarWidget, 'progressBar').value() == ContentWidget.DEFAULT_PROGRESS
    assert content_widget.findChild(LabelWidget, 'infoLabel').text() == ContentWidget.DEFAULT_INFO
    assert content_widget.findChild(LabelWidget, 'messageLabel').text() == ContentWidget.DEFAULT_MESSAGE
