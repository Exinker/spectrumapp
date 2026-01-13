from abc import ABC, abstractmethod
from pathlib import Path


class ReportManagerABS(ABC):

    @abstractmethod
    def send(self, archive_path: Path, description: str) -> None:
        raise NotImplementedError
