import os
from abc import ABC, abstractmethod

import telepot

from spectrumapp.types import FilePath


class AbstractDelivery(ABC):

    @abstractmethod
    def send(self, timestamp: str, description) -> None:
        raise NotImplementedError


class TelegramDelivery(AbstractDelivery):

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    @property
    def bot(self) -> telepot.Bot:
        return telepot.Bot(self.token)

    def send(self, filepath: FilePath, timestamp: str, description: str) -> None:
        caption = '\n'.join([
            os.environ['APPLICATION_NAME'],
            os.environ['APPLICATION_VERSION'],
            timestamp,
            description,
        ])

        with open(filepath, 'rb') as file:
            self.bot.sendDocument(
                chat_id=self.chat_id,
                document=file,
                caption=caption,
            )
