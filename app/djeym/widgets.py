"""Widgets."""

from __future__ import annotations

from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe


class CenterMapWidget(forms.Widget):
    class Media:  # noqa: D106
        js = ("/static/djeym/js/jquery.min.js", "/static/djeym/js/center_map_widget.js")

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        html_map = '<div id="id_center_map"></div>'
        return mark_safe(html_map)  # noqa: S308


class CheckIconOffsetWidget(forms.Widget):
    class Media:  # noqa: D106
        js = ("/static/djeym/js/jquery.min.js", "/static/djeym/js/check_icon_offset_widget.js")

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        html_map = '<div id="id_check_icon_offset_map"></div>'
        return mark_safe(html_map)  # noqa: S308


class AdminFileThumbWidget(AdminFileWidget):
    template_name = "djeym/admin/widgets/clearable_file_input.html"
