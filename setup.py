#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask-Navigator
===============

A dead simple navigation for your Flask application.

Contributing
------------

Don't hesitate to create a `GitHub issue
<https://github.com/vitalk/flask-navigator/issues>`_ for any **bug** or
**suggestion**.

"""
import io
import os
import re
from setuptools import (
    find_packages, setup
)


def read(*parts):
    """Reads the content of the file created from *parts*."""
    try:
        with io.open(os.path.join(*parts), 'r', encoding='utf-8') as f:
            return f.readlines()
    except IOError:
        return []


def get_version():
    version_file = ''.join(read('flask_navigator', '__init__.py'))
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file, re.MULTILINE)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


__version__ = get_version()
install_requires = read('requirements', 'main.txt')


setup(
    name='Flask-Navigator',
    version=__version__,

    author='Vital Kudzelka',
    author_email='vital.kudzelka@gmail.com',

    url="https://github.com/vitalk/flask-navigator",
    description='A dead simple navigation for your Flask application.',
    download_url='https://github.com/vitalk/flask-navigator/tarball/%s' % __version__,
    long_description=__doc__,
    license='MIT',

    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,

    keywords='flask navigation pagination sqlalchemy',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Alpha',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
