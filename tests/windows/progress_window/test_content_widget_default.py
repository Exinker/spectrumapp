from spectrumapp.windows.progress_window import ProgressWindow
from spectrumapp.windows.progress_window.progress_window import (
    ContentWidget,
    LabelWidget,
    LoggingPlainTextEditWidget,
    ProgressBarWidget,
)


def test_content_widget_default(
    default_logging_text: str,
    default_progress: int,
    default_info: str,
    default_message: str,
    progress_window: ProgressWindow,
):
    content_widget = progress_window.findChild(ContentWidget, 'contentWidget')

    assert isinstance(content_widget, ContentWidget)
    assert content_widget.findChild(LoggingPlainTextEditWidget, 'loggingPlainText').toPlainText() == default_logging_text  # noqa: E501
    assert content_widget.findChild(ProgressBarWidget, 'progressBar').value() == default_progress
    assert content_widget.findChild(LabelWidget, 'infoLabel').text() == default_info
    assert content_widget.findChild(LabelWidget, 'messageLabel').text() == default_message
