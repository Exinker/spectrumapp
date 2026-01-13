import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Self

from telepot import Bot
from telepot.exception import (
    TelegramError,
    UnauthorizedError,
)
from urllib3.exceptions import RequestError

from spectrumapp.windows.exception_window import ExceptionDialog, ExceptionLevel
from spectrumapp.windows.report_issue_window.exceptions import AuthorizationError, InternetConnectionError
from spectrumapp.windows.report_issue_window.report_managers.base_report_manager import ReportManagerABS


LOGGER = logging.getLogger('spectrumapp')


class TelegramReportManager(ReportManagerABS):

    @classmethod
    def create(
        cls,
        timestamp: float,
        token: str,
        chat_id: str,
    ) -> Self:

        return cls(
            timestamp=timestamp,
            chat_id=chat_id,
            bot=Bot(token),
        )

    def __init__(
        self,
        timestamp: float,
        chat_id: str,
        bot: Bot,
    ) -> None:

        self._timestamp = timestamp
        self._chat_id = chat_id
        self._bot = bot

    def send(
        self,
        archive_path: Path,
        description: str,
    ) -> None:

        try:
            self._bot.sendDocument(
                chat_id=self._chat_id,
                document=open(archive_path, 'rb'),
                caption='\n'.join([
                    os.environ['APPLICATION_NAME'],
                    os.environ['APPLICATION_VERSION'],
                    datetime.fromtimestamp(self._timestamp).strftime('%Y.%m.%d %H:%M'),
                    description,
                ]),
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
