from spectrumapp.exceptions import BaseApplicationError


class ArchiverError(BaseApplicationError):
    pass


class DeliveryError(BaseApplicationError):
    pass


class InternetConnectionError(DeliveryError):
    pass


class TelegramAuthorizationError(DeliveryError):
    pass
