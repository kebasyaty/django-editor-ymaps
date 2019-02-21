============
DjEYM
============

.. image:: https://img.shields.io/badge/version-1.0%20beta-brightgreen.svg
   :target: https://pypi.org/project/django-editor-ymaps/
   :alt: Version
.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: https://github.com/genkosta/django-editor-ymaps/blob/master/LICENSE
   :alt: MIT
.. image:: https://pepy.tech/badge/django-editor-ymaps
   :target: https://pepy.tech/project/django-editor-ymaps
   :alt: Downloads
.. image:: https://img.shields.io/badge/django-%3E%3D%202.0-brightgreen.svg
   :target: https://www.djangoproject.com/
   :alt: Django
.. image:: https://img.shields.io/badge/python-%3E%3D%203.5-yellow.svg
   :target: https://www.python.org/
   :alt: Python

django-editor-ymaps
*******************
Удобное использование картографической службы Яндекса для веб-разработки на популярном и свободном фреймворке Django.

Requirements
************
- Python >= 3.5
- Django >= 2.0
- Pillow
- django-imagekit
- python-slugify
- django-ckeditor
- lxml
- django-smart-selects==1.5.3
- django-ipware

Installation
************
Install using pip::

 pip install django-editor-ymaps

Settings
********
Add 'djeym' to your INSTALLED_APPS setting::

 INSTALLED_APPS = [
     ...
     'imagekit',
     'smart_selects',
     'ckeditor',
     'ckeditor_uploader',
     'djeym',
     ...
 ]
