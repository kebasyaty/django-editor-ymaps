#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2018 genkosta
#
#  django-editor-ymaps is free software under terms of the MIT License.
#

import os
import re
from setuptools import setup, find_packages


def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    with open(file_path, encoding='utf-8') as target_file:
        result = target_file.read()
    return result


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(
        r'''^__version__ = ['"]([^'"]*)['"]''', version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError('Unable to find version string.')


def get_readme(file_path):
    with open(file_path, encoding='utf-8') as readme_file:
        result = readme_file.read()
    return result


setup(
    name='django-editor-ymaps',
    version=find_version('yandex_maps', '__init__.py'),
    packages=find_packages(),
    include_package_data=True,
    requires=['python (>= 3.6)', 'django (>= 2.1)'],
    description='Creating and editing Yandex maps.',
    long_description=get_readme('README.rst'),
    author='genkosta',
    author_email='genkosta43@gmail.com',
    url='https://github.com/genkosta/django-editor-ymaps',
    download_url='https://github.com/genkosta/django-editor-ymaps/tarball/master',
    license='MIT License',
    keywords='django editor ymaps yandex maps',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'Pillow==5.2.0',
        'django-imagekit==4.0.2',
        'python-slugify==1.2.6',
        'django-smart-selects==1.5.4',
        'django-ckeditor==5.6.1',
    ],
)
