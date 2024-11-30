import os
import time

from PySide6 import QtWidgets

import spectrumapp
from spectrumapp.windows.splashScreenWindow import SplashScreenWindow


def setdefault_environ() -> None:
    os.environ['APPLICATION_NAME'] = 'Demo'
    os.environ['APPLICATION_VERSION'] = spectrumapp.__version__
    os.environ['ORGANIZATION_NAME'] = spectrumapp.__organization__


if __name__ == '__main__':

    setdefault_environ()

    app = QtWidgets.QApplication()

    window = SplashScreenWindow()
    window.show()
    for i in range(1, 100+1):
        window.update(
            progress=i,
            info='<strong>PLEASE, WAIT!</strong>',
            message='Loading {value} {label} is complited!'.format(
                value=i,
                label='percent' if i == 1 else 'percents',
            ),
        )

        time.sleep(.025)

    app.quit()
