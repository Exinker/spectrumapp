import logging
import os
from abc import ABC, abstractmethod

import telepot
from telepot.exception import (
    TelegramError,
    UnauthorizedError,
)
from urllib3.exceptions import RequestError

from spectrumapp.types import FilePath
from spectrumapp.windows.exceptionWindow import ExceptionDialog, ExceptionLevel
from spectrumapp.windows.reportIssueWindow.exceptions import (
    InternetConnectionError,
    AuthorizationError,
)


LOGGER = logging.getLogger('spectrumapp')


class AbstractDelivery(ABC):

    @abstractmethod
    def send(self, filepath: FilePath, description: str) -> None:
        raise NotImplementedError


class TelegramDelivery(AbstractDelivery):

    def __init__(
        self,
        timestamp: str,
        token: str,
        chat_id: str,
    ):
        self._timestamp = timestamp
        self._token = token
        self._chat_id = chat_id

        self._bot = None

    @property
    def bot(self) -> telepot.Bot:

        if self._bot is None:
            self._bot = telepot.Bot(self._token)

        return self._bot

    def send(self, filepath: FilePath, description: str) -> None:
        caption = '\n'.join([
            os.environ['APPLICATION_NAME'],
            os.environ['APPLICATION_VERSION'],
            self._timestamp,
            description,
        ])

        with open(filepath, 'rb') as file:
            try:
                self.bot.sendDocument(
                    chat_id=self._chat_id,
                    document=file,
                    caption=caption,
                )
            except RequestError as error:
                LOGGER.warning(
                    'Send message failed with %s: %s',
                    type(error).__name__,
                    error,
                )
                dialog = ExceptionDialog(
                    message='Send message failed with {}!'.format(
                        InternetConnectionError.__name__,
                    ),
                    info='Check an internet connection.',
                    level=ExceptionLevel.ERROR,
                )
                dialog.show()
            except UnauthorizedError as error:
                LOGGER.warning(
                    'Send message failed with %s: %s',
                    type(error).__name__,
                    error,
                )
                dialog = ExceptionDialog(
                    message='Send message failed with {}!'.format(
                        AuthorizationError.__name__,
                    ),
                    info='TELEGRAM_TOKEN is invalid.',
                    level=ExceptionLevel.WARNING,
                )
                dialog.show()
            except TelegramError as error:
                LOGGER.warning(
                    'Send message failed with %s: %s',
                    type(error).__name__,
                    error,
                )

                dialog = ExceptionDialog(
                    message='Send message failed with {}!'.format(
                        AuthorizationError.__name__,
                    ),
                    info={
                        400: 'TELEGRAM_CHAT_ID is invalid!',
                        404: 'File is not found. Create .env file with Telegram credentials!',
                    }.get(error.error_code, error.description),
                    level=ExceptionLevel.WARNING,
                )
                dialog.show()

            except Exception as error:
                LOGGER.warning(
                    'Send message failed with %s: %s',
                    type(error).__name__,
                    error,
                )
                raise
            else:
                LOGGER.debug('Dump file is send successfully.')
