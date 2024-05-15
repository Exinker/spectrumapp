import os
from abc import abstractmethod, abstractproperty

from PySide6 import QtWidgets


try:  # change app id for correct icon present
    from PySide6.QtWinExtras import QtWin

    app_id = '{organization}.{name}.MAINWINDOW.{version}'.format(
        name=os.environ['APPLICATION_NAME'],
        version=os.environ['APPLICATION_VERSION'],
        organization=os.environ['ORGANIZATION_NAME'],
    )
    QtWin.setCurrentProcessExplicitAppUserModelID(app_id)

except ImportError:
    pass


class AbstractApplication(QtWidgets.QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setApplicationName(os.environ['APPLICATION_NAME'])
        self.setApplicationVersion(os.environ['APPLICATION_VERSION'])
        self.setOrganizationName(os.environ['ORGANIZATION_NAME'])

    @abstractproperty
    def window(self) -> QtWidgets.QWidget:
        """The main window."""
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """Run the application."""
        raise NotImplementedError

    @abstractmethod
    def refresh(self) -> None:
        """Refresh all windows and widgets of an application."""
        raise NotImplementedError

    @abstractmethod
    def reset(self, refresh: bool = True) -> None:
        """Update settings, config and refresh (optionally) the windows."""
        raise NotImplementedError
