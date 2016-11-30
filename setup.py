#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2016 genkosta
#
#  django-yandex-maps is free software under terms of the MIT License.
#

import os
import re
from codecs import open as codecs_open
from setuptools import setup, find_packages


def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs_open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(
        r'''^__version__ = ['"]([^'"]*)['"]''', version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError('Unable to find version string.')


setup(
    name     = 'django-yandex-maps',
    version  = find_version('yandex_maps', '__init__.py'),
    packages= find_packages(),
    requires = ['python (== 2.7)', 'django (>= 1.8)'],
    description  = 'Creating and editing Yandex maps.',
    long_description = open('README.rst').read(),
    author       = 'genkosta',
    author_email = 'genkosta43@gmail.com',
    url          = 'https://github.com/genkosta/django-yandex-maps',
    download_url = 'https://github.com/genkosta/django-yandex-maps/tarball/master',
    license      = 'MIT License',
    keywords     = 'django yandex maps map',
    classifiers  = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires = [
        'Pillow',
        'django-imagekit',
        'django-tinymce',
        'djlime-filebrowser',
        'python-slugify',
        'django-smart-selects',
    ],
)
