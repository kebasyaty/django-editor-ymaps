.. figure:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/logo.png?raw=true
   :target: https://pypi.org/project/django-editor-ymaps/
   :alt: Logo

|

.. image:: https://img.shields.io/badge/version-1.2.11%20beta-brightgreen.svg
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

DjEYM ( django-editor-ymaps )
=============================
**Удобное использование картографической службы Яндекса для веб-разработки на популярном и свободном фреймворке Django.**

( *Convenient use of the Yandex map service for web development on the popular and free Django framework.* )

Условия использования API Яндекс.Карт ( *Terms of use for the API* )
--------------------------------------------------------------------
- `Условия использования API Яндекс.Карт <https://tech.yandex.ru/maps/doc/jsapi/2.1/terms/index-docpage/>`_

- `Terms of use for the API <https://tech.yandex.com/maps/doc/jsapi/2.1/terms/index-docpage/>`_

.. attention::
   **При переходе на версию 1.2, обновите миграции:** python manage.py migrate djeym

   **Обратите внимание на раздел -** `Выводим карту на страницу сайта. <https://pypi.org/project/django-editor-ymaps/#display-a-map-on-the-site-page>`_ **Добавлены минимизированные файлы (.min.)**.

   **When upgrading to version 1.2, upgrade the migration:** python manage.py migrate djeym

Features
--------
1. **Через панель администратора, создавать новые карты с богатой возможностью настроек.** ( *Through the admin panel, create new maps with a wide range of options.* )

2. **Редактировать карты на специальной странице редактора, с доступом только для персонала.** ( *Edit maps on a special page of the editor, with access only for staff.* )

3. **Создавать геообъекты четырех типов - Маркеры, маршруты, территории и тепловые точки.** ( *Create geo-objects of four types - Markers, routes, territories and heat points.* )

4. **Использовать кастомные иконки для кластеров и маркеров в формате SVG.** ( *Use custom icons for clusters and markers in the format SVG.* )

5. **Создавать категории и подкатегории для фильтрации геообъектов на карте.** ( *Create categories and subcategories for filtering geo objects on the map.* )

6. **Добавлять источники тайловых слоев и API-ключи к ним (если требуется). Имеется возможность добавить стандартный набор из 21 источника.** ( *Add tile layer sources and API keys to them (if required). It is possible to add a standard set of 21 sources.* )

7. **Скрывать ненужные элементы управления на картах.** ( *Hide unnecessary controls on maps.* )

8. **Активировать тепловой слой, изменять настройки слоя и создавать тепловые точки.** ( *Activate the thermal layer, change the layer settings and create heat points.* )

9. **Имеется возможность создавать и управлять пресетами для автоматической вставки некоторой текстовой информации или дополнительного функционала в информационных окнах геообъектов. Для каждой карты добавляются два стандартных пресета (Text и Likes).** ( *It is possible to create and manage presets for automatic insertion of some textual information or additional functionality in the information windows of geoobjects. Two standard presets are added for each map (Text and Likes).* )

10. **Начиная с версии 1.1, добавлен шаблонный тег для прямого геокодирования. Например - На странице профиля, геокодер получает адрес пользователя и отображает его маркером на отдельной карте. Эти карты независимы, их ненужно создавать через панель администратора. Ниже, в документации, есть пример с описанием.** ( *Starting with version 1.1, a template tag has been added for direct geocoding. For example - On the profile page, the geocoder receives the user's address and displays it with a marker on a separate map. These cards are independent, it is unnecessary to hack them through the admin panel. Below, in the documentation, there is an example with a description.* )

11. **Начиная с версии 1.2, имеется возможность добавить индикатор загрузки в иноформационные окна геообектов. Назначение индикатора, в основном декоративное. На GitHub-е проекта находится архив с иконками ( Spinner.zip ). При переходе на версию 1.2, обновите миграции.** ( *Starting from version 1.2, it is possible to add a loading indicator to the information windows of geo objects. The purpose of the indicator, mostly decorative. On the GitHub project there is an archive with icons (Spinner.zip). When upgrading to version 1.2, upgrade the migration.* )

Requirements
------------
- **Python** (3.5, 3.6, 3.7)
- **Django** (2.0, 2.1, 2.2)
- **Pillow** - `https://pypi.org/project/Pillow/ <https://pypi.org/project/Pillow/>`_
- **django-imagekit** - `https://github.com/matthewwithanm/django-imagekit <https://github.com/matthewwithanm/django-imagekit>`_
- **python-slugify** - `https://github.com/un33k/python-slugify <https://github.com/un33k/python-slugify>`_
- **django-ckeditor** - `https://github.com/django-ckeditor/django-ckeditor <https://github.com/django-ckeditor/django-ckeditor>`_
- **lxml** - `https://pypi.org/project/lxml/ <https://pypi.org/project/lxml/>`_
- **django-smart-selects==1.5.3** - `https://github.com/digi604/django-smart-selects <https://github.com/digi604/django-smart-selects>`_
- **django-ipware** - `https://github.com/un33k/django-ipware <https://github.com/un33k/django-ipware>`_

Installation
------------
Install libraries ( Ubuntu >= 18.04, Mint 19.x )::

    sudo apt install python-dev python3-dev libjpeg8-dev python-pil libevent-dev build-essential libpq-dev libxml2-dev libxslt1-dev gettext libjpeg-dev

Install django-editor-ymaps using pip::

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
    LOGIN_URL = '/admin/'
    
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

Add to main URLs::

    urlpatterns = [
        ...
        path('chaining/', include('smart_selects.urls')),
        path('ckeditor/', include('ckeditor_uploader.urls')),
        path('djeym/', include('djeym.urls', namespace='djeym')),
        ...
    ]

Add directory to your project::

    media/uploads

Update Migrations::

    python manage.py migrate djeym

Usage
-----
1) Добавьте иконку кластера. ( *Add Cluster Icon.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте коллекции иконок. (Download icon collections.) <https://github.com/genkosta/django-editor-ymaps/blob/master/Icon_Collections.zip?raw=true>`_
2. **Ознакомьтесь с содержимым архива.** ( *Read the contents of the archive.* )
3. **Выберите иконку кластера и добавьте по адресу - Панель администратора > ЯНДЕКС КАРТЫ > Иконки для кластеров > Добавить Иконку для кластеров.**
   ( *Select the cluster icon and add it to the address - Admin Panel > YANDEX MAPS > Icons for Clusters > Add Icon for Clusters.* )

2) Добавьте коллекцию иконок. ( *Add icon collection.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте коллекции иконок. (Download icon collections.) <https://github.com/genkosta/django-editor-ymaps/blob/master/Icon_Collections.zip?raw=true>`_
2. **Ознакомьтесь с содержимым архива.** ( *Read the contents of the archive.* )
3. **Прочитайте readme файл для выбранной коллекции и добавьте коллекцию через панель администратора.**
   ( *Read the readme file for the selected collection and add the collection through the admin panel.* )

.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/import_icon_collection.png?raw=true
   :alt: Import Icon Collection

**Добавляя собственные иконки, проверяйте смещение по эталону.** ( *By adding your own icons, check the offset by standard.* )

.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/offset_icon_for_markers.png?raw=true
   :alt: Change Icon for markers

3) Добавьте источники тайловых слоев. ( *Add tile sources.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. `Скачайте источники тайловых слоев. (Download tile sources.) <https://github.com/genkosta/django-editor-ymaps/blob/master/Tile.zip?raw=true>`_
2. **Ознакомьтесь с содержимым архива.** ( *Read the contents of the archive.* )
3. **Прочитайте readme файл и добавьте источники через панель администратора.** ( *Read the readme file and add sources through the admin panel.* )

4) Создайте вашу первую карту. ( *Create your first map.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. **Перейдите по адресу - Панель администратора > ЯНДЕКС КАРТЫ >  Карты > Добавить Карту.**
   ( *Navigate to the address - Admin Panel > YANDEX MAPS > Maps > Add Map.* )

5) Создайте категории геообъектов нужного типа для новой карты. ( *Create categories of geo-objects of the desired type for the new map.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. **Категории маркеров.** ( *Marker categories.* )
2. **Подкатегории маркеров.** ( *Subcategories of markers.* )
3. **Категории маршрутов.** ( *Categories of routes.* )
4. **Категории территорий.** ( *Categories of territories.* )

6) Редактировать карту. ( *Edit map.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/edit_map.png?raw=true
   :alt: Edit map

Обзор страницы редактора. ( *Editor page overview.* )
-----------------------------------------------------

1) Меню редактора - Иконки. ( *Editor Menu - Icons.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **Доступ только для персонала.** ( *Access only to staff.* )

.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_icons.png?raw=true
   :alt: Editor Menu - Icons

2) Меню редактора - Фильтры по категориям. ( *Editor Menu - Filters by category.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_filters.png?raw=true
   :alt: Editor Menu - Filters by category

3) Меню редактора - Источники тайлов. ( *Editor Menu - Tile Sources.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_tile.png?raw=true
   :alt: Editor Menu - Tile Sources

4) Меню редактора - Общие настройки. ( *Editor Menu - General settings.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_settings.png?raw=true
   :alt: Editor Menu - General settings

5) Меню редактора - Настройки тепловой карты. (*Editor Menu - Heatmap settings.*)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_heatmap.png?raw=true
   :alt: Editor Menu - Heatmap settings

6) Меню редактора - Пресеты. ( *Editor Menu - Presets.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **Имеется возможность создавать свои пресеты.** ( You can create your own presets. )

   Панель администратора > ЯНДЕКС КАРТЫ >  Карты > Карта > ПРЕСЕТЫ > Добавить еще один Пресет

   ( *Admin Panel > YANDEX MAPS > Maps > Map > PRESETS > Add another preset* )

.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editor_menu_presets.png?raw=true
   :alt: Editor Menu - Presets

Добавление геообъектов на карту. ( *Adding geo-objects to the map.* )
---------------------------------------------------------------------
1) Добавим маркер. ( *Add a marker.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. **Левый клик на карте, откроется меню с предложением выбрать тип объекта.** ( *Left-clicking on the map opens a menu with a suggestion to choose the type of object.* )

2. **Выбираем кнопку - Добавить новый Маркер.** ( *Select the button - Add a new Marker.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/add_marker.png?raw=true
       :alt: Add a marker

3. **Выберите подходящую иконку.** ( *Choose the appropriate icon.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/%D1%81hoose_an_icon.png?raw=true
       :alt: Choose an icon

4. **Добавим информацию об объекте.** ( *Add information about the object.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/add_info.png?raw=true
       :alt: Add Info

    - **Каждая из кнопок открывает свое окно текстового редактора.** ( *Each of the buttons opens its text editor window.* )
        .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/popup_with_text_editor.png?raw=true
           :alt: Popup with text editor

5. **Выбираем категорию для геообъекта.** ( *Select a category for a geoobject.* )
    - **Открываем категории.** ( *Open categories.* )
        .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/select_category.png?raw=true
           :alt: Open categories

    - **Выбираем категорию.** ( *Choose a category.* )
        .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/select_category_2.png?raw=true
           :alt: Choose a category

6. **Нажимаем кнопку "+" и получаем результат.** ( *Press the "+" button and get the result.* )
    - pic 1
        .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/result_1.png?raw=true
           :alt: View result 1

    - pic 2
        .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/result_2.png?raw=true
           :alt: View result 2

7. **Геообъекты редактируются через контекстное меню - Сделайте правый клик на объекте и внесите нужные изменения. Чтобы сохранить результат, нажмите кнопку с изображением дискеты.** ( *Geo-objects are edited via the context menu - Right-click on the object and make the necessary changes. To save the result, click the button with the image of a floppy disk.* )
    - pic
        .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/update_info.png?raw=true
           :alt: Update info

2) Вид Кластера. ( *Cluster View.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **Кластер** ( *Cluster* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/cluster.png?raw=true
       :alt: Cluster

- **Popup - Two columns**
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/cluster_popup_two_columns.png?raw=true
       :alt: Two columns

- **Popup - Carousel**
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/cluster_popup_carousel.png?raw=true
       :alt: Carousel

3) Маршрут. ( *Route.* )
^^^^^^^^^^^^^^^^^^^^^^^^
- **Добавить маршрут.** ( *Add route.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/add_route.png?raw=true
       :alt: Add route

- **Результат.** ( *Result.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/result_route.png?raw=true
       :alt: Result

- **Редактировать** ( *Edit* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editing_route.png?raw=true
       :alt: Edit

- **Можно настроить соответствие по цвету.** ( *You can adjust the color matching.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/route_color_matching.png?raw=true
       :alt: Color matching

4) Территория. ( *Territory.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **Добавить территорию.** ( *Add territory.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/add_territory.png?raw=true
       :alt: Add territory

- **Результат.** ( *Result.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/result_territory.png?raw=true
       :alt: Result

- **Редактировать** ( *Edit* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/editing_territory.png?raw=true
       :alt: Edit

- **Можно настроить соответствие по цвету.** ( *You can adjust the color matching.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/territory_color_matching.png?raw=true
       :alt: Color matching

5) Тепловая карта. ( *Heatmap.* )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **Добавить тепловую точку.** ( *Add heat point.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/add_heatpoint.png?raw=true
       :alt: Add heat point

- **Добавить информацию.** ( *Add information.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/heatpoint_add_info.png?raw=true
       :alt: Add info

Выводим карту на страницу сайта. ( *Display a map on the site page.* )
----------------------------------------------------------------------

Добавьте в шаблон. ( Add to template. )::

    {% load i18n staticfiles djeymtags %}

    <head>
        <!-- START CSS -->
        <link rel="stylesheet" type="text/css" href="{% static "djeym/plugins/fontawesome/css/all.min.css" %}">
        <link rel="stylesheet" type="text/css" href="{% static "djeym/plugins/boxiOS/boxios.min.css" %}">
        <link rel="stylesheet" type="text/css" href="{% static "djeym/css/ymfront.min.css" %}">
        <!-- END CSS -->
    </head>

    <body>
      <!-- START MAP -->
      <div id="djeymYMapsID" class="djeym-ymap" style="width: auto; height: 400px"></div>
      <!-- END MAP -->

        <!-- START JS -->
        <script type="text/javascript" src="{% static "djeym/js/jquery-3.3.1.min.js" %}"></script>
        <script type="text/javascript" src="{% static "djeym/plugins/boxiOS/boxios.min.js" %}"></script>
        <script type="text/javascript" src="{% static "djeym/plugins/fontawesome/js/all.min.js" %}"></script>
        {% djeym_load_ymap slug='test' panel='djeym/includes/panel.html' %}
        <!-- END JS -->
    </body>

- **Карта с закрытой панелью.** ( *Map with a closed panel.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/map_closed_panel.png?raw=true
       :alt: Map with a closed panel

- **Карта с открытой панелью.** ( *Map with open panel.* )
    .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/map_opened_panel.png?raw=true
       :alt: Map with open panel

Custom Commands
---------------
- **Для того, чтобы проверить производительность ( достаточна ли она для вашего проекта ) - С помощью команды "addmarker", добавьте некоторое количество маркеров на карту.** ( *In order to check the performance (whether it is sufficient for your project) - Using the "addmarker" command, add a certain number of markers to the map.* )

1. `Скачайте архив, распакуйте и добавьте файлы в свой медиа-раздел. ( Download archive, unpack and add files to your media section. ) <https://github.com/genkosta/django-editor-ymaps/blob/master/media.zip?raw=true>`_

2. **Запустите команду.** ( *Run the command.* )

  Запустите в корневой директории вашего проекта. ( Run in the root directory of your project. )::

    # Название карты: Test ( Map name: Test )
    #
    # Рекомендуется для настроек карты. ( Recommended for map settings. )
    # Масштаб ( Zoom ): 3
    # Широта ( Latitude ): 0
    # Долгота ( Longitude ): 0

    # --count - Default = 100
    python manage.py addmarker --count 1000

  .. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/result_addmarker.png?raw=true
     :alt: Command result - addmarker

Использование Геокодера. ( *Using Geocoder.* )
----------------------------------------------
- **Начиная с версии 1.1, добавлен шаблонный тег для прямого геокодирования. Например - На странице профиля, геокодер получает адрес пользователя и отображает его маркером на отдельной карте. Эти карты независимы, их ненужно создавать через панель администратора.** ( *Starting with version 1.1, a template tag has been added for direct geocoding. For example - On the profile page, the geocoder receives the user's address and displays it with a marker on a separate map. These cards are independent, it is unnecessary to hack them through the admin panel.* )

`Условия использования API Геокодера <https://tech.yandex.ru/maps/doc/geocoder/desc/concepts/limits-docpage/>`_

`Terms of use for the Geocoder API <https://tech.yandex.com/maps/doc/geocoder/desc/concepts/limits-docpage/>`_

Добавьте в шаблон. ( Add to template. )::

    {% load i18n staticfiles djeymtags %}

    <body>
        <!-- START MAP -->
        <div id="djeymYMapsID" class="djeym-ymap" style="width: auto; height: 400px"></div>
        <!-- END MAP -->

        <!-- START JS -->
        <!--
        // Address. (Адрес.)
        address = country + region + city + district + street + house
        // Address Example: 'Россия, Белгородская обл., Старый Оскол, мкр. Жукова, дом 29а'
    
        // Map Controls. (Элементы управления картой.)
        controls = 'all' // Default -> 'zoom'
    
        // Tile layer map. (Тайловый слой карты.)
        tile_slug = 'openstreetmap' // Default -> 'default'
    
        // Marker icon. (Иконка маркера.)
        marker_slug = 'home-light-blue-sherry' // Default -> 'default'
    
        // Load indicator icon. (Иконка индикатора загрузки.)
        load_indicator_slug = 'platinum-circle' // Default -> 'default'
    
        // Load indicator size (Размер индикатора нагрузки.)
        size = '96' - (64, 96, 128) // Default -> '64'

        // Скорость анимации для индикатора загрузки. ( Animation speed for loading indicator. )
        speed = '0.3' - (0.3-1.8) // Default -> '0.8'
        -->
        {% ymap_geocoder address='Россия, Белгородская обл., Старый Оскол, мкр. Жукова, дом 29а' tile_slug='openstreetmap' marker_slug='home-light-blue-sherry' load_indicator_slug='platinum-circle' size='96' speed='0.3' %}
        <!-- END JS -->
    </body>

.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/geocoder.png?raw=true
  :alt: Geocoder

Первый вариант логотипа. ( *The first version of the logo.* )
-------------------------------------------------------------
- **Возможно пригодится для поклонников теории плоской земли.** ( *Perhaps useful for fans of the theory of flat land.* )

- `Скачать архив изображений в месте с проектным файлом (xcf) для редактора GIMP. <https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/first_logo/first_logo.zip?raw=true>`_

- `Download the image archive in place with the project file (xcf) for the GIMP editor. <https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/first_logo/first_logo.zip?raw=true>`_

.. image:: https://github.com/genkosta/django-editor-ymaps/blob/master/screenshots/first_logo/first_logos.png?raw=true
   :alt: First logo

LICENSE
-------
- `MIT License <https://github.com/genkosta/django-editor-ymaps/blob/master/LICENSE>`_
- Copyright (c) 2014 genkosta

Donation
--------
- `Yandex Money <https://money.yandex.ru/to/410015413221944>`_

CHANGELOG
---------
- # 1.2.11
    - Добавлен дефолтный шрифт в инфо-окна геообъектов и окна контекстного меню. ( Added default font in geo-objects info-windows and context menu windows. )

- # 1.2.10
   - Обновлены стили для панели, для страницы сайта. Добавлен дефолтный шрифт. ( Updated styles for the panel for the page. Added default font. )

- # 1.2.9
    - Обновлена панель для страницы редактора. ( Updated panel page editor. )

- # 1.2.8
    - Индикатор загрузки - В панель редактора карт, добавлено уточнение для величины скорости анимации. ( Load Indicator - In the panel of the map editor, added clarification for the value of the speed of animation. )

- # 1.2.7
    - В настройки карт добавлен параметр - Скорость анимации для индикатора загрузки. ( Added a parameter to the map settings - Animation speed for the load indicator. )
    - Добавлен параметр "speed" для Геокодера. ( Added "speed" parameter for Geocoder. )
    - `Использование Геокодера. ( Using Geocoder. ) <https://pypi.org/project/django-editor-ymaps/#using-geocoder>`_
    - Обновите миграции. ( Update the migration. )
    - python manage.py migrate djeym

- # 1.2.6
    - Минимизированы файлы CSS и JS, загружаемые  в панель администратора. ( The CSS and JS files loaded into the admin panel are minimized. )

- # 1.2.5
    - Исправлено отсутствие полной поддержки для SQLite3.
    - За комментарии на GitHub-е, отдельное спасибо `Александру Бардину. <https://github.com/AlexanderBardin>`_

- # 1.2.4
    - Обновленная панель для страницы редактора карт. Изменения сделаны для раздела - Помощь.
    - ( Updated panel for the map editor page. Changes are made to the section - Help. )
    - Обратите внимание на раздел - `Выводим карту на страницу сайта. <https://pypi.org/project/django-editor-ymaps/#display-a-map-on-the-site-page>`_ Добавлены минимизированные файлы (.min.).

- # 1.2.3
    - Сделаны исправления и улучшения для индикатора загрузки.
    - ( Made fixes and improvements for the load indicator. )

- # 1.2.2
    - Индикатор загрузки - Исправлено некорректное определение минимальной высоты окна для геообъекта.
    - ( Load Indicator - Fixed incorrect determination of the minimum window height for a geoobject. )

- # 1.2.1
    - Обновлен индикатор загрузки. ( Updated load indicator. )
    - Обновите миграции. ( Update the migration. )
    - python manage.py migrate djeym

- # 1.2
    - Возможность добавить индикатор загрузки в информационные ока геообъектов.  На GitHub-е проекта находится архив с иконками ( Spinner.zip ). ( Ability to add a loading indicator to the information eye of geo objects. On the GitHub project there is an archive with icons (Spinner.zip). )
    - Обновлен Геокодер и его настройки. Новые настройки имеются в описании выше. ( Updated Geocoder and its settings. New settings are available in the description above. )
    - Сделано несколько небольших исправлений. ( Made a few minor fixes. )
    - При переходе на версию 1.2, обновите миграции. ( When upgrading to version 1.2, upgrade the migration. )
    - python manage.py migrate djeym

- # 1.1
    - Добавлен Геокодер, пример использования в описании выше. ( Added Geocoder, an example of use in the description above. )

- # 1.0.11
    - Optimized update information for presets.

- # 1.0.10
    - Tile Sources - Updated templatetags - random_domain ( increased subdomains scatter ).

- # 1.0.9
    - Updated custom command - addmarker.
    - Updated admin panel section - Change icon for markers.

- # 1.0.8
    - Admin panel, section "Change Icon for markers" - The size of the icons on the map is increased, for the convenience of correction the offset.

- # 1.0.7
    - Optimized map panel for the site page.

- # 1.0.6
    - Custom command "addmarker" - The value of the variable Slug is changed to "test".
    - Panel for the site map - Added conditions for hiding buttons with empty filters.
    - Admin Panel, section "Change Icon for markers" - Changed the map to a dark theme, for contrast.
    - Updated README.rst

- # 1.0 - 1.0.5
    - Added automatic styles correction for Firefox. - Fixed font size for headings and buttons.
    - Added automatic substitution of the version number in the help section.
    - Updated migration for optimization.

----

.. contents:: Contents
   :depth: 3
