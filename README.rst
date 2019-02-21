=====
DjEYM
=====
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

*******************
django-editor-ymaps
*******************
Удобное использование картографической службы Яндекса для веб-разработки на популярном и свободном фреймворке Django. (Convenient use of the Yandex map service for web development on the popular and free Django framework.)

************
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

************
Installation
************
Install using pip::

 pip install django-editor-ymaps

********
Settings
********
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

*****
Usage
*****
1) Добавьте иконку кластера. (Add Cluster Icon.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте коллекции иконок (Download icon collections) <https://github.com/genkosta/django-editor-ymaps/blob/master/Icon_Collections.zip?raw=true>`_
2. Ознакомьтесь с содержимым массива (Read the contents of the array)
3. Выберите иконку кластера и добавьте по адресу - Панель администратора > ЯНДЕКС КАРТЫ > Иконки для кластеров > Добавить Иконку для кластеров
   (Select the cluster icon and add it to the address - Admin Panel > YANDEX MAPS > Icons for Clusters > Add Icon for Clusters)

2) Добавьте коллекцию иконок (Add icon collection)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте коллекции иконок (Download icon collections) <https://github.com/genkosta/django-editor-ymaps/blob/master/Icon_Collections.zip?raw=true>`_
2. Ознакомьтесь с содержимым массива (Read the contents of the array)
3. Прочтите readme файл для выбранной коллекции и добавьте коллекцию через панель администратора.
   (Read the readme file for the selected collection and add the collection through the admin panel.)
