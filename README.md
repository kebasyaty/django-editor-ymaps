<div align="center">
  <p align="center">
    <a href="https://github.com/kebasyaty/django-editor-ymaps">
      <img
        height="80"
        alt="Logo"
        src="https://raw.githubusercontent.com/kebasyaty/django-editor-ymaps/v3/assets/logo.svg">
    </a>
  </p>
  <p>
    <h1>django-editor-ymaps</h1>
    <h3>Plugin for creating and editing Yandex maps with Django framework.</h3>
    <p align="center">
      <a href="https://github.com/kebasyaty/django-editor-ymaps/actions/workflows/test.yml" alt="Build Status"><img src="https://github.com/kebasyaty/django-editor-ymaps/actions/workflows/test.yml/badge.svg" alt="Build Status"></a>
      <a href="https://kebasyaty.github.io/django-editor-ymaps/" alt="Docs"><img src="https://img.shields.io/badge/docs-available-brightgreen.svg" alt="Docs"></a>
      <a href="https://pypi.python.org/pypi/django-editor-ymaps/" alt="PyPI pyversions"><img src="https://img.shields.io/pypi/pyversions/django-editor-ymaps.svg" alt="PyPI pyversions"></a>
      <a href="https://pypi.python.org/pypi/django-editor-ymaps/" alt="PyPI status"><img src="https://img.shields.io/pypi/status/django-editor-ymaps.svg" alt="PyPI status"></a>
      <a href="https://pypi.python.org/pypi/django-editor-ymaps/" alt="PyPI version fury.io"><img src="https://badge.fury.io/py/django-editor-ymaps.svg" alt="PyPI version fury.io"></a>
      <br>
      <a href="https://pyrefly.org/" alt="Types: Pyrefly"><img src="https://img.shields.io/badge/types-Pyrefly-FFB74D.svg" alt="Types: Pyrefly"></a>
      <a href="https://docs.astral.sh/ruff/" alt="Code style: Ruff"><img src="https://img.shields.io/badge/code%20style-Ruff-FDD835.svg" alt="Code style: Ruff"></a>
      <a href="https://pypi.org/project/django-editor-ymaps"><img src="https://img.shields.io/pypi/format/django-editor-ymaps" alt="Format"></a>
      <a href="https://pepy.tech/projects/django-editor-ymaps"><img src="https://static.pepy.tech/badge/django-editor-ymaps" alt="PyPI Downloads"></a>
      <a href="https://github.com/kebasyaty/django-editor-ymaps/blob/main/LICENSE" alt="GitHub license"><img src="https://img.shields.io/github/license/kebasyaty/django-editor-ymaps" alt="GitHub license"></a>
    </p>
    <p align="center">
      Convenient use of the Yandex map service for web development on the popular and free Django framework.
    </p>
  </p>
</div>

##

<img src="https://raw.githubusercontent.com/kebasyaty/django-editor-ymaps/v3/assets/attention.svg" alt="Attention">
<p>Some text ...</a>

<br>
<br>

[![Documentation](https://raw.githubusercontent.com/kebasyaty/django-editor-ymaps/v3/assets/links/documentation.svg "Documentation")](https://kebasyaty.github.io/django-editor-ymaps/ "Documentation")

[![Requirements](https://raw.githubusercontent.com/kebasyaty/django-editor-ymaps/v3/assets/links/requirements.svg "Requirements")](https://github.com/kebasyaty/django-editor-ymaps/blob/v3/REQUIREMENTS.md "Requirements")

## Terms of use for the API

[Terms of use for the Yandex.Maps](https://yandex.ru/dev/commercial/doc/en/ "Terms of use for the Yandex.Maps")

[Get the API key](https://yandex.com/dev/jsapi-v2-1/doc/en/#get-api-key "Get the API key")

## Installation

```shell
# Install gettext:
# https://docs.python.org/3/library/gettext.html
# Ubuntu
sudo apt install gettext
# Fedora
sudo dnf install gettext
# MacOS
brew install gettext
brew link gettext --force
# Windows
# https://mlocati.github.io/articles/gettext-iconv-windows.html
run: gettext0.25-iconv1.17-shared-64.exe

# Install django-editor-ymaps:
cd project-name
pip install django-editor-ymaps
# or
uv add django-editor-ymaps
```

## Usage

[![Examples](https://raw.githubusercontent.com/kebasyaty/django-editor-ymaps/v3/assets/links/examples.svg "Examples")](https://kebasyaty.github.io/django-editor-ymaps/latest/pages/usage/ "Examples")

- **Add to Settings**

```python
"""Settings."""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    ...
    "imagekit",
    "ckeditor",
    "ckeditor_uploader",
    "colorful",
    "adminsortable",
    "djeym",
    ...
]

MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',
    'djeym.middleware.AjaxMiddleware',
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

# Map download mode.
# Default = 'release'
# DJEYM_YMAPS_DOWNLOAD_MODE = 'debug' if DEBUG else 'release'
```

- **Add to main URLs**

```python
"""???"""

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
```

<br>

[![Changelog](https://raw.githubusercontent.com/kebasyaty/django-editor-ymaps/v3/assets/links/changelog.svg "Changelog")](https://github.com/kebasyaty/django-editor-ymaps/blob/v3/CHANGELOG.md "Changelog")

[![MIT](https://raw.githubusercontent.com/kebasyaty/django-editor-ymaps/v3/assets/links/mit.svg "MIT")](https://github.com/kebasyaty/django-editor-ymaps/blob/main/LICENSE "MIT")
