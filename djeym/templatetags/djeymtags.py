# -*- coding: utf-8 -*-

from django import template
from django.conf import settings

from ..models import Map
from ..views import vue_vendors_css_js

register = template.Library()


@register.inclusion_tag('djeym/includes/ymaps_front.html')
def djeym_yandex_map(slug, lang='en'):
    """Load the map to the front page."""

    ymap = Map.objects.filter(slug=slug, active=True).first()
    ctx = {'ymap': ymap}
    if ymap is not None:
        general_settings = ymap.general_settings
        ctx['lang'] = lang or 'en',
        ctx['load_indicator'] = ymap.load_indicator
        ctx['load_indicator_size'] = ymap.load_indicator_size
        ctx['is_heatmap'] = ymap.heatmap_settings.active
        ctx['is_round_theme'] = general_settings.roundtheme
        ctx['width_map_front'] = general_settings.width_map_front
        ctx['height_map_front'] = general_settings.height_map_front
        ctx['presets'] = ymap.presets.values_list('js', flat=True)
        vue_vendors = vue_vendors_css_js('front')
        ctx.update(vue_vendors)
    return ctx


@register.inclusion_tag('djeym/includes/api_ymaps.html')
def djeym_load_api_ymaps(lang='en', ns='djeymYMaps'):
    """Get URL for API Yandex Maps"""

    api_version = '2.1'
    api_key = getattr(settings, 'DJEYM_YMAPS_API_KEY', "")
    is_enterprise = getattr(
        settings, 'DJEYM_YMAPS_API_KEY_FOR_ENTERPRISE', False)
    mode = getattr(settings, 'DJEYM_YMAPS_DOWNLOAD_MODE', 'release')
    lang = lang[:2].lower() if bool(lang) else 'en'

    if lang == 'ru':
        lang += '_RU'
    elif lang == 'en':
        lang += '_US'
    elif lang == 'uk':
        lang += '_UA'
    elif lang == 'tr':
        lang += '_TR'
    else:
        lang = 'en_US'

    return {
        'api_key': api_key,
        'is_enterprise': is_enterprise,
        'api_version': api_version,
        'lang': lang,
        'mode': mode,
        'ns': ns
    }
