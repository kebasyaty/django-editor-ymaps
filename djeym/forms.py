# -*- coding: utf-8 -*-
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import (CustomMarkerIcon, GeneralSettings, HeatmapSettings,
                     HeatPoint, Map, MapControls, Placemark, Polygon, Polyline,
                     Preset)
from .widgets import CenterMapWidget, CheckIconOffsetWidget


class GeneralSettingsForm(forms.ModelForm):

    class Meta:
        model = GeneralSettings
        fields = ('ymap', 'clustering_edit', 'clustering_site',
                  'cluster_layout', 'cluster_icon_content',
                  'cluster_icon_content_bg_color', 'cluster_icon_content_txt_color')


class PresetForm(forms.ModelForm):

    class Meta:
        model = Preset
        fields = ('ymap', 'autoheader', 'autobody', 'autofooter',
                  'placemark', 'polyline', 'polygon', 'position')


class HeatPointForm(forms.ModelForm):

    class Meta:
        model = HeatPoint
        fields = ('ymap', 'title', 'weight', 'coordinates')


class HeatmapSettingsForm(forms.ModelForm):

    class Meta:
        model = HeatmapSettings
        fields = ('ymap', 'radius', 'dissipating', 'opacity', 'intensity',
                  'gradient_color1', 'gradient_color2', 'gradient_color3',
                  'gradient_color4')

        widgets = {
            'ymap': forms.HiddenInput(attrs={'id': 'id_djeym_heatmap_ymap'}),
            'radius': forms.NumberInput(attrs={'id': 'id_djeym_heatmap_radius'}),
            'dissipating': forms.CheckboxInput(attrs={'id': 'id_djeym_heatmap_dissipating'}),
            'opacity': forms.TextInput(attrs={'id': 'id_djeym_heatmap_opacity'}),
            'intensity': forms.TextInput(attrs={'id': 'id_djeym_heatmap_intensity'}),
            'gradient_color1': forms.TextInput(
                attrs={'id': 'id_djeym_heatmap_gradient_color1',
                       'class': 'djeym_heatmap_gradient_color'}),
            'gradient_color2': forms.TextInput(
                attrs={'id': 'id_djeym_heatmap_gradient_color2',
                       'class': 'djeym_heatmap_gradient_color'}),
            'gradient_color3': forms.TextInput(
                attrs={'id': 'id_djeym_heatmap_gradient_color3',
                       'class': 'djeym_heatmap_gradient_color'}),
            'gradient_color4': forms.TextInput(
                attrs={'id': 'id_djeym_heatmap_gradient_color4',
                       'class': 'djeym_heatmap_gradient_color'})
        }


class MapControlsForm(forms.ModelForm):

    class Meta:
        model = MapControls
        fields = ('ymap', 'geolocation', 'search', 'provider',
                  'route', 'traffic', 'typeselector', 'fullscreen',
                  'zoom', 'ruler', 'maptype')

        widgets = {
            'ymap': forms.HiddenInput(attrs={'id': 'id_djeym_controls_ymap'}),
            'geolocation': forms.CheckboxInput(attrs={'id': 'id_djeym_controls_geolocation'}),
            'search': forms.CheckboxInput(attrs={'id': 'id_djeym_controls_search'}),
            'provider': forms.CheckboxInput(attrs={'id': 'id_djeym_controls_provider'}),
            'route': forms.CheckboxInput(attrs={'id': 'id_djeym_controls_route'}),
            'traffic': forms.CheckboxInput(attrs={'id': 'id_djeym_controls_traffic'}),
            'typeselector': forms.CheckboxInput(attrs={'id': 'id_djeym_controls_typeselector'}),
            'fullscreen': forms.CheckboxInput(attrs={'id': 'id_djeym_controls_fullscreen'}),
            'zoom': forms.CheckboxInput(attrs={'id': 'id_djeym_controls_zoom'}),
            'ruler': forms.CheckboxInput(attrs={'id': 'id_djeym_controls_ruler'}),
        }


class PlacemarkForm(forms.ModelForm):

    class Meta:
        model = Placemark
        fields = ('ymap', 'category', 'subcategories', 'header',
                  'body', 'footer', 'icon_name', 'coordinates')


class PolylineForm(forms.ModelForm):

    class Meta:
        model = Polyline
        fields = ('ymap', 'category', 'header', 'body', 'footer',
                  'stroke_width', 'stroke_color', 'stroke_opacity', 'coordinates')

        widgets = {
            'stroke_opacity': forms.TextInput()
        }


class PolygonForm(forms.ModelForm):

    class Meta:
        model = Polygon
        fields = ('ymap', 'category', 'header', 'body', 'footer',
                  'stroke_width', 'stroke_color', 'stroke_opacity', 'fill_color',
                  'fill_opacity', 'coordinates')

        widgets = {
            'stroke_opacity': forms.TextInput(),
            'fill_opacity': forms.TextInput(),
        }


class GeoObjectsTransferForm(forms.Form):

    def __init__(self, ymap_id, *args, **kwargs):
        super(GeoObjectsTransferForm, self).__init__(*args, **kwargs)
        self.fields['ymap'].initial = ymap_id

    ymap = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    category = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    subcategories = forms.CharField(
        widget=forms.SelectMultiple(),
        required=False
    )
    header = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )
    body = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )
    footer = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )
    icon_name = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    coordinates = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )
    stroke_width = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    stroke_color = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    stroke_opacity = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    fill_color = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    fill_opacity = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    pk = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    geo_type = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    action = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )

    title = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )

    weight = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )


class CenterMapForm(forms.ModelForm):

    class Meta:
        model = Map
        fields = '__all__'

    center_map = forms.CharField(
        widget=CenterMapWidget,
        label=_('Center map'),
        required=False
    )


class OffsetCustomIconForm(forms.ModelForm):

    class Meta:
        model = CustomMarkerIcon
        fields = '__all__'

    check_icon_offset = forms.CharField(
        widget=CheckIconOffsetWidget,
        label=_('Check icon offset'),
        required=False
    )


class CKEditorTextareaForm(forms.Form):

    ckeditor_textarea = forms.CharField(
        widget=CKEditorUploadingWidget(config_name='djeym'),
    )
