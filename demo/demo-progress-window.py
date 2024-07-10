import os
import time

from PySide6 import QtWidgets

import spectrumapp
from spectrumapp.windows.progressWindow import ProgressWindow


def setdefault_environ(debug: bool = False) -> None:
    os.environ['APPLICATION_NAME'] = 'Demo'
    os.environ['APPLICATION_VERSION'] = spectrumapp.__version__
    os.environ['ORGANIZATION_NAME'] = spectrumapp.__organization__

    os.environ['DEBUG'] = str(debug)


if __name__ == '__main__':

    # setup env
    setdefault_environ()

    # apps
    app = QtWidgets.QApplication()

    window = ProgressWindow()
    window.show()

    for i in range(1, 100+1):

        # update window
        window.update(
            progress=i,
            info='<strong>PLEASE, WAIT!</strong>',
            message='Loading {value} {label} is complited!'.format(
                value=i,
                label='percent' if i == 1 else 'percents',
            ),
        )

        # delay
        time.sleep(.025)

    app.quit()
