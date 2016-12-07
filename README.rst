django-editor-ymaps
===================

Удобное использование Яндекс-Карт в проектах на Django.

version **0.2.1**

Проверено на Django 1.8 и 1,9 , Python 2.7

Данное дополнение, предназначено для работы с яндекс-картами.
Все настройки и переход на страницу редактора, 
располагаются на панели администратора.
Имеется возможность, добавлять на карту геообъекты типа placemark, polyline и polygon.
Также можно добавить и настроить свои иконки для маркеров и кластеризатора.
Ссылка на страницу редактора, расположена в левом верхнем углу, в настройках карт.


Автоустановка необходимого ПО:
++++++++++++++++++++++++++++++

::

    1. Pillow
    2. django-imagekit
    3. django-tinymce
    4. djlime-filebrowser
    5. python-slugify
    6. django-smart-selects


Установка:
++++++++++

::

    pip install django-editor-ymaps


settings:
+++++++++

::

    INSTALLED_APPS = [
        ...
        
        'imagekit',
        'tinymce',
        'djlime_filebrowser',
        'smart_selects',
        'yandex_maps',
    ]
    
    # Здесь ставьте свои настройки. Для карт, они подгружаются отдельно.
    # https://github.com/aljosa/django-tinymce
    TINYMCE_DEFAULT_CONFIG = { ... }

    # Файловый браузер, настройте как принято в Ваших проектах,
    # или воспользуйтесь настройками ниже.
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ROOT = os.path.normpath(os.path.join(PROJECT_DIR, ".."))
    root_path = lambda *args: os.path.join(ROOT, *args)
    path = lambda *args: os.path.join(PROJECT_DIR, *args)
    
    # filebrowser - https://github.com/freshlimestudio/djlime-filebrowser
    TINYMCE_FILEBROWSER = True
    FILEBROWSER_PATH_TINYMCE = path(STATIC_ROOT, '/tiny_mce/')
    FILEBROWSER_URL_TINYMCE = STATIC_URL+'/tiny_mce/'
    FILEBROWSER_PATH_FILEBROWSER_STATIC = path(STATIC_ROOT, 'filebrowser/')
    FILEBROWSER_URL_FILEBROWSER_STATIC = STATIC_URL+'filebrowser/'
    FILEBROWSER_VERSIONS_BASEDIR = 'thumbnails/'
    FILEBROWSER_EXTENSIONS = {
        'Image': ['.jpg', '.jpeg', '.gif', '.png'],
        'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv'],
    }
    FILEBROWSER_MAX_UPLOAD_SIZE = '1024000'


urls:
+++++

::

    urlpatterns = patterns(
        '',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^chaining/', include('smart_selects.urls')),
        url(r'^tinymce/', include('tinymce.urls')),
        url(r'^admin/filebrowser/', include('djlime_filebrowser.urls')),
        url(r'^yandex_maps/', include('yandex_maps.urls', namespace='yandex_maps')),
    )


migrate:
++++++++

::

    python manage.py migrate


templates:
++++++++++

::

    {% load ymaptags %}
    
    <head>
    <link rel="stylesheet" type="text/css" href="{% static 'yandex_maps/css/ymap_front.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'yandex_maps/switchery/switchery.min.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'yandex_maps/ymap_tinymce/css/front_tinymce.css' %}">

    <script src="https://api-maps.yandex.ru/2.1/?lang=ru_RU" type="text/javascript"></script>
    <script type="text/javascript" src="{% static 'js/jquery.js' %}"></script>
    <script type="text/javascript" src="{% static 'yandex_maps/js/jquery.json.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'yandex_maps/switchery/switchery.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'yandex_maps/js/ymap_front_load.js' %}"></script>
    </head>
    <body>
    <h1>Карта</h1>
    <!-- parameters: slug_map width height -->
    {% load_ymap 'supermarkety-kharkova' 'auto' '400px' %}
    </body>


Скриншоты:
++++++++++


Кнопка перехода на страницу редактора.
-------------------------------------
.. class:: no-web
    
    .. image:: https://raw.githubusercontent.com/genkosta/django-editor-ymaps/master/images/02.png
        :alt: Кнопка перехода на страницу редактора.
        :width: 100%


Центровка карты.
----------------

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/genkosta/django-editor-ymaps/master/images/05.png
        :alt: Центровка карты.
        :width: 100%


Фрагмент страницы редактора с открытой панелью.
----------------------------------------------

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/genkosta/django-editor-ymaps/master/images/04.png
        :alt: Фрагмент страницы редактора с открытой панелью.
        :width: 100%


Добавить объект на карту (левый клик).
----------------------------------------------

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/genkosta/django-editor-ymaps/master/images/07.png
        :alt: Добавить объект на карту (левый клик).
        :width: 100%


Настройки метки (правый клик на объекте).
----------------------------------------------

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/genkosta/django-editor-ymaps/master/images/09.png
        :alt: Настройки метки (правый клик на объекте).
        :width: 100%


Карта на странице сайта, с открытой панелью для выбора геообъектов.
-------------------------------------------------------------------

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/genkosta/django-editor-ymaps/master/images/01.png
        :alt: Карта на странице сайта, с открытой панелью для выбора геообъектов.
        :width: 100%

