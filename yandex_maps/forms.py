# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Map, Placemark, Polyline, Polygon
from .widgets import CenterMapWidget


class PlacemarkForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PlacemarkForm, self).__init__(*args, **kwargs)
        self.fields['map'].label = _('Map')
        self.fields['category'].label = _('Category')
        self.fields['icon_content'].label = _('Text on icon')
        self.fields['hint_content'].label = _('Hint content')
        self.fields['balloon_content'].label = _('Balloon content')
        self.fields['icon_name'].label = _('Icon name')
        self.fields['coordinates'].label = _('Coordinates')
        self.fields['subcategory'].label = _('Subcategory')

    class Meta:
        model = Placemark

        fields = ('map', 'category', 'subcategory', 'icon_content', 'hint_content', 'balloon_content',
                  'icon_name', 'color', 'coordinates')


class PolylineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PolylineForm, self).__init__(*args, **kwargs)
        self.fields['map'].label = _('Map')
        self.fields['category'].label = _('Category')
        self.fields['hint_content'].label = _('Hint content')
        self.fields['balloon_content'].label = _('Balloon content')
        self.fields['stroke_width'].label = _('Stroke width')
        self.fields['stroke_color'].label = _('Stroke color')
        self.fields['stroke_opacity'].label = _('Stroke opacity')
        self.fields['stroke_opacity'].initial = '1.0'
        self.fields['coordinates'].label = _('Coordinates')

    class Meta:
        model = Polyline

        fields = ('map', 'category', 'hint_content', 'balloon_content', 'stroke_width',
                  'stroke_color', 'stroke_opacity', 'coordinates')


class PolygonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PolygonForm, self).__init__(*args, **kwargs)
        self.fields['map'].label = _('Map')
        self.fields['category'].label = _('Category')
        self.fields['hint_content'].label = _('Hint content')
        self.fields['balloon_content'].label = _('Balloon content')
        self.fields['stroke_width'].label = _('Stroke width')
        self.fields['stroke_color'].label = _('Stroke color')
        self.fields['stroke_opacity'].label = _('Stroke opacity')
        self.fields['stroke_opacity'].initial = '1.0'
        self.fields['fill_color'].label = _('Fill color')
        self.fields['fill_opacity'].label = _('Fill opacity')
        self.fields['fill_opacity'].initial = '1.0'
        self.fields['coordinates'].label = _('Coordinates')

    class Meta:
        model = Polygon

        fields = ('map', 'category', 'hint_content', 'balloon_content', 'stroke_width',
                  'stroke_color', 'stroke_opacity', 'fill_color', 'fill_opacity', 'coordinates')


class CenterMapForm(forms.ModelForm):

    class Meta:
        model = Map
        fields = '__all__'

    center_map = forms.CharField(
        widget=CenterMapWidget,
        label=_('Center map'),
        required=False
    )
