import os

from PySide6 import QtWidgets


try:  # change app id for correct icon present
    from ctypes import windll

    app_id = '{organization}.{name}.MAINWINDOW.{version}'.format(
        name=os.environ['APPLICATION_NAME'],
        version=os.environ['APPLICATION_VERSION'],
        organization=os.environ['ORGANIZATION_NAME'],
    )
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

except ImportError:
    pass

except KeyError:  # for testing only
    pass


class BaseApplication(QtWidgets.QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def applicationName(self) -> str:  # noqa: N802
        return os.environ['APPLICATION_NAME']

    def applicationVersion(self) -> str:  # noqa: N802
        return os.environ['APPLICATION_VERSION']

    def organizationName(self) -> str:  # noqa: N802
        return os.environ['ORGANIZATION_NAME']

    @property
    def window(self) -> QtWidgets.QWidget:
        """The main window."""
        raise NotImplementedError

    def run(self) -> None:
        """Run the application."""
        raise NotImplementedError

    def refresh(self) -> None:
        """Refresh all windows and widgets of an application."""
        raise NotImplementedError

    def reset(self, refresh: bool = True) -> None:
        """Update settings, config and refresh (optionally) the windows."""
        raise NotImplementedError
