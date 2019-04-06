#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
$$$$$___$$$$$$__$$$$$__$$__$$__$$___$$
$$__$$______$$__$$______$$$$___$$$_$$$
$$__$$______$$__$$$$_____$$____$$_$_$$
$$__$$__$$__$$__$$_______$$____$$___$$
$$$$$____$$$$___$$$$$____$$____$$___$$
"""
#
#  Convenient use of the Yandex map service for web development on 
#  the popular and free Django framework.
#
#  Copyright (c) 2014 genkosta
#
#  django-editor-ymaps is free software under terms of the MIT License.
#

from os import path
from setuptools import find_packages, setup


VERSION = (1, 2, 11)
__version__ = '.'.join(map(str, VERSION))


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-editor-ymaps',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    requires=['python (>= 3.5)', 'django (>= 2.0)'],
    description='Creating and editing Yandex maps.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='genkosta',
    author_email='genkosta43@gmail.com',
    url='https://github.com/genkosta/django-editor-ymaps',
    download_url='https://github.com/genkosta/django-editor-ymaps/tarball/master',
    license='MIT License',
    platforms=['any'],
    keywords=['django', 'yandex', 'maps', 'admin', 'editor'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=2.0',
        'Pillow',
        'django-imagekit',
        'python-slugify',
        'django-ckeditor',
        'lxml',
        'django-smart-selects==1.5.3',
        'django-ipware'
    ],
)
