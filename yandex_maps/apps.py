# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig


class YandexMapsConfig(AppConfig):
    name = 'yandex_maps'
    verbose_name = _('Yandex maps')
