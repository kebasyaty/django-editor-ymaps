# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (Map, CategoryPlacemark, CategoryPolyline, CategoryPolygon,
                     SubCategoryPlacemark, Placemark, Polyline, Polygon, CustomIcon)

from .forms import CenterMapForm
from .widgets import ColorPickerWidget


@admin.register(SubCategoryPlacemark)
class SubCategoryPlacemarkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'map', 'active')
    list_editable = ('active',)
    list_filter = ('map',)


@admin.register(CategoryPlacemark)
class CategoryPlacemarkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'map', 'active')
    list_editable = ('active',)
    list_filter = ('map',)


@admin.register(CategoryPolyline)
class CategoryPolylineAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'map', 'active')
    list_editable = ('active',)


@admin.register(CategoryPolygon)
class CategoryPolygonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'map', 'active')
    list_editable = ('active',)


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    form = CenterMapForm
    change_form_template = 'yandex_maps/admin/change_form.html'
    list_display = ('title', 'zoom', 'slug', 'active')
    list_editable = ('zoom', 'active')
    readonly_fields = ('slug', 'icon')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'color':
            kwargs['widget'] = ColorPickerWidget()
        return super(MapAdmin, self).formfield_for_dbfield(db_field, **kwargs)


@admin.register(Placemark)
class PlacemarkAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'map', 'category', 'get_subcategory', 'active')
        list_filter = ('map', 'category')
        readonly_fields = ('coordinates', 'icon_name')
        list_editable = ('active',)

        def formfield_for_dbfield(self, db_field, **kwargs):
            if db_field.name == 'color':
                kwargs['widget'] = ColorPickerWidget()
            return super(PlacemarkAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        class Media:
            js = (
                '/static/yandex_maps/js/jquery-1.12.4.min.js',
                '/tinymce/filebrowser/',
                'yandex_maps/tiny_mce/jquery.tinymce.js',
                'yandex_maps/tiny_mce/tiny_mce.js',
                '/static/yandex_maps/tiny_mce/init_tinymce.js'
            )


@admin.register(Polyline)
class PolylineAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'active')
        list_filter = ('map',)
        readonly_fields = ('coordinates',)
        list_editable = ('active',)

        def formfield_for_dbfield(self, db_field, **kwargs):
            if db_field.name == 'stroke_color':
                kwargs['widget'] = ColorPickerWidget()
            return super(PolylineAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        class Media:
            js = (
                '/static/yandex_maps/js/jquery-1.12.4.min.js',
                '/tinymce/filebrowser/',
                'yandex_maps/tiny_mce/jquery.tinymce.js',
                'yandex_maps/tiny_mce/tiny_mce.js',
                '/static/yandex_maps/tiny_mce/init_tinymce.js'
            )


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'active')
        list_filter = ('map',)
        readonly_fields = ('coordinates',)
        list_editable = ('active',)

        def formfield_for_dbfield(self, db_field, **kwargs):
            if db_field.name == 'stroke_color' or db_field.name == 'fill_color':
                kwargs['widget'] = ColorPickerWidget()
            return super(PolygonAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        class Media:
            js = (
                '/static/yandex_maps/js/jquery-1.12.4.min.js',
                '/tinymce/filebrowser/',
                'yandex_maps/tiny_mce/jquery.tinymce.js',
                'yandex_maps/tiny_mce/tiny_mce.js',
                '/static/yandex_maps/tiny_mce/init_tinymce.js'
            )


@admin.register(CustomIcon)
class CustomIconAdmin(admin.ModelAdmin):
        list_display = ('title', 'admin_thumbnail', 'active')
        list_display_links = ('title', 'admin_thumbnail')
        readonly_fields = ('slug',)
        list_editable = ('active',)
