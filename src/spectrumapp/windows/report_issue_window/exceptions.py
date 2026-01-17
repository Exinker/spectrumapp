from spectrumapp.exceptions import BaseApplicationError


class ArchiverError(BaseApplicationError):
    pass


class ProviderManagerError(BaseApplicationError):
    pass


class InternetConnectionError(ProviderManagerError):
    pass


class AuthorizationError(ProviderManagerError):
    pass
