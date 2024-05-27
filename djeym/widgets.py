# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class CenterMapWidget(forms.Widget):

    class Media:
        js = (
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/admin_center_map_widget.min.js'
        )

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        html_map = "<div id=\"id_center_map\"></div>"
        return mark_safe(html_map)


class CheckIconOffsetWidget(forms.Widget):

    class Media:
        js = (
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/admin_check_icon_offset_widget.min.js'
        )

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        html_map = "<div id=\"id_check_icon_offset_map\"></div>"
        return mark_safe(html_map)


class AdminFileThumbWidget(AdminFileWidget):
    template_name = "djeym/admin/widgets/clearable_file_input.html"
