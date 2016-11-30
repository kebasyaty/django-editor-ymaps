# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yandex_maps.models import Map, CustomIcon

from django import template
register = template.Library()


@register.inclusion_tag('yandex_maps/includes/ymap_include.html')
def load_ymap(slug='', width='auto', height='400px'):

    try:
        ymap = Map.objects.get(slug=slug, active=True)
        custom_icons = CustomIcon.objects.filter(active=True)
    except Map.DoesNotExist:
        ymap = custom_icons = None

    return {
        'ymap': ymap,
        'custom_icons': custom_icons,
        'width': width,
        'height': height
    }
