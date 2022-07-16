#! /usr/bin/env python
#
# Copyright (C) 2021 Mikko Kotila

DESCRIPTION = "Multi dictionary API for Tibetan Unicode and Wylie searches with exact, partial, and fuzzy match."
LONG_DESCRIPTION = """\
"""

DISTNAME = 'Dictionary Lookup'
MAINTAINER = 'Mikko Kotila'
MAINTAINER_EMAIL = 'mailme@mikkokotila.com'
URL = 'http://padma.io'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/Lotus-King-Research/Tibetan-Lookup'
VERSION = '0.7.1'

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

install_requires = ['pandas',
                    'botok',
                    'pyewts',
                    'strsimpy']


if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=install_requires,
          packages=['dictionary_lookup',
                    'dictionary_lookup.models',
                    'dictionary_lookup.utils'],

          classifiers=['Intended Audience :: Science/Research',
                       'Programming Language :: Python :: 3.7',
                       'Programming Language :: Python :: 3.8',
                       'License :: OSI Approved :: MIT License',
                       'Topic :: Scientific/Engineering :: Human Machine Interfaces',
                       'Topic :: Scientific/Engineering :: Artificial Intelligence',
                       'Operating System :: POSIX',
                       'Operating System :: Unix',
                       'Operating System :: MacOS',
                       'Operating System :: Microsoft :: Windows :: Windows 10'])
