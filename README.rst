.. figure:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/logo.png?raw=true
   :target: https://pypi.org/project/django-editor-ymaps/
   :alt: Logo

|

.. image:: https://img.shields.io/badge/pypi-v20.0.2%20-blue.svg
   :target: https://pypi.org/project/pip/
   :alt: PyPI badge
.. image:: https://img.shields.io/badge/python-%3E%3D%203.6-yellow.svg
   :target: https://www.python.org/
   :alt: Python badge
.. image:: https://img.shields.io/badge/django-%3E%3D%202.0-brightgreen.svg
   :target: https://www.djangoproject.com/
   :alt: Django badge
.. image:: https://pepy.tech/badge/django-editor-ymaps
   :target: https://pepy.tech/project/django-editor-ymaps
   :alt: Downloads badge
.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: https://github.com/kebasyaty/django-editor-ymaps/blob/master/LICENSE
   :alt: MIT badge

DjEYM ( django-editor-ymaps )
=============================
- **(ru)** *Удобное использование картографической службы Яндекса для веб-разработки на популярном и свободном фреймворке Django.*
- **(en)** *Convenient use of the Yandex map service for web development on the popular and free Django framework.*

Условия использования API Яндекс.Карт ( *Terms of use for the API* )
--------------------------------------------------------------------
- **(ru)** `Условия использования Яндекс.Карт <https://tech.yandex.ru/maps/jsapi/doc/2.1/quick-start/index-docpage/#get-api-key>`_
- **(ru)** `Получить API-ключ <https://tech.yandex.ru/maps/jsapi/doc/2.1/quick-start/index-docpage/#get-api-key>`_
- 
- **(en)** `Terms of use for the Yandex.Maps <https://tech.yandex.com/maps/jsapi/doc/2.1/terms/index-docpage/>`_
- **(en)** `Get the API key <https://tech.yandex.com/maps/jsapi/doc/2.1/quick-start/index-docpage/#get-api-key>`_

|

Attention
---------
- **(ru)** Версия 2.0 несовместима с предыдущей.
- **(en)** Version 2.0 is not compatible with the previous one.

|

Requirements
------------
- **Python** >= 3.6
- **Django** >= 2.0
- **Pillow** - `https://pypi.org/project/Pillow/ <https://pypi.org/project/Pillow/>`_
- **django-imagekit** - `https://github.com/matthewwithanm/django-imagekit <https://github.com/matthewwithanm/django-imagekit>`_
- **python-slugify** - `https://github.com/un33k/python-slugify <https://github.com/un33k/python-slugify>`_
- **django-ckeditor** - `https://github.com/django-ckeditor/django-ckeditor <https://github.com/django-ckeditor/django-ckeditor>`_
- **lxml** - `https://pypi.org/project/lxml/ <https://pypi.org/project/lxml/>`_
- **django-ipware** - `https://github.com/un33k/django-ipware <https://github.com/un33k/django-ipware>`_
- **django-colorful** - `<https://pypi.org/project/django-colorful/>`_
- **django-admin-sortable** - `<https://pypi.org/project/django-admin-sortable/>`_
-
- **Vue.js** - `<https://vuejs.org/>`_
- **Vuetify.js** - `<https://vuetifyjs.com/>`_

Installation
------------
Install libraries ( Ubuntu >= 18.04, Mint 19.x )::

    sudo apt install -y python-dev python3-dev libjpeg8-dev python-pil libevent-dev build-essential libpq-dev libxml2-dev libxslt1-dev gettext libjpeg-dev python-setuptools python3-setuptools

Install django-editor-ymaps using pip::

    pip install django-editor-ymaps

Settings
--------

Add settings::

    import os
    
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    INSTALLED_APPS = [
        ...
        'imagekit',
        'ckeditor',
        'ckeditor_uploader',
        'colorful',
        'adminsortable',
        'djeym',
        ...
    ]

    MIDDLEWARE = [
        ...
        'django.middleware.locale.LocaleMiddleware',
    ]

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.0/howto/static-files/
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # To send test messages.
    # 1. Notify administrator of a new custom marker.
    # 2. Notify user about successful moderation of his marker.
    # Mail server for testings: $ python -m smtpd -n -c DebuggingServer localhost:1025
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'noreply@site.net'

    # django-ckeditor
    # https://github.com/django-ckeditor/django-ckeditor
    CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
    CKEDITOR_UPLOAD_PATH = 'uploads/'
    CKEDITOR_FILENAME_GENERATOR = 'djeym.utils.get_filename'
    CKEDITOR_THUMBNAIL_SIZE = (300, 300)
    CKEDITOR_FORCE_JPEG_COMPRESSION = True
    CKEDITOR_IMAGE_QUALITY = 40
    CKEDITOR_IMAGE_BACKEND = 'pillow'
    CKEDITOR_ALLOW_NONIMAGE_FILES = False  # False - Only image files. (At your discretion)
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
            'colorButton_colors': 'F44336,C62828,E91E63,AD1457,9C27B0,6A1B9A,'
                                  '673AB7,4527A0,3F51B5,283593,2196F3,1565C0,'
                                  '03A9F4,0277BD,00BCD4,00838F,009688,00695C,'
                                  '4CAF50,2E7D32,8BC34A,558B2F,CDDC39,9E9D24,'
                                  'FFEB3B,F9A825,FFC107,FF8F00,FF9800,EF6C00,'
                                  'FF5722,D84315,795548,4E342E,607D8B,37474F,'
                                  '9E9E9E,424242,000000,FFFFFF',
            'colorButton_enableAutomatic': False,
            'colorButton_enableMore': True
        }
    }
    
    # (If a non-authenticated user requests an editor page.)
    # (Если не аутентифицированный пользователь запросит страницу редактора.)
    LOGIN_URL = '/admin/'  # or change to your URL
    
    # Required for django-admin-sortable
    # https://github.com/alsoicode/django-admin-sortable#configuration
    CSRF_COOKIE_HTTPONLY = False
    
    # The API key is used in the free and paid versions.
    # You can get the key in the developer’s office - https://passport.yandex.com/
    # ( API-ключ используется в свободной и платной версиях.
    #   Получить ключ можно в кабинете разработчика - https://developer.tech.yandex.ru/ )
    DJEYM_YMAPS_API_KEY = ''
    
    # For paid use API --> True
    # ( Для платного использования --> True )
    DJEYM_YMAPS_API_KEY_FOR_ENTERPRISE = False
    
    # Map download mode. Default = 'release'
    # (Режим загрузки карт.)
    # DJEYM_YMAPS_DOWNLOAD_MODE = 'debug'

Add to main URLs
----------------

urls.py::

    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.contrib.staticfiles.urls import static
    
    urlpatterns = [
        ...
        path('admin/', admin.site.urls),
        path('ckeditor/', include('ckeditor_uploader.urls')),
        path('djeym/', include('djeym.urls', namespace='djeym')),
        ...
    ] + static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    ) + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

Add media directory to your project
-----------------------------------

    media/uploads

Update Migrations
-----------------

    python manage.py migrate djeym

Usage
-----
1) Добавьте иконку кластера. ( *Add Cluster Icon.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте коллекцию кластеров. (Download the cluster collection.) <https://github.com/kebasyaty/django-editor-ymaps/blob/master/Cluster_Collection.zip?raw=true>`_
2. **Ознакомьтесь с содержимым архива.** ( *Read the contents of the archive.* )
3. **Выберите иконку кластера и добавьте по адресу - Панель администратора > ЯНДЕКС КАРТЫ > Иконки для кластеров > Добавить Иконку для кластеров.**
   ( *Select the cluster icon and add it to the address - Admin Panel > YANDEX MAPS > Icons for Clusters > Add Icon for Clusters.* )

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/add_cluster.png?raw=true
   :alt: Add Cluster

2) Добавьте коллекцию маркеров. ( *Add a collection of markers.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте коллекцию маркеров. (Download the marker collection.) <https://github.com/kebasyaty/django-editor-ymaps/blob/master/Marker_Collection.zip?raw=true>`_
2. **Ознакомьтесь с содержимым архива.** ( *Read the contents of the archive.* )
3. **Прочитайте readme файл, выберите коллекцию и добавьте через панель администратора.**
   ( *Read the readme file, select the collection and add it through the admin panel.* )

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/import_icon_collection.png?raw=true
   :alt: Import the Marker Collection

**Добавляя собственные иконки, проверяйте смещение по эталону.** ( *By adding your own icons, check the offset by standard.* )

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/offset_icon_for_markers.png?raw=true
   :alt: Check marker icon offset

3) Добавьте источники тайловых слоев. ( *Add tile sources.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте источники тайловых слоев. (Download tile sources.) <https://github.com/kebasyaty/django-editor-ymaps/blob/master/Tile.zip?raw=true>`_
2. **Ознакомьтесь с содержимым архива.** ( *Read the contents of the archive.* )
3. **Прочитайте readme файл и добавьте источники через панель администратора.** ( *Read the readme file and add sources through the admin panel.* )

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/import_tile_sources.png?raw=true
   :alt: Import the Tile Sources

4) Добавьте иконку индикатора загрузки. ( *Add loading indicator icon.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте иконки для индикатора загрузки. (Download the icon for the loading indicator.) <https://github.com/kebasyaty/django-editor-ymaps/blob/master/Spinner.zip?raw=true>`_
2. **Ознакомьтесь с содержимым архива.** ( *Read the contents of the archive.* )
3. **Прочитайте readme файл и добавьте иконку через панель администратора.** ( *Read the readme file and add the icon through the admin panel.* )

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/add_loading_indicator.png?raw=true
   :alt: Add Loading Indicator

5) Создайте вашу первую карту. ( *Create your first map.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. **Перейдите по адресу - Панель администратора > ЯНДЕКС КАРТЫ >  Карты > Добавить Карту.**
   ( *Navigate to the address - Admin Panel > YANDEX MAPS > Maps > Add Map.* )

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/create_map.png?raw=true
   :alt: Create map

6) Редактировать карту. ( *Edit map.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/edit_map.png?raw=true
   :alt: Edit map

Обзор страницы редактора. ( *Editor page overview.* )
-----------------------------------------------------

1) Меню редактора - Фильтры по категориям. ( *Editor Menu - Filters by category.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/editor_menu_filters.png?raw=true
   :alt: Editor Menu - Filters by category

2) Меню редактора - Источники тайлов. ( *Editor Menu - Tile Sources.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/editor_menu_tile.png?raw=true
   :alt: Editor Menu - Tile Sources

3) Меню редактора - Общие настройки. ( *Editor Menu - General settings.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/editor_menu_general_settings.png?raw=true
   :alt: Editor Menu - General settings

4) Меню редактора - Элементы управления. ( *Editor Menu - Controls.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/editor_menu_controls.png?raw=true
   :alt: Editor Menu - Controls

5) Меню редактора - Настройки тепловой карты. (*Editor Menu - Heatmap settings.*)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/editor_menu_heatmap.png?raw=true
   :alt: Editor Menu - Heatmap settings

6) Меню редактора - Индикаторы загрузки. (*Editor Menu - Loading indicators.*)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/editor_menu_loading_indicators.png?raw=true
   :alt: Editor Menu - Loading indicators

Добавление геообъектов на карту. ( *Adding geo-objects to the map.* )
---------------------------------------------------------------------

- **(ru)** Левый клик на карте, откроется меню с предложением выбрать тип объекта.
- **(en)** Left-clicking on the map opens a menu with a suggestion to choose the type of object.

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/adding_geo_objects.png?raw=true
   :alt: Adding geo-objects

- **(ru)** Маркер - Сменить иконку.
- **(en)** Marker - Change icon.

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/marker_change_icon.png?raw=true
   :alt: Marker - Change icon

- **(ru)** Пример маршрута на карте.
- **(en)** Example route on the map.

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/example_route.png?raw=true
   :alt: Example of the route

- **(ru)** Пример территории на карте.
- **(en)** An example of the territory on the map.

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/example_territory.png?raw=true
   :alt: Example of the territory

Выводим карту на страницу сайта. ( *Display a map on the site page.* )
----------------------------------------------------------------------

Добавьте в шаблон. ( Add to template. )::

    {% load i18n static djeymtags %}

    <head>
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">

      <!-- START VENDORS CSS -->
      <!-- Roboto Font:
            Usage (css):
              font-size: 16px;
              font-family: Roboto, sans-serif !important;
              font-weight: 100|300|400|500|700|900;
              font-style: italic!important; -->
      <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
      <!-- Material Design Icons:
            url: https://materialdesignicons.com/
            Usage (html):
              <span class="mdi mdi-name"></span>
              Size: mdi-18px|mdi-24px|mdi-36px|mdi-48px or font-size: 16px;
              Rotate: mdi-rotate-45|mdi-rotate-90|mdi-rotate-135|mdi-rotate-180|mdi-rotate-225|mdi-rotate-270|mdi-rotate-315
              Flip: mdi-flip-h|mdi-flip-v
              Color: mdi-light|mdi-light mdi-inactive|mdi-dark|mdi-dark mdi-inactive or color: #212121; -->
      <link href="https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css" rel="stylesheet">
      <!-- END VENDORS CSS -->
    </head>

    <body>
      <!-- START MAP -->
      <!-- Buttons are optional.
           (Кнопки не являются обязательными.) -->
      <style type="text/css">
        .djeym-button {
          font-family: Roboto, sans-serif !important;
          background-color: #4CAF50;
          border: none;
          color: white;
          padding: 10px 24px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          margin: 4px 2px;
          cursor: pointer;
        }
        .djeym-button-bar {
          display: none;
          margin-bottom: 10px;
        }
      </style>
      <div class="djeym-button-bar">
        <button id="djeym-open-panel" type="button" class="djeym-button">
          <span class="mdi mdi-arrow-expand-right"></span>
          Open Panel
        </button>
        <button id="djeym-add-marker" type="button" class="djeym-button">
          <span class="mdi mdi-map-marker-plus"></span>
          Add Marker
        </button>
      </div>
      <div id="djeym-app" class="djeym"></div>
      <!-- END MAP -->

      <!-- START VENDORS JS -->
      <script type="text/javascript" src="{% static "djeym/js/jquery.min.js" %}"></script>
      <script src="{% static "djeym/js/jquery-regex.min.js" %}"></script>
      ...
      {% djeym_yandex_map slug='test-map' lang=request.LANGUAGE_CODE %}
      <!-- END VENDORS JS -->
    </body>

Карта с открытой панелью. ( *Map with open panel.* )
----------------------------------------------------

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/map_opened_panel.png?raw=true
    :alt: Map with open panel

Карта с открытой формой для добавления пользовательских маркеров. ( *Map with an open form for adding custom markers.* )
------------------------------------------------------------------------------------------------------------------------

- **(ru)** Для безопасности, в названии и описании, все html теги удаляются.
- **(en)** For security, in the title and description, all html tags are deleted.

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/map_opened_form.png?raw=true
    :alt: Map with open form

Действия администратора после успешной модерации. ( *Admin actions after successful moderation.* )
------------------------------------------------------------------------------------------------------------------------

.. image:: https://github.com/kebasyaty/django-editor-ymaps/blob/master/screenshots_v3/after_successful_moderation.png?raw=true
    :alt: After successful moderation

Уведомление о новом пользовательском маркере. ( *Notification of a new custom marker.* )
----------------------------------------------------------------------------------------

Add in views.py::

    from django.core.mail import send_mail
    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from djeym.models import Placemark
    
    # SIMPLE EXAMPLE.
    # 1. Notify administrator of a new custom marker.
    # 2. Notify user about successful moderation of his marker.
    # Mail server for testings: $ python -m smtpd -n -c DebuggingServer localhost:1025
    @receiver(post_save, sender=Placemark)
    def notify_email(instance, **kwargs):
        """Notify by email of a new custom marker."""
    
        """
        # May come in handy. (Может пригодится.)
        title = instance.header  # (html)
        description = instance.body  # (html)
        image_url = instance.user_image.url
        """
        # Notify administrator of a new custom marker.
        if instance.is_user_marker and not instance.is_sended_admin_email:
            subject = 'Text subject'
            message = 'Text message - Url: ' + \
                'http(s)://your.domain/admin/djeym/placemark/{}/change/'.format(instance.pk)
            from_email = 'admin@site.net'  # or corporate email
            recipient_list = ['admin@site.net']  # Your work email
            send_mail(subject, message, from_email,
                      recipient_list, fail_silently=False)
            # Required
            instance.is_sended_admin_email = True
            instance.save()
        # Notify user about successful moderation of his marker.
        elif instance.active and instance.is_user_marker and not instance.is_sended_user_email:
            subject = 'Text subject'
            message = 'Text message'
            from_email = 'admin@site.net'  # Your work email
            recipient_list = [instance.user_email]
            send_mail(subject, message, from_email,
                      recipient_list, fail_silently=False)
            # Required
            instance.is_sended_user_email = True
            instance.save()

LICENSE
-------
- `MIT License <https://github.com/kebasyaty/django-editor-ymaps/blob/master/LICENSE>`_
- Copyright (c) 2014 kebasyaty

CHANGELOG
---------
#2.1.20
    - 1
    - (ru) Небольшая доработка рестайлинга на странице редактора.
    - (en) Small revision of the restyling on the editor page.
    - 2
    - (ru) Замена кнопки закрытия на всплывающем сообщении, на странице редактора.
    - (en) Replacing the close button on the popup message on the editor page.

#2.1.19
    - (ru) Небольшой рестайлинг страницы редактора.
    - (en) A small restyling of the editor page.

#2.1.18
    - (ru) Переход на MaterialDesignIcons v5.x - Обратите внимание на раздел `Выводим карту на страницу сайта`.
    - (en) Switching to MaterialDesignIcons v5.x - Pay attention to the section `Displaying the map on the site page`.

#2.1.17
    - 1
    - (ru) Исправлен баг для Django 3.1 - Ошибка при открытии страницы редактора.
    - (en) Fixed bug for Django 3.1 - Error opening editor page.
    - 2
    - (ru) Небольшой рестайлинг формы для добавления пользовательских маркеров.
    - (en) Small restyling of the form to add custom markers.

#2.1.16
    - (ru) Обновлен README.rst и восстановлены скриншоты для первой версии.
    - (en) Updated README.rst and restored screenshots for the first version.

#2.1.14
    - (ru) Небольшой рестайлинг страницы редактора.
    - (en) A small restyling of the editor page.

.. contents:: Contents
   :depth: 3
