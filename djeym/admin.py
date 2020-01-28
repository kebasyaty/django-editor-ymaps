# -*- coding: utf-8 -*-
from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline
from django.contrib import admin
from django.db import models

from .forms import CenterMapForm, OffsetMarkerIconForm
from .models import (BlockedIP, CategoryPlacemark, CategoryPolygon,
                     CategoryPolyline, ClusterIcon, HeatPoint, IconCollection,
                     LoadIndicator, Map, MarkerIcon, Placemark, Polygon,
                     Polyline, Preset, Statistics, SubCategoryPlacemark,
                     SubCategoryPolygon, SubCategoryPolyline, TileSource)
from .widgets import AdminFileThumbWidget


@admin.register(TileSource)
class TileSourceAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
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
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/import_export.min.js'
        ]


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


@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('ip', 'timestamp')

    class Media:
        css = {
            'all': ['/static/djeym/css/djeym_admin.min.css']
        }


class PresetInline(admin.StackedInline):
    model = Preset
    extra = 0
    exclude = ('slug',)
    classes = ['collapse']


class CategoryPlacemarkInline(SortableTabularInline):
    model = CategoryPlacemark
    extra = 0
    classes = ['collapse']


class SubCategoryPlacemarkInline(SortableTabularInline):
    model = SubCategoryPlacemark
    extra = 0
    classes = ['collapse']


class CategoryPolylineInline(SortableTabularInline):
    model = CategoryPolyline
    extra = 0
    classes = ['collapse']


class SubCategoryPolylineInline(SortableTabularInline):
    model = SubCategoryPolyline
    extra = 0
    classes = ['collapse']


class CategoryPolygonInline(SortableTabularInline):
    model = CategoryPolygon
    extra = 0
    classes = ['collapse']


class SubCategoryPolygonInline(SortableTabularInline):
    model = SubCategoryPolygon
    extra = 0
    classes = ['collapse']


@admin.register(Map)
class MapAdmin(NonSortableParentAdmin):
    form = CenterMapForm
    change_form_template_extends = 'djeym/admin/center_map_change_form.html'
    list_display = ('title', 'slug', 'get_cluster', 'get_icon_collection',
                    'get_tile_screenshot', 'get_load_indicator', 'get_status_heatmap',
                    'zoom', 'active')
    list_display_links = ('title', 'get_cluster', 'get_status_heatmap',
                          'get_icon_collection', 'get_tile_screenshot', 'get_load_indicator')
    list_editable = ('active',)
    inlines = (PresetInline, CategoryPlacemarkInline, SubCategoryPlacemarkInline,
               CategoryPolylineInline, SubCategoryPolylineInline, CategoryPolygonInline,
               SubCategoryPolygonInline)

    class Media:
        css = {
            'all': ['/static/djeym/css/djeym_admin.min.css']
        }

        js = [
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/admin_view_icons.min.js'
        ]


@admin.register(Placemark)
class PlacemarkAdmin(admin.ModelAdmin):
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('__str__', 'ymap', 'category', 'active')
    list_filter = ('ymap',)
    list_editable = ('active',)
    filter_horizontal = ('subcategories',)

    formfield_overrides = {
        models.ImageField: {'widget': AdminFileThumbWidget()},
    }

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = (
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/ckeditor_resize_image.min.js',
            '/static/djeym/js/admin_icon_collection.min.js',
            '/static/djeym/js/admin_block_ip.min.js'
        )


@admin.register(Polyline)
class PolylineAdmin(admin.ModelAdmin):
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('__str__', 'active')
    list_filter = ('ymap',)
    list_editable = ('active',)
    filter_horizontal = ('subcategories',)

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = (
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/ckeditor_resize_image.min.js',
        )


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('__str__', 'active')
    list_filter = ('ymap',)
    list_editable = ('active',)
    filter_horizontal = ('subcategories',)

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }

        js = (
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/ckeditor_resize_image.min.js',
        )


@admin.register(HeatPoint)
class HeatPointAdmin(admin.ModelAdmin):
    # ckeditor_change_form.html - Used by default.
    change_form_template = 'djeym/admin/ckeditor_change_form.html'
    list_display = ('title', 'weight', 'slug', 'active')
    list_editable = ('active',)
    list_filter = ('ymap',)
    readonly_fields = ('slug',)
    search_fields = ('title',)

    class Media:
        css = {
            'all': [
                '/static/djeym/css/djeym_admin.min.css',
            ]
        }


@admin.register(ClusterIcon)
class ClusterIconAdmin(admin.ModelAdmin):
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
            '/static/djeym/js/jquery.min.js',
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
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/import_export.min.js'
        ]


@admin.register(MarkerIcon)
class MarkerIconAdmin(admin.ModelAdmin):
    form = OffsetMarkerIconForm
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
            '/static/djeym/js/jquery.min.js',
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
            '/static/djeym/js/jquery.min.js',
            '/static/djeym/js/get_icon_name.min.js'
        ]
