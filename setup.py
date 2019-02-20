#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2014 genkosta
#
#  django-editor-ymaps is free software under terms of the MIT License.
#

from setuptools import find_packages, setup


def get_readme(file_path):
    with open(file_path) as readme_file:
        result = readme_file.read()
    return result


setup(
    name='django-editor-ymaps',
    version='1.0 beta',
    packages=find_packages(),
    include_package_data=True,
    requires=['python (>= 3.5)', 'django (>= 2.0)'],
    description='Creating and editing Yandex maps.',
    long_description=get_readme('README.rst'),
    author='genkosta',
    author_email='genkosta43@gmail.com',
    url='https://github.com/genkosta/django-editor-ymaps',
    download_url='https://github.com/genkosta/django-editor-ymaps/tarball/master',
    license='MIT License',
    keywords='django yandex map maps djeym',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'Django',
        'Pillow',
        'django-imagekit',
        'python-slugify',
        'django-ckeditor',
        'lxml',
        'django-smart-selects==1.5.3',
        'django-ipware'
    ],
)
