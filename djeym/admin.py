# -*- coding: utf-8 -*-
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.db import models

from .forms import CenterMapForm, OffsetCustomIconForm
from .models import (CategoryPlacemark, CategoryPolygon, CategoryPolyline,
                     CustomClusterIcon, CustomMarkerIcon, ExternalModules,
                     GeneralSettings, HeatmapSettings, HeatPoint,
                     IconCollection, LoadIndicator, Map, MapControls,
                     Placemark, Polygon, Polyline, Preset, Statistics,
                     SubCategoryPlacemark, TileSource)
from .utils import get_icon_font_plugin
from .widgets import AdminFileThumbWidget, ColorPickerWidget

DJEYM_YMAPS_ICONS_FOR_CATEGORIES = get_icon_font_plugin()


@admin.register(TileSource)
class TileSourceAdmin(admin.ModelAdmin):
    change_list_template = 'djeym/admin/tile_source_change_list.html'
    list_display = ('title', 'admin_thumbnail', 'maxzoom', 'minzoom', 'slug')
    list_display_links = ('title', 'admin_thumbnail')
    readonly_fields = ('slug',)

    formfield_overrides = {
        models.ImageField: {'widget': AdminFileThumbWidget()},
    }

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/import_export.min.js'
        ]


class MapControlsInline(admin.TabularInline):
    model = MapControls
    can_delete = False
    classes = ['collapse']


class ExternalModulesInline(admin.StackedInline):
    model = ExternalModules
    classes = ['collapse']
    can_delete = False


class GeneralSettingsInline(admin.StackedInline):
    model = GeneralSettings
    can_delete = False
    classes = ['collapse']
    exclude = ('cluster_icon_content_bg_color',
               'cluster_icon_content_txt_color')


"""
class HeatmapSettingsInline(admin.StackedInline):
    model = HeatmapSettings
    can_delete = False
"""


class PresetInline(admin.StackedInline):
    model = Preset
    extra = 0
    exclude = ('slug',)
    classes = ['collapse']


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('obj_type', 'obj_id', 'ip', 'timestamp')
    readonly_fields = ('likes',)

    class Media:
        css = {
            'all': ['/static/djeym/css/djeym_admin.min.css']
        }


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    form = CenterMapForm
    change_form_template = 'djeym/admin/center_map_change_form.html'
    list_display = ('title', 'get_status_heatmap', 'get_custom_cluster',
                    'get_custom_marker_icon', 'get_tile_screenshot', 'get_load_indicator',
                    'zoom', 'slug', 'active')
    list_display_links = ('title', 'get_custom_cluster', 'get_status_heatmap',
                          'get_custom_marker_icon', 'get_tile_screenshot',
                          'get_load_indicator')
    list_editable = ('active',)
    readonly_fields = ('slug',)
    inlines = (MapControlsInline, ExternalModulesInline,
               GeneralSettingsInline, PresetInline)

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/admin_view_icons.min.js',
        ]
        css['all'].extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[0])
        js.extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[1])


@admin.register(CategoryPlacemark)
class CategoryPlacemarkAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('get_title', 'get_category_icon', 'get_category_color',
                    'get_map_name', 'active')
    list_display_links = ('get_title', 'get_category_icon')
    list_editable = ('active',)
    list_filter = ('ymap',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        target_field_name = db_field.name
        if target_field_name == 'category_color' or target_field_name == 'cluster_color':
            kwargs['widget'] = ColorPickerWidget()
        return super(CategoryPlacemarkAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    formfield_overrides = {
        models.FileField: {'widget': AdminFileThumbWidget()},
    }

    class Media:
        css = {
            'all': ['/static/djeym/css/djeym_admin.min.css']
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/admin_view_icons.min.js',
        ]
        css['all'].extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[0])
        js.extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[1])


@admin.register(SubCategoryPlacemark)
class SubCategoryPlacemarkAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('get_title', 'get_category_icon', 'get_category_color',
                    'get_map_name', 'active')
    list_display_links = ('get_title', 'get_category_icon')
    list_editable = ('active',)
    list_filter = ('ymap',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'category_color':
            kwargs['widget'] = ColorPickerWidget()
        return super(SubCategoryPlacemarkAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    class Media:
        css = {
            'all': ['/static/djeym/css/djeym_admin.min.css']
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/admin_view_icons.min.js',
        ]
        css['all'].extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[0])
        js.extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[1])


@admin.register(CategoryPolyline)
class CategoryPolylineAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('get_title', 'get_category_icon', 'get_category_color',
                    'get_map_name', 'active')
    list_display_links = ('get_title', 'get_category_icon')
    list_editable = ('active',)
    list_filter = ('ymap',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'category_color':
            kwargs['widget'] = ColorPickerWidget()
        return super(CategoryPolylineAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    class Media:
        css = {
            'all': ['/static/djeym/css/djeym_admin.min.css']
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/admin_view_icons.min.js',
        ]
        css['all'].extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[0])
        js.extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[1])


@admin.register(CategoryPolygon)
class CategoryPolygonAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('get_title', 'get_category_icon', 'get_category_color',
                    'get_map_name', 'active')
    list_display_links = ('get_title', 'get_category_icon')
    list_editable = ('active',)
    list_filter = ('ymap',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'category_color':
            kwargs['widget'] = ColorPickerWidget()
        return super(CategoryPolygonAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    class Media:
        css = {
            'all': ['/static/djeym/css/djeym_admin.min.css']
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/admin_view_icons.min.js',
        ]
        css['all'].extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[0])
        js.extend(DJEYM_YMAPS_ICONS_FOR_CATEGORIES[1])


@admin.register(Placemark)
class PlacemarkAdmin(admin.ModelAdmin):
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('__str__', 'ymap', 'category', 'active')
    list_filter = ('ymap',)
    readonly_fields = ('coordinates', 'icon_name', 'json_code')
    list_editable = ('active',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget(config_name='djeym')},
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'marker_color':
            kwargs['widget'] = ColorPickerWidget()
        return super(PlacemarkAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = (
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/ckeditor_resize_image.min.js',
        )


@admin.register(Polyline)
class PolylineAdmin(admin.ModelAdmin):
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('__str__', 'active')
    list_filter = ('ymap',)
    readonly_fields = ('coordinates', 'json_code')
    list_editable = ('active',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget(config_name='djeym')},
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'stroke_color':
            kwargs['widget'] = ColorPickerWidget()
        return super(PolylineAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = (
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/ckeditor_resize_image.min.js',
        )


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('__str__', 'active')
    list_filter = ('ymap',)
    readonly_fields = ('coordinates', 'json_code')
    list_editable = ('active',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget(config_name='djeym')},
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'stroke_color' or db_field.name == 'fill_color':
            kwargs['widget'] = ColorPickerWidget()
        return super(PolygonAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = (
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/ckeditor_resize_image.min.js',
        )


@admin.register(HeatPoint)
class HeatPointAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('title', 'weight', 'slug', 'active')
    list_editable = ('active',)
    list_filter = ('ymap',)
    readonly_fields = ('coordinates', 'slug', 'json_code')
    search_fields = ('title',)

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }


@admin.register(CustomClusterIcon)
class CustomClusterIconAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('title', 'admin_thumbnail')
    list_display_links = ('title', 'admin_thumbnail')
    readonly_fields = ('size_width', 'size_height', 'offset_x', 'offset_y')

    formfield_overrides = {
        models.FileField: {'widget': AdminFileThumbWidget()},
    }

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/get_icon_name.min.js'
        ]


@admin.register(IconCollection)
class IconCollectionAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    change_list_template = 'djeym/admin/icon_collection_change_list.html'
    list_display = ('title', 'admin_thumbnail', 'get_export_file_btn',
                    'get_icon_count', 'get_count_of_active_icons')
    list_display_links = ('title', 'admin_thumbnail')
    readonly_fields = ('slug',)

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/import_export.min.js'
        ]


@admin.register(CustomMarkerIcon)
class CustomMarkerIconAdmin(admin.ModelAdmin):
    form = OffsetCustomIconForm
    change_form_template = 'djeym/admin/check_icon_offset_change_form.html'
    list_display = ('title', 'admin_thumbnail', 'get_collection_name',
                    'active', 'slug')
    list_display_links = ('title', 'admin_thumbnail')
    readonly_fields = ('size_width', 'size_height', 'slug')
    list_editable = ('active',)
    list_filter = ('icon_collection',)

    formfield_overrides = {
        models.FileField: {'widget': AdminFileThumbWidget()},
    }

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/plugins/jquery_mousewheel/jquery.mousewheel.min.js',
            '/static/djeym/js/get_icon_name.min.js'
        ]


@admin.register(LoadIndicator)
class LoadIndicatorAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'

    list_display = ('title', 'admin_thumbnail', 'slug')
    list_display_links = ('title', 'admin_thumbnail')
    readonly_fields = ('slug',)

    formfield_overrides = {
        models.FileField: {'widget': AdminFileThumbWidget()},
    }

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = [
            '/static/djeym/js/jquery-3.3.1.min.js',
            '/static/djeym/js/get_icon_name.min.js'
        ]
