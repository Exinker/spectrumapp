from spectrumapp.applications import BaseApplication


def test_application(
    application_name: str,
    application_version: str,
    organization_name: str,
    qapp_cls: BaseApplication,
):
    app = qapp_cls()

    assert app.applicationName() == application_name
    assert app.applicationVersion() == application_version
    assert app.organizationName() == organization_name
