===========================
DjEYM (django-editor-ymaps)
===========================
.. image:: https://img.shields.io/badge/version-1.0%20beta-brightgreen.svg
   :target: https://pypi.org/project/django-editor-ymaps/
   :alt: Version
.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: https://github.com/genkosta/django-editor-ymaps/blob/master/LICENSE
   :alt: MIT
.. image:: https://pepy.tech/badge/django-editor-ymaps
   :target: https://pepy.tech/project/django-editor-ymaps
   :alt: Downloads
.. image:: https://img.shields.io/badge/python-%3E%3D%203.5-yellow.svg
   :target: https://www.python.org/
   :alt: Python
.. image:: https://img.shields.io/badge/django-%3E%3D%202.0-brightgreen.svg
   :target: https://www.djangoproject.com/
   :alt: Django

Description
===========
Удобное использование картографической службы Яндекса для веб-разработки на популярном и свободном фреймворке Django.

(Convenient use of the Yandex map service for web development on the popular and free Django framework.)

Requirements
------------
- Python (3.5, 3.6, 3.7)
- Django (2.0, 2.1, 2.2)
- Pillow - `https://pypi.org/project/Pillow/ <https://pypi.org/project/Pillow/>`_
- django-imagekit - `https://github.com/matthewwithanm/django-imagekit <https://github.com/matthewwithanm/django-imagekit>`_
- python-slugify - `https://github.com/un33k/python-slugify <https://github.com/un33k/python-slugify>`_
- django-ckeditor - `https://github.com/django-ckeditor/django-ckeditor <https://github.com/django-ckeditor/django-ckeditor>`_
- lxml - `https://pypi.org/project/lxml/ <https://pypi.org/project/lxml/>`_
- django-smart-selects==1.5.3 - `https://github.com/digi604/django-smart-selects <https://github.com/digi604/django-smart-selects>`_
- django-ipware - `https://github.com/un33k/django-ipware <https://github.com/un33k/django-ipware>`_


Installation
------------
Install using pip::

 pip install django-editor-ymaps

Settings
--------
Add apps to your INSTALLED_APPS setting::

    INSTALLED_APPS = [
        ...
        'imagekit',
        'smart_selects',
        'ckeditor',
        'ckeditor_uploader',
        'djeym',
        ...
    ]

Add other settings::

    # django-ckeditor
    CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
    CKEDITOR_UPLOAD_PATH = 'uploads/'
    CKEDITOR_FILENAME_GENERATOR = 'djeym.utils.get_filename'
    CKEDITOR_IMAGE_BACKEND = 'pillow'
    CKEDITOR_ALLOW_NONIMAGE_FILES = False  # Only image files. (На Ваше усмотрение)
    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': 'full',
            'height': 400,
            'width': '100%',
        },
        'djeym': {
            'toolbar': 'full',
            'height': 400,
            'width': 362,
            'colorButton_colors': 'FFFFFF,F08080,CD5C5C,FF0000,FF1493,C71585,800080,F0E68C,'
                                  'BDB76B,6A5ACD,483D8B,3CB371,2E8B57,9ACD32,008000,808000,'
                                  '20B2AA,008B8B,00BFFF,F4A460,CD853F,A52A2A,708090,34495e,'
                                  '999966,333333,82cdff,1e98ff,177bc9,0e4779,56db40,1bad03,'
                                  '97a100,595959,b3b3b3,f371d1,b51eff,793d0e,ffd21e,ff931e,'
                                  'e6761b,ed4543',
            'colorButton_enableAutomatic': False,
            'colorButton_enableMore': True
        }
    }
    
    # Add your URL
    LOGIN_URL = '/login/'
    
    # django-smart-selects
    # https://github.com/digi604/django-smart-selects
    JQUERY_URL = False
    USE_DJANGO_JQUERY = True
    
    # API key - Used only in the paid API version.
    # You can get the key in the developer’s office - https://developer.tech.yandex.ru/
    # ( API-ключ - Используется только в платной версии API.
    #   Получить ключ можно в кабинете разработчика - https://developer.tech.yandex.ru/ )
    DJEYM_YMAPS_API_KEY = ''
    
    # Map download mode. Default -> 'release'
    # (Режим загрузки карт.)
    # DJEYM_YMAPS_DOWNLOAD_MODE = 'debug'
    
    # Font Awesome, Material Design etc.
    # Default Font Awesome Free 5.3.1 - https://fontawesome.com
    # Example: ['/static/path/css/style.min.css']
    # Example: ['/static/path/js/script.min.js']
    # Only for admin panel and editor page. (Только для панели администратора и страницы редактора.)
    # For the site connect directly in templates. (Для сайта подключите непосредственно в шаблонах.)
    DJEYM_YMAPS_ICONS_FOR_CATEGORIES_CSS = []
    DJEYM_YMAPS_ICONS_FOR_CATEGORIES_JS = []

Update Migrations::

    python manage.py migrate djeym

Usage
-----
1) Добавьте иконку кластера. (Add Cluster Icon.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте коллекции иконок. (Download icon collections.) <https://github.com/genkosta/django-editor-ymaps/blob/master/Icon_Collections.zip?raw=true>`_
2. Ознакомьтесь с содержимым массива. (Read the contents of the array.)
3. Выберите иконку кластера и добавьте по адресу - Панель администратора > ЯНДЕКС КАРТЫ > Иконки для кластеров > Добавить Иконку для кластеров.
   (Select the cluster icon and add it to the address - Admin Panel > YANDEX MAPS > Icons for Clusters > Add Icon for Clusters.)

2) Добавьте коллекцию иконок. (Add icon collection.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте коллекции иконок. (Download icon collections.) <https://github.com/genkosta/django-editor-ymaps/blob/master/Icon_Collections.zip?raw=true>`_
2. Ознакомьтесь с содержимым массива. (Read the contents of the array.)
3. Прочитайте readme файл для выбранной коллекции и добавьте коллекцию через панель администратора.
   (Read the readme file for the selected collection and add the collection through the admin panel.)

.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/import_icon_collection.png?raw=true
   :alt: Import Icon Collection

Добавляя собственные иконки, проверяйте смещение по эталону. (By adding your own icons, check the offset by standard.)
*************************************************************************************************************
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/change_icon_for_markers.png?raw=true
   :alt: Change Icon for markers

3) Добавьте источники тайловых слоев. (Add tile sources.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте источники тайловых слоев. (Download tile sources.) <https://github.com/genkosta/django-editor-ymaps/blob/master/Tile.zip?raw=true>`_
2. Ознакомьтесь с содержимым массива. (Read the contents of the array.)
3. Прочитайте readme файл и добавьте источники через панель администратора. (Read the readme file and add sources through the admin panel.)

4) Создайте вашу первую карту. (Create your first map.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Перейдите по адресу - Панель администратора > ЯНДЕКС КАРТЫ >  Карты > Добавить Карту.
   (Navigate to the address - Admin Panel > Yandex Maps > Maps > Add Map.)

5) Создайте категории геообъектов нужного типа для новой карты. (Create categories of geo-objects of the desired type for the new map.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Категории маркеров. (Marker categories.)
2. Подкатегории маркеров. (Subcategories of markers.)
3. Категории маршрутов. (Categories of routes.)
4. Категории территорий. (Categories of territories.)

6) Редактировать карту. (Edit map.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/edit_map.png?raw=true
   :alt: Edit map

Обзор страницы редактора. (Editor page overview.)
-------------------------------------------------

1) Меню редактора - Иконки. (Editor Menu - Icons.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Доступ только для персонала. (Access only to staff.)
****************************************************
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_icons.png?raw=true
   :alt: Editor Menu - Icons

2) Меню редактора - Фильтры по категориям. (Editor Menu - Filters by category.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_filters.png?raw=true
   :alt: Editor Menu - Filters by category

3) Меню редактора - Источники тайлов. (Editor Menu - Tile Sources.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_tile.png?raw=true
   :alt: Editor Menu - Tile Sources

4) Меню редактора - Общие настройки. (Editor Menu - General settings.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_settings.png?raw=true
   :alt: Editor Menu - General settings
