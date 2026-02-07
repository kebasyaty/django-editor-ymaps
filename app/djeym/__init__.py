# :::::::-.      ....::::::.,::::::.-:.     ::-..        :
#  ;;,   `';, ;;;;;;;;;````;;;;'''' ';;.   ;;;;';;,.    ;;;
#  `[[     [[ ''`  `[[.     [[cccc    '[[,[[['  [[[[, ,[[[[,
#   $$,    $$,,,    `$$     $$""""      c$$"    $$$$$$$$"$$$
#   888_,o8P'888boood88     888oo,__  ,8P"`     888 Y88" 888o
#   MMMMP"`  "MMMMMMMM"     """"YUMMMmM"        MMM  M'  "MMM
#
# Django-Editor-YMaps - Plugin for creating and editing Yandex maps with Django framework.
# Copyright (c) 2014 Gennady Kostyunin
# SPDX-License-Identifier: MIT
"""Convenient use of the Yandex map service for web development on the popular and free Django framework."""

from __future__ import annotations

DjEYM_VERSION = (3, 0, 0)  # noqa: RUF067
PYTHON_VERSION = (3, 12)  # noqa: RUF067
DJANGO_VERSION = (5, 0, 0)  # noqa: RUF067
VUE_VERSION = (2, 7, 14)  # noqa: RUF067
VUETIFY_VERSION = (2, 2, 1)  # noqa: RUF067

__title__ = "DjEYM (django-editor-ymaps)"  # noqa: RUF067
__djeym_version__ = ".".join(map(str, DjEYM_VERSION))  # noqa: RUF067
__python_version__ = ".".join(map(str, PYTHON_VERSION))  # noqa: RUF067
__django_version__ = ".".join(map(str, DJANGO_VERSION))  # noqa: RUF067
__vue_version__ = ".".join(map(str, VUE_VERSION))  # noqa: RUF067
__vuetify_version__ = ".".join(map(str, VUETIFY_VERSION))  # noqa: RUF067
__author__ = "kebasyaty"
__license__ = "MIT"  # noqa: RUF067
__copyright__ = "Copyright (c) 2014 kebasyaty - Gennady Kostyunin"  # noqa: RUF067

default_app_config = "djeym.apps.DjeymConfig"  # noqa: RUF067
