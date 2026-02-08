"""Admin."""

from __future__ import annotations

from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline
from django.contrib import admin
from django.db import models

from .forms import CenterMapForm, OffsetMarkerIconForm
from .models import (
    BlockedIP,
    CategoryPlacemark,
    CategoryPolygon,
    CategoryPolyline,
    ClusterIcon,
    HeatPoint,
    IconCollection,
    LoadIndicator,
    Map,
    MarkerIcon,
    Placemark,
    Polygon,
    Polyline,
    Preset,
    Statistics,
    Status,
    SubCategoryPlacemark,
    SubCategoryPolygon,
    SubCategoryPolyline,
    TileSource,
)
from .widgets import AdminFileThumbWidget


@admin.register(TileSource)
class TileSourceAdmin(admin.ModelAdmin):  # noqa: D101
    # ckeditor_change_form.html - Used by default.
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    change_list_template = "djeym/admin/tile_source_change_list.html"
    list_display = ("title", "admin_thumbnail", "maxzoom", "minzoom", "slug")  # pyrefly: ignore[bad-override]
    list_display_links = ("title", "admin_thumbnail")  # pyrefly: ignore[bad-override]
    readonly_fields = ("slug",)  # pyrefly: ignore[bad-override]

    formfield_overrides = {  # noqa: RUF012
        models.ImageField: {"widget": AdminFileThumbWidget()},
    }

    class Media:  # noqa: D106
        css = {  # noqa: RUF012
            "all": [
                "/static/djeym/css/djeym_admin.css",
            ],
        }

        js = (
            "/static/djeym/js/jquery.min.js",
            "/static/djeym/js/import_export.js",
        )


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):  # noqa: D101
    # ckeditor_change_form.html - Used by default.
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    list_display = ("obj_type", "obj_id", "ip", "timestamp")  # pyrefly: ignore[bad-override]
    readonly_fields = ("likes",)  # pyrefly: ignore[bad-override]

    class Media:  # noqa: D106
        css = {"all": ["/static/djeym/css/djeym_admin.css"]}  # noqa: RUF012


@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):  # noqa: D101
    # ckeditor_change_form.html - Used by default.
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    list_display = ("ip", "timestamp")  # pyrefly: ignore[bad-override]

    class Media:  # noqa: D106
        css = {"all": ["/static/djeym/css/djeym_admin.css"]}  # noqa: RUF012


class PresetInline(admin.StackedInline):  # noqa: D101
    model = Preset
    extra = 0
    exclude = ("slug",)
    classes = ["collapse"]  # noqa: RUF012


class CategoryPlacemarkInline(SortableTabularInline):  # noqa: D101
    model = CategoryPlacemark
    extra = 0
    classes = ["collapse"]  # noqa: RUF012


class SubCategoryPlacemarkInline(SortableTabularInline):  # noqa: D101
    model = SubCategoryPlacemark
    extra = 0
    classes = ["collapse"]  # noqa: RUF012


class CategoryPolylineInline(SortableTabularInline):  # noqa: D101
    model = CategoryPolyline
    extra = 0
    classes = ["collapse"]  # noqa: RUF012


class SubCategoryPolylineInline(SortableTabularInline):  # noqa: D101
    model = SubCategoryPolyline
    extra = 0
    classes = ["collapse"]  # noqa: RUF012


class CategoryPolygonInline(SortableTabularInline):  # noqa: D101
    model = CategoryPolygon
    extra = 0
    classes = ["collapse"]  # noqa: RUF012


class SubCategoryPolygonInline(SortableTabularInline):  # noqa: D101
    model = SubCategoryPolygon
    extra = 0
    classes = ["collapse"]  # noqa: RUF012


@admin.register(Map)
class MapAdmin(NonSortableParentAdmin):  # noqa: D101
    form = CenterMapForm
    change_form_template_extends = "djeym/admin/center_map_change_form.html"
    list_display = (  # pyrefly: ignore[bad-override]
        "title",
        "slug",
        "get_cluster",
        "get_icon_collection",
        "get_tile_screenshot",
        "get_load_indicator",
        "get_status_heatmap",
        "zoom",
        "active",
    )
    list_display_links = (  # pyrefly: ignore[bad-override]
        "title",
        "get_cluster",
        "get_status_heatmap",
        "get_icon_collection",
        "get_tile_screenshot",
        "get_load_indicator",
    )
    list_editable = ("active",)  # pyrefly: ignore[bad-override]
    inlines = (  # pyrefly: ignore[bad-override]
        PresetInline,
        CategoryPlacemarkInline,
        SubCategoryPlacemarkInline,
        CategoryPolylineInline,
        SubCategoryPolylineInline,
        CategoryPolygonInline,
        SubCategoryPolygonInline,
    )

    class Media:  # noqa: D106
        css = {"all": ["/static/djeym/css/djeym_admin.css"]}  # noqa: RUF012

        js = (
            "/static/djeym/js/jquery.min.js",
            "/static/djeym/js/admin_view_icons.js",
        )


@admin.register(Placemark)
class PlacemarkAdmin(admin.ModelAdmin):  # noqa: D101
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    list_display = ("__str__", "ymap", "category", "active")  # pyrefly: ignore[bad-override]
    list_filter = ("ymap",)  # pyrefly: ignore[bad-override]
    list_editable = ("active",)  # pyrefly: ignore[bad-override]
    filter_horizontal = ("subcategories",)  # pyrefly: ignore[bad-override]

    formfield_overrides = {  # noqa: RUF012
        models.ImageField: {"widget": AdminFileThumbWidget()},
    }

    class Media:  # noqa: D106
        css = {  # noqa: RUF012
            "all": [
                "/static/djeym/css/djeym_admin.css",
            ],
        }

        js = (
            "/static/djeym/js/jquery.min.js",
            "/static/djeym/js/ckeditor_resize_image.js",
            "/static/djeym/js/admin_icon_collection.js",
            "/static/djeym/js/admin_block_ip.js",
        )


@admin.register(Polyline)
class PolylineAdmin(admin.ModelAdmin):  # noqa: D101
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    list_display = ("__str__", "active")  # pyrefly: ignore[bad-override]
    list_filter = ("ymap",)  # pyrefly: ignore[bad-override]
    list_editable = ("active",)  # pyrefly: ignore[bad-override]
    filter_horizontal = ("subcategories",)  # pyrefly: ignore[bad-override]

    class Media:  # noqa: D106
        css = {  # noqa: RUF012
            "all": [
                "/static/djeym/css/djeym_admin.css",
            ],
        }

        js = (
            "/static/djeym/js/jquery.min.js",
            "/static/djeym/js/ckeditor_resize_image.js",
        )


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):  # noqa: D101
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    list_display = ("__str__", "active")  # pyrefly: ignore[bad-override]
    list_filter = ("ymap",)  # pyrefly: ignore[bad-override]
    list_editable = ("active",)  # pyrefly: ignore[bad-override]
    filter_horizontal = ("subcategories",)  # pyrefly: ignore[bad-override]

    class Media:  # noqa: D106
        css = {  # noqa: RUF012
            "all": [
                "/static/djeym/css/djeym_admin.css",
            ],
        }

        js = (
            "/static/djeym/js/jquery.min.js",
            "/static/djeym/js/ckeditor_resize_image.js",
        )


@admin.register(HeatPoint)
class HeatPointAdmin(admin.ModelAdmin):  # noqa: D101
    # ckeditor_change_form.html - Used by default.
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    list_display = ("title", "weight", "slug", "active")  # pyrefly: ignore[bad-override]
    list_editable = ("active",)  # pyrefly: ignore[bad-override]
    list_filter = ("ymap",)  # pyrefly: ignore[bad-override]
    readonly_fields = ("slug",)  # pyrefly: ignore[bad-override]
    search_fields = ("title",)  # pyrefly: ignore[bad-override]

    class Media:  # noqa: D106
        css = {  # noqa: RUF012
            "all": [
                "/static/djeym/css/djeym_admin.css",
            ],
        }


@admin.register(ClusterIcon)
class ClusterIconAdmin(admin.ModelAdmin):  # noqa: D101
    # ckeditor_change_form.html - Used by default.
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    list_display = ("title", "admin_thumbnail")  # pyrefly: ignore[bad-override]
    list_display_links = ("title", "admin_thumbnail")  # pyrefly: ignore[bad-override]
    readonly_fields = (  # pyrefly: ignore[bad-override]
        "size_width",
        "size_height",
        "offset_x",
        "offset_y",
    )

    formfield_overrides = {  # noqa: RUF012
        models.FileField: {"widget": AdminFileThumbWidget()},
    }

    class Media:  # noqa: D106
        css = {  # noqa: RUF012
            "all": [
                "/static/djeym/css/djeym_admin.css",
            ],
        }

        js = (
            "/static/djeym/js/jquery.min.js",
            "/static/djeym/js/get_icon_name.js",
        )


@admin.register(IconCollection)
class IconCollectionAdmin(admin.ModelAdmin):  # noqa: D101
    # ckeditor_change_form.html - Used by default.
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    change_list_template = "djeym/admin/icon_collection_change_list.html"
    list_display = (  # pyrefly: ignore[bad-override]
        "title",
        "admin_thumbnail",
        "get_export_file_btn",
        "get_icon_count",
        "get_count_of_active_icons",
    )
    list_display_links = ("title", "admin_thumbnail")  # pyrefly: ignore[bad-override]
    readonly_fields = ("slug",)  # pyrefly: ignore[bad-override]

    class Media:  # noqa: D106
        css = {  # noqa: RUF012
            "all": [
                "/static/djeym/css/djeym_admin.css",
            ],
        }

        js = (
            "/static/djeym/js/jquery.min.js",
            "/static/djeym/js/import_export.js",
        )


@admin.register(MarkerIcon)
class MarkerIconAdmin(admin.ModelAdmin):  # noqa: D101
    form = OffsetMarkerIconForm
    change_form_template = "djeym/admin/check_icon_offset_change_form.html"
    list_display = (  # pyrefly: ignore[bad-override]
        "title",
        "admin_thumbnail",
        "get_collection_name",
        "active",
        "slug",
    )  # pyrefly: ignore[bad-override]
    list_display_links = ("title", "admin_thumbnail")  # pyrefly: ignore[bad-override]
    readonly_fields = ("size_width", "size_height", "slug")  # pyrefly: ignore[bad-override]
    list_editable = ("active",)  # pyrefly: ignore[bad-override]
    list_filter = ("icon_collection",)  # pyrefly: ignore[bad-override]

    formfield_overrides = {  # noqa: RUF012
        models.FileField: {"widget": AdminFileThumbWidget()},
    }

    class Media:  # noqa: D106
        css = {  # noqa: RUF012
            "all": [
                "/static/djeym/css/djeym_admin.css",
            ],
        }

        js = (
            "/static/djeym/js/jquery.min.js",
            "/static/djeym/plugins/jquery_mousewheel/jquery.mousewheel.js",
            "/static/djeym/js/get_icon_name.js",
        )


@admin.register(LoadIndicator)
class LoadIndicatorAdmin(admin.ModelAdmin):  # noqa: D101
    # ckeditor_change_form.html - Used by default.
    change_form_template = "djeym/admin/ckeditor_change_form.html"

    list_display = ("title", "admin_thumbnail", "slug")  # pyrefly: ignore[bad-override]
    list_display_links = ("title", "admin_thumbnail")  # pyrefly: ignore[bad-override]
    readonly_fields = ("slug",)  # pyrefly: ignore[bad-override]

    formfield_overrides = {  # noqa: RUF012
        models.FileField: {"widget": AdminFileThumbWidget()},
    }

    class Media:  # noqa: D106
        css = {  # noqa: RUF012
            "all": [
                "/static/djeym/css/djeym_admin.css",
            ],
        }

        js = (
            "/static/djeym/js/jquery.min.js",
            "/static/djeym/js/get_icon_name.js",
        )


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):  # noqa: D101
    # ckeditor_change_form.html - Used by default.
    change_form_template = "djeym/admin/ckeditor_change_form.html"
    list_display = ("title", "slug")  # pyrefly: ignore[bad-override]

    class Media:  # noqa: D106
        css = {"all": ["/static/djeym/css/djeym_admin.css"]}  # noqa: RUF012
