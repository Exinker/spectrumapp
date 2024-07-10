from setuptools import find_packages, setup

import spectrumapp


setup(
    # info
    name=spectrumapp.__name__,
    description=spectrumapp.__doc__,
    license=spectrumapp.__license__,
    keywords=['spectroscopy', 'app'],

    # version
    version=spectrumapp.__version__,

    # author details
    author=spectrumapp.__author__,
    author_email=spectrumapp.__email__,

    # setup directories
    packages=find_packages(),

    # setup data
    package_data={
        '': ['*.css', '*.ico'],
    },

    # requires
    install_requires=[
        item.strip() for item in open('requirements.txt', 'r').readlines()
        if item.strip()
    ],
    python_requires='>=3.10',
)
