# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class ColorPickerWidget(forms.widgets.TextInput):

    class Media:
        css = {
            'all': (
                '/static/djeym/plugins/really-simple-color-picker/css/colorPicker.min.css',
            )
        }
        js = (
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/plugins/really-simple-color-picker/js/jquery.colorPicker.min.js',
            '/static/djeym/js/admin_color_picker_widget.min.js'
        )

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        input_static = super(ColorPickerWidget, self).render(
            name, value, attrs)
        return mark_safe(input_static)


class CenterMapWidget(forms.Widget):

    class Media:
        js = (
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/admin_center_map_widget.min.js'
        )

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        text_hint = _("To determine the center of the map, move the marker or "
                      "click on the map in the right place.")
        html_hint = "<div class=\"hint_center_map\">{}</div>".format(text_hint)
        html_map = "<div id=\"id_center_map\"></div>"
        text_input_html = "{0}{1}".format(html_hint, html_map)
        return mark_safe(text_input_html)


class CheckIconOffsetWidget(forms.Widget):

    class Media:
        js = (
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/admin_check_icon_offset_widget.min.js'
        )

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        text_hint = _("Changing values along the axes X and Y, "
                      "match your marker with the standard:")
        img_hint = "<img src=\"/static/djeym/img/hint.svg\" class=\"hint_offset\" alt=\"hint\">"
        html_hint = "<div class=\"hint_check_icon_offset\">{0} {1}</div>"\
            .format(text_hint, img_hint)
        html_map = "<div id=\"id_check_icon_offset_map\"></div>"
        text_input_html = "{0}{1}".format(html_hint, html_map)
        return mark_safe(text_input_html)


class AdminFileThumbWidget(AdminFileWidget):
    template_name = "djeym/admin/widgets/clearable_file_input.html"
