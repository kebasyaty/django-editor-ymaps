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
"""Main URLs."""

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djeym/", include("djeym.urls", namespace="djeym")),
]

if settings.DEBUG:
    (
        urlpatterns
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
```

- **Add media directory to your project:** `media/uploads`.

- **Update Migrations:**

```shell
cd project-name
python manage.py migrate djeym
# or
uv run python app_name/manage.py migrate app_name/djeym
```

<br>

[![Changelog](https://raw.githubusercontent.com/kebasyaty/django-editor-ymaps/v3/assets/links/changelog.svg "Changelog")](https://github.com/kebasyaty/django-editor-ymaps/blob/v3/CHANGELOG.md "Changelog")

[![MIT](https://raw.githubusercontent.com/kebasyaty/django-editor-ymaps/v3/assets/links/mit.svg "MIT")](https://github.com/kebasyaty/django-editor-ymaps/blob/main/LICENSE "MIT")
