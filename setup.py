#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Convenient use of the Yandex map service for web development on 
#  the popular and free Django framework.
#
#  Copyright (c) 2014-2019 genkosta
#
#  django-editor-ymaps is free software under terms of the MIT License.
#

from setuptools import find_packages, setup


VERSION = (1, 0)
__version__ = '.'.join(map(str, VERSION))


def get_readme(file_path):
    with open(file_path, 'r', encoding='utf-8') as readme_file:
        result = readme_file.read()
    return result


setup(
    name='django-editor-ymaps',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    requires=['python (>= 3.5)', 'django (>= 2.0)'],
    description='Creating and editing Yandex maps.',
    long_description=get_readme('README.rst'),
    long_description_content_type='text/x-rst',
    author='genkosta',
    author_email='genkosta43@gmail.com',
    url='https://github.com/genkosta/django-editor-ymaps',
    download_url='https://github.com/genkosta/django-editor-ymaps/tarball/master',
    license='MIT License',
    platforms=['any'],
    keywords='django yandex map maps djeym',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
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
