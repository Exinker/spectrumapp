"""This is a template for an any PySide6 (PyQt6) application."""

from datetime import datetime
from importlib import metadata


distribution = metadata.distribution('spectrumapp')
__name__ = distribution.metadata['Name']
__version__ = distribution.version
__author__ = 'Pavel Vaschenko'
__email__ = 'vaschenko@vmk.ru'
__organization__ = 'VMK-Optoelektronika'
__license__ = 'MIT'
__copyright__ = 'Copyright {}, {}'.format(datetime.now().year, __organization__)
