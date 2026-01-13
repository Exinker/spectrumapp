import logging
import time
from pathlib import Path
from zipfile import ZipFile

from spectrumapp.windows.report_issue_window.archive_managers.base_archive_manager import ArchiveManagerABC
from spectrumapp.windows.report_issue_window.archive_managers.utils import explore


LOGGER = logging.getLogger('spectrumapp')


class ZipArchiveManager(ArchiveManagerABC):

    TIMEOUT = 1

    def dump(self) -> None:
        """Archive selected `files` to .zip archive."""

        n_dumped = 0
        with ZipFile(self.archive_path, 'w') as archive:

            for prefix, file in self._files:
                try:
                    archive.write(file, arcname=_get_arcname(file, prefix=prefix))

                except Exception as error:
                    LOGGER.warning(
                        'Write file %r failed with %s: %s',
                        file,
                        type(error).__name__,
                        error,
                    )

                else:
                    n_dumped += 1

        time.sleep(self.TIMEOUT)  # add timeout to realistic
        LOGGER.info('%s files were dumped successfully.', n_dumped)

    @property
    def archive_path(self) -> Path:
        return self.archive_dir / '{}.zip'.format(self.archive_name)


def _get_arcname(__file: Path, prefix: Path | None) -> str:

    if prefix:
        return str(__file.relative_to(prefix))

    return str(__file)
