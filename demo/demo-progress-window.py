import time

from PySide6 import QtWidgets

from spectrumapp.windows.progressWindow import ProgressWindow
from utils import setdefault_environ


if __name__ == '__main__':
    setdefault_environ()

    app = QtWidgets.QApplication()

    window = ProgressWindow()
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
