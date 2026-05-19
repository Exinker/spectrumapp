import sys

from PySide6 import QtWidgets


def set_app_id(
    application_name: str,
    application_version: str,
    organization_name: str,
) -> None:

    if sys.platform.startswith('win'):
        from ctypes import windll

        app_id = '{organization}.{name}.MAINWINDOW.{version}'.format(
            name=application_name,
            version=application_version,
            organization=organization_name,
        )
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


class ApplicationABC(QtWidgets.QApplication):

    def __init__(
        self,
        *args,
        application_name: str,
        application_version: str,
        organization_name: str,
        **kwargs,
    ) -> None:
        set_app_id(
            application_name=application_name,
            application_version=application_version,
            organization_name=organization_name,
        )

        super().__init__(*args, **kwargs)

        self.setApplicationName(application_name)  # noqa: N802
        self.setApplicationVersion(application_version)  # noqa: N802
        self.setOrganizationName(organization_name)  # noqa: N802

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
        """Update settings or configs and refresh (optionally) the windows."""
        raise NotImplementedError
