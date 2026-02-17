"""Forms."""

from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import (
    BannedIP,
    GeneralSettings,
    HeatmapSettings,
    HeatPoint,
    Map,
    MapControls,
    MarkerIcon,
    Placemark,
    Polygon,
    Polyline,
    Preset,
)
from .widgets import CenterMapWidget, CheckIconOffsetWidget


class GeneralSettingsForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = GeneralSettings
        fields = (
            "ymap",
            "clustering_edit",
            "clustering_site",
            "cluster_layout",
            "cluster_icon_content",
            "cluster_icon_content_bg_color",
            "cluster_icon_content_txt_color",
            "controls_color",
            "buttons_text_color",
            "theme_type",
            "roundtheme",
            "panorama",
            "width_panel_editor",
            "width_panel_front",
            "open_panel_front",
            "img_bg_panel_front",
            "tinting_panel_front",
            "hide_group_name_panel_front",
            "width_map_front",
            "height_map_front",
        )


class PresetForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = Preset
        fields = (
            "ymap",
            "autoheader",
            "autofooter",
            "placemark",
            "polyline",
            "polygon",
            "position",
        )


class HeatPointForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = HeatPoint
        fields = ("ymap", "title", "weight", "coordinates")


class HeatmapSettingsForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = HeatmapSettings
        fields = (
            "ymap",
            "radius",
            "dissipating",
            "opacity",
            "intensity",
            "gradient_color1",
            "gradient_color2",
            "gradient_color3",
            "gradient_color4",
            "active",
        )


class MapControlsForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = MapControls
        fields = (
            "ymap",
            "geolocation",
            "search",
            "provider",
            "route",
            "traffic",
            "typeselector",
            "fullscreen",
            "zoom",
            "ruler",
        )


class PlacemarkForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = Placemark
        fields = (
            "ymap",
            "category",
            "subcategories",
            "header",
            "image",
            "footer",
            "icon_slug",
            "coordinates",
        )


class CustomPlacemarkForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = Placemark
        fields = (
            "ymap",
            "category",
            "subcategories",
            "header",
            "image",
            "footer",
            "icon_slug",
            "coordinates",
            "user_email",
            "active",
            "is_user_geotag",
        )


class PolylineForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = Polyline
        fields = (
            "ymap",
            "category",
            "subcategories",
            "header",
            "image",
            "footer",
            "stroke_width",
            "stroke_color",
            "stroke_style",
            "stroke_opacity",
            "coordinates",
        )


class PolygonForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = Polygon
        fields = (
            "ymap",
            "category",
            "subcategories",
            "header",
            "image",
            "footer",
            "stroke_width",
            "stroke_color",
            "stroke_opacity",
            "fill_color",
            "stroke_style",
            "fill_opacity",
            "coordinates",
        )


class BanIPForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = BannedIP
        fields = ("ip",)


class CenterMapForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = Map
        fields = "__all__"

    center_map = forms.CharField(widget=CenterMapWidget, label=_("Center map"), required=False)


class OffsetMarkerIconForm(forms.ModelForm):
    class Meta:  # noqa: D106
        model = MarkerIcon
        fields = "__all__"

    check_icon_offset = forms.CharField(widget=CheckIconOffsetWidget, label=_("Check icon offset"), required=False)
