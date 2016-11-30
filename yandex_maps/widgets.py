# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.safestring import mark_safe


class ColorPickerWidget(forms.widgets.TextInput):

    class Media:
        css = {
            'all': (
                '/static/yandex_maps/really-simple-color-picker/css/colorPicker.css',
            )
        }
        js = (
            '/static/yandex_maps/js/jquery-1.12.4.min.js',
            '/static/yandex_maps/really-simple-color-picker/js/jquery.colorPicker.min.js',
            '/static/yandex_maps/js/admin_color_picker_widget.js'
        )

    def render(self, name, value, attrs=None):
        input_static = super(ColorPickerWidget, self).render(name, value, attrs)
        return mark_safe(input_static)


class CenterMapWidget(forms.Widget):

    class Media:
        css = {
            'all': (
                '/static/yandex_maps/css/ymap_admin.css',
            )
        }
        js = (
            'https://api-maps.yandex.ru/2.1/?lang=ru_RU',
            '/static/yandex_maps/js/jquery-1.12.4.min.js',
            '/static/yandex_maps/js/admin_center_map_widget.js'
        )

    def render(self, name, value, attrs=None):
        text_input_html = '<div id="id_center_map"></div>'
        return mark_safe(text_input_html)
