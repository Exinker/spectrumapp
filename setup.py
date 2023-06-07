# python setup.py sdist --dist-dir //10.11.12.11/Users/vaschenko/spectrumapp/dist/

import os
from setuptools import setup, find_packages


APPLICATION_NAME = os.environ.get('APPLICATION_NAME', '')
APPLICATION_DESCRIPTION = os.environ.get('APPLICATION_DESCRIPTION', '')
APPLICATION_VERSION = os.environ.get('APPLICATION_VERSION', '')

AUTHOR_NAME = os.environ.get('AUTHOR_NAME', '')
AUTHOR_EMAIL = os.environ.get('AUTHOR_EMAIL', '')

ORGANIZATION_NAME = os.environ.get('ORGANIZATION_NAME', '')


setup(
	# info
    name=APPLICATION_NAME,
	description=APPLICATION_DESCRIPTION,
	license='MIT',
    keywords=['spectroscopy', 'app'],

	# version
    version=APPLICATION_VERSION,

	# author details
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,

	# setup directories
    packages=find_packages(),
    # package_dir={'': 'src'},

	# setup data
    include_package_data=True,

	# requires
    install_requires=['pyside6', 'matplotlib', 'numpy'],
    python_requires='>=3.10',

)
