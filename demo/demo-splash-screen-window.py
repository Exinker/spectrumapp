import os
import time

from PySide6 import QtWidgets

from spectrumapp import ORGANIZATION_NAME, VERSION
from spectrumapp.windows.splashScreenWindow import SplashScreenWindow


def setdefault_environ(debug: bool = False) -> None:
    os.environ['APPLICATION_NAME'] = 'Demo'
    os.environ['APPLICATION_VERSION'] = VERSION
    os.environ['ORGANIZATION_NAME'] = ORGANIZATION_NAME

    os.environ['DEBUG'] = str(debug)


if __name__ == '__main__':

    # setup env
    setdefault_environ()

    # apps
    app = QtWidgets.QApplication()

    window = SplashScreenWindow()
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
