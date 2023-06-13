# python setup.py sdist --dist-dir //10.11.12.11/Users/vaschenko/spectrumapp/dist/

from setuptools import setup, find_packages

from spectrumapp.core.config import APPLICATION_NAME, APPLICATION_DESCRIPTION, APPLICATION_VERSION, AUTHOR_NAME, AUTHOR_EMAIL


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
