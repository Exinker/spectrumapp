# python setup.py sdist --dist-dir //10.11.12.11/Users/vaschenko/spectrumapp/dist/

import os
from setuptools import setup, find_packages


APPLICATION_NAME = os.environ['APPLICATION_NAME']
APPLICATION_DESCRIPTION = os.environ['APPLICATION_DESCRIPTION']
APPLICATION_VERSION = os.environ['APPLICATION_VERSION']

AUTHOR_NAME = os.environ['AUTHOR_NAME']
AUTHOR_EMAIL = os.environ['AUTHOR_EMAIL']

ORGANIZATION_NAME = os.environ['ORGANIZATION_NAME']


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
    install_requires=['pyside6'],
    python_requires='>=3.10',

)
