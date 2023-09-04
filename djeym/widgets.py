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
        text_hint = _(
            "Move the marker or click on the map in the right place.")
        html_hint = "<div class=\"hint_center_map\">{}</div>".format(text_hint)
        html_map = "<div id=\"id_center_map\"></div>"
        text_input_html = "{0}{1}".format(html_hint, html_map)
        return mark_safe(text_input_html)


class CheckIconOffsetWidget(forms.Widget):

    class Media:
        js = (
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/admin_check_icon_offset_widget.min.js'
        )

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        text_hint = _("Changing values along the axes X and Y, "
                      "match your marker with the standard")
        img_hint = "<img src=\"/static/djeym/img/hint.svg\" class=\"hint_offset\" alt=\"hint\">"
        html_hint = "<div class=\"hint_check_icon_offset\">{0} {1}</div>"\
            .format(text_hint, img_hint)
        html_map = "<div id=\"id_check_icon_offset_map\"></div>"
        text_input_html = "{0}{1}".format(html_hint, html_map)
        return mark_safe(text_input_html)


class AdminFileThumbWidget(AdminFileWidget):
    template_name = "djeym/admin/widgets/clearable_file_input.html"
