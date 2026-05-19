from spectrumapp.windows.splash_screen_window import SplashScreenWindow
from spectrumapp.windows.splash_screen_window.splash_screen_window import (
    ContentWidget,
    LabelWidget,
    ProgressBarWidget,
)


def test_content_widget_default(
    application_name: str,
    application_version: str,
    default_progress: int,
    default_info: str,
    default_message: str,
    splash_screen_window: SplashScreenWindow,
):
    content_widget = splash_screen_window.findChild(ContentWidget, 'contentWidget')

    assert isinstance(content_widget, ContentWidget)
    assert content_widget.findChild(LabelWidget, 'appNameLabel').text() == '<strong>{name}</strong>'.format(
        name=application_name.upper(),
    )
    assert content_widget.findChild(LabelWidget, 'appVersionLabel').text() == '<strong>VERSION</strong> {version}'.format(  # noqa: E501
        version=application_version,
    )
    assert content_widget.findChild(ProgressBarWidget, 'progressBar').value() == default_progress
    assert content_widget.findChild(LabelWidget, 'infoLabel').text() == default_info
    assert content_widget.findChild(LabelWidget, 'messageLabel').text() == default_message
