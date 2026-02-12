"""Models."""

from __future__ import annotations

import json
import re
from decimal import Decimal

from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from ckeditor_uploader.fields import RichTextUploadingField
from colorful.fields import RGBColorField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit
from slugify import slugify

from .globals import (
    ANIMATION_SPEED,
    CLUSTER_BALLOON_CONTENT_LAYOUT_CHOICES,
    COLORS,
    FEATURE_HEAT_POINT,
    FEATURE_LINE,
    FEATURE_POINT,
    FEATURE_POLYGON,
    LOAD_INDICATOR_SIZE_CHOICES,
    STROKE_STYLE_CHOICES,
    THEME_TYPE_CHOICES,
    TRANSPARENCY_CHOICES,
    ZOOM_CHOICES,
)
from .raw_presets import raw_presets
from .signals_func import (
    convert_all_settings_to_json,
    icon_cluster_size_correction,
    icon_marker_size_correction,
    placemark_delete_statistics,
    polygon_delete_statistics,
    polyline_delete_statistics,
    refresh_icon,
    refresh_json_code,
)
from .utils import (
    heatpoint_update_json_code,
    make_upload_path,
    placemark_update_json_code,
    polygon_update_json_code,
    polyline_update_json_code,
    validate_coordinates,
    validate_image,
    validate_transparency,
)


class JsonSettings(models.Model):
    """All settings in json format."""

    ymap = models.OneToOneField(
        "Map",
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="json_settings",
        null=True,
        on_delete=models.CASCADE,
    )

    editor = models.TextField("All settings for editor page", default="{}")

    front = models.TextField("All settings for front page", default="{}")

    def __str__(self):  # noqa: D105
        return "Json Settings"


class TileSource(models.Model):
    """Source tile layer."""

    title = models.CharField(_("Title"), max_length=255, unique=True, default="")

    maxzoom = models.PositiveSmallIntegerField(_("Maximum zoom"), choices=ZOOM_CHOICES, default=12)

    minzoom = models.PositiveSmallIntegerField(_("Minimum zoom"), choices=ZOOM_CHOICES, default=0)

    source = models.TextField(_("Source"), default="")

    screenshot = models.ImageField(
        _("Screenshot"),
        upload_to=make_upload_path,
        validators=[validate_image],
        null=True,
        help_text=_("Recommended size - Width=360 x Height=180"),
    )

    copyrights = models.TextField(_("Copyrights"), default="")

    site = models.URLField(_("Site"), blank=True, default="")

    apikey = models.CharField(
        _("API Key"),
        max_length=255,
        blank=True,
        default="",
        help_text=_("API key or access_token"),
    )

    note = models.TextField(_("Note"), blank=True, default="")
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    middle = ImageSpecField(source="screenshot", processors=[ResizeToFill(360, 180, upscale=True)])

    @property
    def upload_dir(self):  # noqa: D102
        return "djeym/tile_screenshot"

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("title",)
        verbose_name = _("Tile Source")
        verbose_name_plural = _("Tile Sources")

    def save(self, *args, **kwargs):  # noqa: D102
        self.slug = slugify(str(self.title))  # pyrefly: ignore[bad-assignment]
        super().save(*args, **kwargs)

    def admin_thumbnail(self):  # noqa: D102
        if bool(self.screenshot):
            img_html = f'<img src="{self.screenshot.url}" height="40" alt="Screenshot">'
            return mark_safe(img_html)  # noqa: S308
        return ""

    admin_thumbnail.short_description = _("Screenshot")


class MapControls(models.Model):
    """Map Controls."""

    ymap = models.OneToOneField(
        "Map",
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="map_controls",
        null=True,
        on_delete=models.CASCADE,
    )

    geolocation = models.BooleanField(_("Geolocation"), default=True)
    search = models.BooleanField(_("Search by map"), default=True)
    provider = models.BooleanField(_("Search by organization name"), default=True)
    route = models.BooleanField(_("Routing panel"), default=True)
    traffic = models.BooleanField(_("Traffic jams"), default=True)
    typeselector = models.BooleanField(_("Map Layer Switch"), default=True)
    fullscreen = models.BooleanField(_("Full screen mode"), default=True)
    zoom = models.BooleanField(_("Zoom"), default=True)
    ruler = models.BooleanField(_("Ruler"), default=True)

    def __str__(self):  # noqa: D105
        return "{}".format(_("Map Controls"))

    class Meta:  # noqa: D106
        verbose_name_plural = _("Map Controls")

    def get_active_control_list(self):
        """Get a list of active controls."""
        controls_dict = {
            "geolocation": "geolocationControl",
            "search": "searchControl",
            "route": "routeButtonControl",
            "traffic": "trafficControl",
            "typeselector": "typeSelector",
            "fullscreen": "fullscreenControl",
            "zoom": "zoomControl",
            "ruler": "rulerControl",
        }
        return [val for key, val in controls_dict.items() if getattr(self, key)]


class HeatmapSettings(models.Model):
    """Heatmap settings."""

    ymap = models.OneToOneField(
        "Map",
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="heatmap_settings",
        null=True,
        on_delete=models.CASCADE,
    )

    radius = models.PositiveIntegerField(_("Point radius of influence (px)"), default=10)

    dissipating = models.BooleanField(
        _("Disperse points"),
        default=False,
        help_text=_("Enable - Disperse points on higher zoom levels according to radius. Disable - Don't disperse."),
    )

    opacity = models.CharField(
        _("Transparency of heat layer"),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default="0.8",
    )

    intensity = models.CharField(
        _("Intensity of median point"),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default="0.2",
    )

    gradient_color1 = RGBColorField(
        "gradient color 1",
        colors=COLORS,
        default="#66BB6A",
    )

    gradient_color2 = RGBColorField(
        "gradient color 2",
        colors=COLORS,
        default="#FDD835",
    )

    gradient_color3 = RGBColorField(
        "gradient color 3",
        colors=COLORS,
        default="#EF5350",
    )

    gradient_color4 = RGBColorField(
        "gradient color 4",
        colors=COLORS,
        default="#B71C1C",
    )

    active = models.BooleanField(_("Active Heatmap ?"), default=False)

    def __str__(self):  # noqa: D105
        return "{}".format(_("Settings"))

    class Meta:  # noqa: D106
        verbose_name = ngettext_lazy("Heatmap", "Heat maps", 1)
        verbose_name_plural = ngettext_lazy("Heatmap", "Heat maps", 1)


class Preset(models.Model):
    """Preset custom solution."""

    ymap = models.ForeignKey(
        "Map",
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="presets",
        null=True,
        on_delete=models.CASCADE,
    )

    position = models.PositiveSmallIntegerField(_("Position"), default=0)

    title = models.CharField(_("Title"), max_length=60, default="")

    icon = models.CharField(
        _("Icon"),
        max_length=255,
        default="",
        help_text=_("https://materialdesignicons.com/ - Example: help"),
    )

    html = models.TextField("Text | Html", default='<p style="color:#E91E63;">iPreset</p>')

    js = models.TextField("JS", blank=True, default="", help_text="JavaScript and jQuery")

    description = models.TextField(
        _("Description"),
        default="""<div style="color:#3F51B5;">Описание</div>
<div style="color:#E91E63;">Description</div>""",
        help_text=_("Brief description of the preset."),
    )

    autoheader = models.BooleanField(_("Automatically add to end of header"), default=False)
    autobody = models.BooleanField(_("Automatically add to end of description"), default=False)
    autofooter = models.BooleanField(_("Automatically add to end of footer"), default=False)

    placemark = models.BooleanField(_("Markers"), default=True)
    polyline = models.BooleanField(_("Routes"), default=True)
    polygon = models.BooleanField(ngettext_lazy("Territory", "Territorys", 2), default=True)

    slug = models.SlugField(max_length=255, blank=True, null=True)

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("position",)
        verbose_name = _("Preset")
        verbose_name_plural = _("Presets")

    def save(self, *args, **kwargs):  # noqa: D102
        self.slug = slugify(str(self.title))  # pyrefly: ignore[bad-assignment]
        super().save(*args, **kwargs)

    def clean(self):  # noqa: D102
        ymap = self.ymap
        raw_slug = slugify(str(self.title))
        if not bool(self.pk) and Preset.objects.filter(ymap=ymap, slug=raw_slug).count() > 0:
            raise ValidationError({"title": _("A preset with this name already exists for this map.")})


class GeneralSettings(models.Model):
    """General map settings."""

    ymap = models.OneToOneField(
        "Map",
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="general_settings",
        null=True,
        on_delete=models.CASCADE,
    )

    clustering_edit = models.BooleanField("Сlustering in editor", default=True)

    clustering_site = models.BooleanField("Сlustering on site", default=True)

    cluster_layout = models.CharField(
        "Layout for the cluster information window",
        max_length=255,
        choices=CLUSTER_BALLOON_CONTENT_LAYOUT_CHOICES,
        default="cluster#balloonTwoColumns",
    )

    cluster_icon_content = models.BooleanField(
        "Display the number of objects in the cluster icon",
        default=True,
    )

    cluster_icon_content_bg_color = RGBColorField(
        "Background color",
        colors=COLORS,
        default="#F5F5F5",
    )

    cluster_icon_content_txt_color = RGBColorField(
        "Text color",
        colors=COLORS,
        default="#212121",
    )

    controls_color = RGBColorField(
        "Color of controls",
        colors=COLORS,
        default="#43A047",
    )

    buttons_text_color = RGBColorField(
        "Text color on buttons",
        colors=COLORS,
        default="#FFFFFF",
    )

    theme_type = models.CharField(
        "Theme type - light | dark",
        max_length=255,
        choices=THEME_TYPE_CHOICES,
        default="light",
    )

    roundtheme = models.BooleanField("Round theme of controls", default=False)

    panorama = models.BooleanField("Panorama - on|off", default=True)

    width_panel_editor = models.PositiveSmallIntegerField("Width for panel of editor", default=380)

    width_panel_front = models.PositiveSmallIntegerField("Width for panel of front", default=380)

    open_panel_front = models.BooleanField("Open panel automatically", default=False)

    img_bg_panel_front = models.ImageField(
        "Background image for the site panel",
        upload_to=make_upload_path,
        blank=True,
        null=True,
    )

    tinting_panel_front = models.CharField(
        "Background under controls of panel",
        max_length=9,
        default="#00000000",
    )

    hide_group_name_panel_front = models.BooleanField(
        "Hide group names (Categories, Subcategories)",
        default=False,
    )

    width_map_front = models.CharField(
        "Width of Map for Front page",
        max_length=255,
        default="100%",
    )

    height_map_front = models.CharField(
        "Height of Map for Front page",
        max_length=255,
        default="600px",
    )

    img_bg_panel_front_thumb = ImageSpecField(
        source="img_bg_panel_front",
        processors=[ResizeToFit(width=96, upscale=False)],
        format="JPEG",
    )

    img_bg_panel_front_large = ImageSpecField(
        source="img_bg_panel_front",
        processors=[ResizeToFit(width=800, upscale=False)],
        format="JPEG",
        options={"quality": 40},
    )

    @property
    def upload_dir(self):  # noqa: D102
        return "djeym/general_settings"

    def __str__(self):  # noqa: D105
        return "Settings"

    class Meta:  # noqa: D106
        verbose_name = "General settings"
        verbose_name_plural = "General settings"

    def save(self, *args, **kwargs):  # noqa: D102
        colors_with_alpha = ["tinting_panel_front"]
        for color_name in colors_with_alpha:
            color = getattr(self, color_name)
            len_txt_color = len(color)
            if len_txt_color == 7:
                color += "FF"
            elif len_txt_color == 4:
                clean_hex = color.replace("#", "")
                color = f"#{clean_hex * 2}FF"
            setattr(self, color_name, color)
        super().save(*args, **kwargs)


class Map(models.Model):
    """Create a map."""

    title = models.CharField(
        _("Title"),
        max_length=60,
        unique=True,
        help_text=_(
            "Examples: Supermarkets of the city of Kharkov | Luxury hotels in Honolulu | Parking of primitive people",
        ),
    )

    icon_cluster = models.ForeignKey(
        "ClusterIcon",
        verbose_name=ngettext_lazy("Icon for cluster", "Icons for clusters", 1),
        related_name="ymap",
        null=True,
        on_delete=models.SET_NULL,
    )

    icon_collection = models.ForeignKey(
        "IconCollection",
        verbose_name=ngettext_lazy("Icon collection for markers", "Icon collections for markers", 1),
        related_name="ymap",
        null=True,
        on_delete=models.SET_NULL,
    )

    tile = models.ForeignKey(
        TileSource,
        verbose_name=_("Tile Source"),
        related_name="ymap",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    load_indicator = models.ForeignKey(
        "LoadIndicator",
        verbose_name="Load indicator",
        related_name="ymap",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    load_indicator_size = models.PositiveSmallIntegerField(
        "Load indicator size",
        choices=LOAD_INDICATOR_SIZE_CHOICES,
        default=64,
        editable=False,
    )

    animation_speed = models.CharField(
        "Load indicator animation speed",
        max_length=255,
        choices=ANIMATION_SPEED,
        default="0.8",
        editable=False,
    )

    disable_indicator_animation = models.BooleanField(
        "Disable loading indicator animation",
        default=False,
        help_text=_(
            "It may be useful for the abbreviation or logo of the company, if it does not make sense to animate them.",
        ),
        editable=False,
    )

    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    active = models.BooleanField(_("Active map ?"), default=True)

    zoom = models.PositiveSmallIntegerField(_("Zoom"), choices=ZOOM_CHOICES, default=3)

    latitude = models.CharField(
        _("Latitude"),
        max_length=255,
        default="0",
        validators=[validate_coordinates],
        help_text=_("Latitude center of the map."),
    )

    longitude = models.CharField(
        _("Longitude"),
        max_length=255,
        default="0",
        validators=[validate_coordinates],
        help_text=_("Longitude center of the map."),
    )

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    demo_categories = models.BooleanField("Add one-time categories", blank=True, default=True, editable=False)

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("title",)
        verbose_name = ngettext_lazy("Map", "Map", 5)
        verbose_name_plural = ngettext_lazy("Map", "Map", 2)

    def clean(self):  # noqa: D102
        # We check the presence in the collection of at least one active icon.
        # (Проверяем наличие в коллекции хотя бы одной активной иконки.)
        if bool(self.icon_collection) and self.icon_collection.icons.filter(active=True).count() == 0:
            msg = _("The collection must have at least one active icon.")
            raise ValidationError({"icon_collection": msg})
        # Coordinate check
        pattern = re.compile(r"^-?\d+(\.\d+)?$")
        if pattern.match(self.latitude) is None:  # pyrefly: ignore[no-matching-overload]
            msg = _("Invalid value.")
            raise ValidationError({"latitude": msg})
        if pattern.match(self.longitude) is None:  # pyrefly: ignore[no-matching-overload]
            msg = _("Invalid value.")
            raise ValidationError({"longitude": msg})

    @staticmethod
    def create_preset(ymap, raw_preset):  # noqa: D102
        Preset.objects.create(
            ymap=ymap,
            position=raw_preset["position"],
            title=raw_preset["title"],
            icon=raw_preset["icon"],
            html=raw_preset["html"],
            js=raw_preset["js"],
            description=raw_preset["description"],
        )

    def __init__(self, *args, **kwargs):  # noqa: D107
        super().__init__(*args, **kwargs)
        self.__icon_collection = self.icon_collection

    def save(self, *args, **kwargs):  # noqa: D102
        self.slug = slugify(str(self.title))  # pyrefly: ignore[bad-assignment]
        self.latitude = str(round(float(self.latitude), 6))  # pyrefly: ignore[bad-assignment, bad-argument-type]
        self.longitude = str(round(float(self.longitude), 6))  # pyrefly: ignore[bad-assignment, bad-argument-type]
        super().save(*args, **kwargs)
        if not hasattr(self, "map_controls"):
            MapControls.objects.create(ymap=self)
        if not hasattr(self, "heatmap_settings"):
            HeatmapSettings.objects.create(ymap=self)
        if not hasattr(self, "general_settings"):
            GeneralSettings.objects.create(ymap=self)
        if hasattr(self, "presets"):
            slugs = [item.slug for item in self.presets.all()]
            if len(slugs) > 0:
                for raw_preset in raw_presets:
                    if raw_preset["slug"] not in slugs:
                        self.create_preset(self, raw_preset)
            else:
                for raw_preset in raw_presets:
                    self.create_preset(self, raw_preset)
        if hasattr(self, "json_settings"):
            convert_all_settings_to_json(self)
        else:
            JsonSettings.objects.create(ymap=self)
            convert_all_settings_to_json(self)
        if self.demo_categories:
            CategoryPlacemark.objects.create(
                ymap=self,
                title="Demo Category",
                category_icon="help",
                category_color="#00C853",
            )
            CategoryPolyline.objects.create(
                ymap=self,
                title="Demo Category",
                category_icon="help",
                category_color="#00C853",
            )
            CategoryPolygon.objects.create(
                ymap=self,
                title="Demo Category",
                category_icon="help",
                category_color="#00C853",
            )
            self.demo_categories = False  # pyrefly: ignore[bad-assignment]
            self.save()
        if self.__icon_collection != self.icon_collection:
            placemarks = Placemark.objects.filter(ymap=self)
            for placemark in placemarks:
                placemark.save()

    def get_cluster(self):  # noqa: D102
        if bool(self.icon_cluster):
            img_html = f'<img src="{self.icon_cluster.svg.url}" height="40" alt="Cluster Icon">'
            return mark_safe(img_html)  # noqa: S308
        return ""

    get_cluster.short_description = _("Cluster")

    def get_icon_collection(self):  # noqa: D102
        icon = MarkerIcon.objects.filter(icon_collection=self.icon_collection).first()
        if icon is not None:
            img_html = f'<img src="{icon.svg.url}" height="40" alt="Icon">'
            return mark_safe(img_html)  # noqa: S308
        return ""

    get_icon_collection.short_description = _("Collection")

    def get_tile_screenshot(self):  # noqa: D102
        screenshot = "/static/djeym/img/default_tile.png"
        if bool(self.tile):
            screenshot = self.tile.screenshot.url
        img_html = f'<img src="{screenshot}" height="40" alt="Screenshot">'
        return mark_safe(img_html)  # noqa: S308

    get_tile_screenshot.short_description = _("Tile")

    def get_status_heatmap(self):  # noqa: D102
        icon = "cold_fire.svg"
        if hasattr(self, "heatmap_settings") and self.heatmap_settings.active:
            icon = "hot_fire.svg"
        img_html = f'<img src="/static/djeym/img/{icon}" height="40" alt="Icon">'
        return mark_safe(img_html)  # noqa: S308

    get_status_heatmap.short_description = ngettext_lazy("Heatmap", "Heat maps", 1)

    def get_load_indicator(self):  # noqa: D102
        if bool(self.load_indicator):
            img_html = f'<img src="{self.load_indicator.svg.url}" height="40" alt="Icon">'
            return mark_safe(img_html)  # noqa: S308
        return ""

    get_load_indicator.short_description = _("Indicator")

    def get_absolute_url(self):  # noqa: D102
        return reverse("djeym:ymap_editor", args=(self.slug,))


class CategoryPlacemark(SortableMixin):
    """Category of Placemark."""

    ymap = SortableForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="categories_placemark",
        null=True,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        _("Title"),
        max_length=60,
        help_text=_(
            "Name of any geographic area - Country Name or "
            "City Name or District Name or The name of the resort coast, etc.",
        ),
    )

    category_icon = models.CharField(
        _("Category Icon"),
        max_length=255,
        default="",
        help_text=_("https://materialdesignicons.com/ - Example: help"),
    )

    category_color = RGBColorField(_("Category color"), colors=COLORS, default="#00C853")

    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(_("Active category ?"), default=True)

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("position",)
        verbose_name = ngettext_lazy("-Category of marker", "-Category of markers", 1)
        verbose_name_plural = ngettext_lazy("-Category of marker", "-Category of markers", 2)

    def clean(self):  # noqa: D102
        count_category = CategoryPlacemark.objects.filter(ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _("A category with this name already exists for the selected map.")
            raise ValidationError({"title": msg})


class SubCategoryPlacemark(SortableMixin):
    """Subcategory of Placemark."""

    ymap = SortableForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="subcategories_placemark",
        null=True,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        _("Title"),
        max_length=60,
        help_text=_(
            "Subcategory - This is a characteristic feature that markers have. "
            "Examples: Parking or Bicycle Parking or ATM or "
            "Cafe or Wi-Fi or Playground, etc.",
        ),
    )

    category_icon = models.CharField(
        _("Category Icon"),
        max_length=255,
        default="",
        help_text=_("https://materialdesignicons.com/ - Example: help"),
    )

    category_color = RGBColorField(_("Category color"), colors=COLORS, default="#0091EA")

    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(_("Active category ?"), default=True)

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("position",)
        verbose_name = ngettext_lazy("_Subcategory of marker", "_Subcategory of markers", 1)
        verbose_name_plural = ngettext_lazy("_Subcategory of marker", "_Subcategory of markers", 2)

    def clean(self):  # noqa: D102
        count_category = SubCategoryPlacemark.objects.filter(ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _("A subcategory with this name already exists for the selected map.")
            raise ValidationError({"title": msg})


class CategoryPolyline(SortableMixin):
    """Category of Route."""

    ymap = SortableForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="categories_polyline",
        null=True,
        on_delete=models.CASCADE,
    )

    title = models.CharField(_("Title"), max_length=60, help_text=_("Examples: Tourist routes or Marathon routes etc."))

    category_icon = models.CharField(
        _("Category Icon"),
        max_length=255,
        default="",
        help_text=_("https://materialdesignicons.com/ - Example: help"),
    )

    category_color = RGBColorField(_("Category color"), colors=COLORS, default="#00C853")

    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(_("Active category ?"), default=True)

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("position",)
        verbose_name = ngettext_lazy("-Category of route", "-Category of routes", 1)
        verbose_name_plural = ngettext_lazy("-Category of route", "-Category of routes", 2)

    def clean(self):  # noqa: D102
        count_category = CategoryPolyline.objects.filter(ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _("A category with this name already exists for the selected map.")
            raise ValidationError({"title": msg})


class SubCategoryPolyline(SortableMixin):
    """Subcategory of Polyline."""

    ymap = SortableForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="subcategories_polyline",
        null=True,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        _("Title"),
        max_length=60,
        help_text=_("Subcategory - This is a characteristic feature that routes have."),
    )

    category_icon = models.CharField(
        _("Category Icon"),
        max_length=255,
        default="",
        help_text=_("https://materialdesignicons.com/ - Example: help"),
    )

    category_color = RGBColorField(_("Category color"), colors=COLORS, default="#0091EA")

    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(_("Active category ?"), default=True)

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("position",)
        verbose_name = ngettext_lazy("_Subcategory of route", "_Subcategory of routes", 1)
        verbose_name_plural = ngettext_lazy("_Subcategory of route", "_Subcategory of routes", 2)

    def clean(self):  # noqa: D102
        count_category = SubCategoryPolyline.objects.filter(ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _("A subcategory with this name already exists for the selected map.")
            raise ValidationError({"title": msg})


class CategoryPolygon(SortableMixin):
    """Category of Polygon."""

    ymap = SortableForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="categories_polygon",
        null=True,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        _("Title"),
        max_length=60,
        help_text=_(
            "The name of the aggregate of any geographic area. "
            "Examples: Honduran cities or Hawaiian beaches or "
            "Residential complexes in Antarctica.",
        ),
    )

    category_icon = models.CharField(
        _("Category Icon"),
        max_length=255,
        default="",
        help_text=_("https://materialdesignicons.com/ - Example: help"),
    )

    category_color = RGBColorField(_("Category color"), colors=COLORS, default="#00C853")

    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(_("Active category ?"), default=True)

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("position",)
        verbose_name = ngettext_lazy("-Category of territory", "-Category of territories", 1)
        verbose_name_plural = ngettext_lazy("-Category of territory", "-Category of territories", 2)

    def clean(self):  # noqa: D102
        count_category = CategoryPolygon.objects.filter(ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _("A category with this name already exists for the selected map.")
            raise ValidationError({"title": msg})


class SubCategoryPolygon(SortableMixin):
    """Subcategory of Polygon."""

    ymap = SortableForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="subcategories_polygon",
        null=True,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        _("Title"),
        max_length=60,
        help_text=_("Subcategory - This is a characteristic feature that the territories have."),
    )

    category_icon = models.CharField(
        _("Category Icon"),
        max_length=255,
        default="",
        help_text=_("https://materialdesignicons.com/ - Example: help"),
    )

    category_color = RGBColorField(_("Category color"), colors=COLORS, default="#0091EA")

    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(_("Active category ?"), default=True)

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("position",)
        verbose_name = ngettext_lazy("_Subcategory of territory", "_Subcategory of territories", 1)
        verbose_name_plural = ngettext_lazy("_Subcategory of territory", "_Subcategory of territories", 2)

    def clean(self):  # noqa: D102
        count_category = SubCategoryPolygon.objects.filter(ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _("A subcategory with this name already exists for the selected map.")
            raise ValidationError({"title": msg})


class Placemark(models.Model):
    """Placemark."""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="placemarks",
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        CategoryPlacemark,
        verbose_name=_("Category"),
        related_name="placemarks",
        on_delete=models.CASCADE,
    )

    subcategories = models.ManyToManyField(
        SubCategoryPlacemark,
        verbose_name=_("Subcategories"),
        related_name="placemarks",
        blank=True,
    )

    header = RichTextUploadingField(_("Place name"), default="", config_name="djeym")

    body = RichTextUploadingField(_("Description of the geo object"), blank=True, default="", config_name="djeym")

    user_image = models.ImageField(
        _("Image from user"),
        upload_to=make_upload_path,
        blank=True,
        null=True,
        editable=False,
        help_text=_("Image from the user to description the geo-object (width = 966px, quality = 40)."),
    )

    footer = RichTextUploadingField(_("Footer"), blank=True, default="", config_name="djeym")
    icon_slug = models.SlugField("{} (slug)".format(_("Icon")), max_length=255, null=True)

    coordinates = models.CharField(_("Coordinates"), max_length=255, default="[0,0]")

    like = models.PositiveIntegerField("Like", default=0, blank=True)
    dislike = models.PositiveIntegerField("Dislike", default=0, blank=True)
    active = models.BooleanField(_("Active placemark ?"), default=True)

    user_email = models.EmailField(
        _("User Email"),
        blank=True,
        null=True,
        help_text=_("To automatically send a one-time message if the user's geotag has been moderated and activated."),
    )

    user_ip = models.GenericIPAddressField(
        _("User IP"),
        blank=True,
        null=True,
        help_text=_("Ban user if vandalism is to be prevented."),
    )

    is_user_geotag = models.BooleanField(_("Is user's geotag ?"), default=False)

    geotag_status = models.ForeignKey(
        "GeotagStatus",
        verbose_name=_("Geotag status"),
        related_name="placemarks",
        on_delete=models.CASCADE,
        null=True,
    )

    json_code = models.TextField(_("JSON"), blank=True, default=json.dumps(FEATURE_POINT), editable=False)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    is_created = models.BooleanField("Is created ?", default=False, editable=False)

    is_sended_admin_email = models.BooleanField("Is sent to admin by email ?", default=False, editable=False)

    is_sended_user_email = models.BooleanField("Is sended user email ?", default=False, editable=False)

    user_image_q40 = ImageSpecField(source="user_image", format="JPEG", options={"quality": 40})

    @property
    def upload_dir(self):  # noqa: D102
        return "djeym/user_images"

    def __str__(self):  # noqa: D105
        header = re.sub(r"<.*?>", "", self.header)[:60]  # pyrefly: ignore[no-matching-overload]
        return mark_safe(header)  # noqa: S308

    class Meta:  # noqa: D106
        ordering = ("-id",)
        verbose_name = _("Marker")
        verbose_name_plural = _("Markers")

    def save(self, *args, **kwargs):  # noqa: D102
        # Rounding coordinates through regex.
        self.coordinates = re.sub(  # pyrefly: ignore[no-matching-overload]
            r"\d*\.\d+",
            lambda match: "{:.6f}".format(float(match.group())),  # noqa: UP032
            self.coordinates,
        )
        # Run create json_code.
        if self.is_created:
            self.json_code = placemark_update_json_code(self)
        super().save(*args, **kwargs)
        if not self.is_created:
            if bool(self.user_image):
                pattern = re.compile(r"<.*?>")
                self.header = (
                    f"<p>{pattern.sub('', self.header)}</p>"  # pyrefly: ignore[bad-assignment, no-matching-overload]
                )
                self.body = (
                    '<img src="{self.user_image_q40.url,}" width="322px" alt=""><p>{pattern.sub("", self.body)}</p>'  # noqa: E501, RUF100 # pyrefly: ignore[bad-assignment]
                )
            else:
                if self.is_user_geotag:
                    pattern = re.compile(r"<.*?>")
                    self.header = f"<p>{pattern.sub('', self.header)}</p>"  # pyrefly: ignore[bad-assignment, no-matching-overload]  # noqa: E261, E501, RUF100
                    self.body = f"<p>{pattern.sub('', self.body)}</p>"  # pyrefly: ignore[bad-assignment, no-matching-overload]  # noqa: E261, E501, RUF100
            self.is_created = True  # pyrefly: ignore[bad-assignment]
            self.save()


class Polyline(models.Model):
    """Polyline."""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="polylines",
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        CategoryPlacemark,
        verbose_name=_("Category"),
        related_name="polylines",
        on_delete=models.CASCADE,
    )

    subcategories = models.ManyToManyField(
        SubCategoryPlacemark,
        verbose_name=_("Subcategories"),
        related_name="polylines",
        blank=True,
    )

    header = RichTextUploadingField(_("Route name"), default="", config_name="djeym")

    body = RichTextUploadingField(_("Description of the geo object"), blank=True, default="", config_name="djeym")

    footer = RichTextUploadingField(_("Footer"), blank=True, default="", config_name="djeym")
    stroke_width = models.PositiveIntegerField(_("Stroke width"), default=5)

    stroke_color = RGBColorField(_("Line color"), colors=COLORS, default="#00C853")

    stroke_style = models.CharField(_("Line style"), max_length=255, choices=STROKE_STYLE_CHOICES, default="solid")

    stroke_opacity = models.CharField(
        _("Opacity line"),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default="0.9",
    )

    coordinates = models.TextField(_("Coordinates"), default="")
    like = models.PositiveIntegerField("Like", default=0, blank=True)
    dislike = models.PositiveIntegerField("Dislike", default=0, blank=True)
    active = models.BooleanField(_("Active route ?"), default=True)

    json_code = models.TextField(_("JSON"), blank=True, default=json.dumps(FEATURE_LINE), editable=False)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    is_created = models.BooleanField("Is created ?", default=False, editable=False)

    def __str__(self):  # noqa: D105
        header = re.sub(r"<.*?>", "", self.header)[:60]  # pyrefly: ignore[no-matching-overload]
        return mark_safe(header)  # noqa: S308

    class Meta:  # noqa: D106
        ordering = ("-id",)
        verbose_name = _("Route")
        verbose_name_plural = _("Routes")

    def save(self, *args, **kwargs):  # noqa: D102
        # Rounding coordinates through regex.
        self.coordinates = re.sub(r"\d*\.\d+", lambda match: "{:.6f}".format(float(match.group())), self.coordinates)  # noqa: UP032 # pyrefly: ignore[no-matching-overload]
        # Run create json_code.
        if self.is_created:
            self.json_code = polyline_update_json_code(self)
        super().save(*args, **kwargs)
        if not self.is_created:
            self.is_created = True  # pyrefly: ignore[bad-assignment]
            self.save()


class Polygon(models.Model):
    """Polygon."""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="polygons",
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        CategoryPlacemark,
        verbose_name=_("Category"),
        related_name="polygons",
        on_delete=models.CASCADE,
    )

    subcategories = models.ManyToManyField(
        SubCategoryPlacemark,
        verbose_name=_("Subcategories"),
        related_name="polygons",
        blank=True,
    )

    header = RichTextUploadingField(_("Territory name"), default="", config_name="djeym")

    body = RichTextUploadingField(_("Description of the geo object"), blank=True, default="", config_name="djeym")

    footer = RichTextUploadingField(_("Footer"), blank=True, default="", config_name="djeym")
    stroke_width = models.PositiveIntegerField(_("Stroke width"), default=2)

    stroke_color = RGBColorField(_("Line color"), colors=COLORS, default="#4caf50")

    stroke_opacity = models.CharField(
        _("Opacity line"),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default="0.9",
    )

    fill_color = RGBColorField(_("Fill color"), colors=COLORS, default="#00C853")

    stroke_style = models.CharField(_("Line style"), max_length=255, choices=STROKE_STYLE_CHOICES, default="solid")

    fill_opacity = models.CharField(
        _("Fill opacity"),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default="0.9",
    )

    coordinates = models.TextField(_("Coordinates"), default="")
    like = models.PositiveIntegerField("Like", default=0, blank=True)
    dislike = models.PositiveIntegerField("Dislike", default=0, blank=True)
    active = models.BooleanField(_("Active territory ?"), default=True)

    json_code = models.TextField(_("JSON"), blank=True, default=json.dumps(FEATURE_POLYGON), editable=False)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    is_created = models.BooleanField("Is created ?", default=False, editable=False)

    def __str__(self):  # noqa: D105
        header = re.sub(r"<.*?>", "", self.header)[:60]  # pyrefly: ignore[no-matching-overload]
        return mark_safe(header)  # noqa: S308

    class Meta:  # noqa: D106
        ordering = ("-id",)
        verbose_name = ngettext_lazy("Territory", "Territorys", 5)
        verbose_name_plural = ngettext_lazy("Territory", "Territorys", 2)

    def save(self, *args, **kwargs):  # noqa: D102
        # Rounding coordinates through regex.
        self.coordinates = re.sub(r"\d*\.\d+", lambda match: "{:.6f}".format(float(match.group())), self.coordinates)  # noqa: UP032 # pyrefly: ignore[no-matching-overload]
        # Run create json_code.
        if self.is_created:
            self.json_code = polygon_update_json_code(self)
        super().save(*args, **kwargs)
        if not self.is_created:
            self.is_created = True  # pyrefly: ignore[bad-assignment]
            self.save()


class HeatPoint(models.Model):
    """Heat Point."""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ngettext_lazy("Map", "Map", 1),
        related_name="heat_points",
        on_delete=models.CASCADE,
    )

    title = models.CharField(_("Place name"), max_length=60, blank=True, default="")

    weight = models.PositiveIntegerField(
        _("Weight"),
        default=0,
        blank=True,
        help_text=_(
            "Examples: Average property value on a district site or Number of cameras installed on a building, etc.",
        ),
    )

    coordinates = models.CharField(_("Coordinates"), max_length=255, default="[0,0]")

    active = models.BooleanField(_("Active heat point ?"), default=True)

    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    json_code = models.TextField(_("JSON"), blank=True, default=json.dumps(FEATURE_HEAT_POINT), editable=False)

    is_created = models.BooleanField("Is created ?", default=False, editable=False)

    def __str__(self):  # noqa: D105
        title = re.sub(r"<.*?>", "", self.title)[:60]  # pyrefly: ignore[no-matching-overload]
        return mark_safe(title)  # noqa: S308

    class Meta:  # noqa: D106
        verbose_name = ngettext_lazy("Heat Point", "Heat points", 5)
        verbose_name_plural = ngettext_lazy("Heat Point", "Heat points", 2)

    def save(self, *args, **kwargs):  # noqa: D102
        if bool(self.pk):
            if len(self.title) == 0:  # pyrefly: ignore[bad-argument-type]
                self.title = f"point {self.pk}"  # pyrefly: ignore[bad-assignment]
            title = self.title
            self.slug = slugify(  # pyrefly: ignore[bad-assignment]
                f"{re.sub(r'-*\d+$', '', title)}-{self.pk}",  # pyrefly: ignore[no-matching-overload]
            )
        # Rounding coordinates through regex.
        self.coordinates = re.sub(  # pyrefly: ignore[no-matching-overload]
            r"\d*\.\d+",
            lambda match: "{:.6f}".format(float(match.group())),  # noqa: UP032
            self.coordinates,
        )
        # Run create json_code.
        if self.is_created:
            self.json_code = heatpoint_update_json_code(self)
        super().save(*args, **kwargs)
        if not self.is_created:
            self.is_created = True  # pyrefly: ignore[bad-assignment]
            self.save()


class ClusterIcon(models.Model):
    """Icon for cluster."""

    svg = models.FileField(
        _("Icon"),
        upload_to=make_upload_path,
        null=True,
        help_text=_("Only SVG files."),
    )

    title = models.CharField(
        _("Cluster name"),
        max_length=60,
        default="",
        unique=True,
        help_text=_("Example: Green Garden"),
    )

    size_width = models.PositiveSmallIntegerField(_("Icon width"), default=0)
    size_height = models.PositiveSmallIntegerField(_("Icon height"), default=0)

    offset_x = models.DecimalField(_("Offset by axis - X"), max_digits=3, decimal_places=1, default=Decimal(".0"))

    offset_y = models.DecimalField(_("Offset by axis - Y"), max_digits=3, decimal_places=1, default=Decimal(".0"))

    @property
    def upload_dir(self):  # noqa: D102
        return "djeym/cluster_icons"

    def __str__(self):  # noqa: D105
        return str(self.title)

    def admin_thumbnail(self):  # noqa: D102
        if bool(self.svg):
            img_html = f'<img src="{self.svg.url}" height="40" alt="Icon">'
            return mark_safe(img_html)  # noqa: S308
        return ""

    admin_thumbnail.short_description = _("Icon")

    class Meta:  # noqa: D106
        ordering = ("title", "id")
        verbose_name = ngettext_lazy("Icon for cluster", "Icons for clusters", 5)
        verbose_name_plural = ngettext_lazy("Icon for cluster", "Icons for clusters", 2)

    def __init__(self, *args, **kwargs):  # noqa: D107
        super().__init__(*args, **kwargs)
        self.__old_image = self.svg

    def save(self, *args, **kwargs):  # noqa: D102
        old_image = self.__old_image
        new_image = self.svg
        if not bool(old_image) or (bool(old_image) and bool(new_image) and old_image.name != new_image.name):
            self.__old_image = new_image
            self.size_width = 0  # pyrefly: ignore[bad-assignment]
            self.size_height = 0  # pyrefly: ignore[bad-assignment]
            self.offset_x = Decimal(".0")  # pyrefly: ignore[bad-assignment]
            self.offset_y = Decimal(".0")  # pyrefly: ignore[bad-assignment]
        super().save(*args, **kwargs)


class IconCollection(models.Model):
    """Icon collection."""

    title = models.CharField(
        _("Collection name"),
        max_length=60,
        default="",
        unique=True,
        help_text=_("Example: Сherry Light Amber"),
    )

    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    def __str__(self):  # noqa: D105
        return str(self.title)

    def clean(self):  # noqa: D102
        slug = slugify(str(self.title))

        if bool(self.pk):
            slug_in_db = IconCollection.objects.get(pk=self.pk).slug
            maps = Map.objects.filter(icon_collection__pk=self.pk)
            if (slug != slug_in_db) and maps.count() > 0:
                msg = _("You cannot change the title, if the collection is tied to a map.")
                raise ValidationError({"title": msg})

    def save(self, *args, **kwargs):  # noqa: D102
        self.slug = slugify(str(self.title))  # pyrefly: ignore[bad-assignment]
        super().save(*args, **kwargs)

    def admin_thumbnail(self):  # noqa: D102
        icon = self.icons.all().first()
        if icon is not None:
            img_html = f'<img src="{icon.svg.url}" height="40" alt="Icon">'
            return mark_safe(img_html)  # noqa: S308
        return ""

    admin_thumbnail.short_description = _("Sample Icon")

    class Meta:  # noqa: D106
        ordering = ("title", "id")
        verbose_name = ngettext_lazy("Icon collection for markers", "Icon collections for markers", 5)
        verbose_name_plural = _("Icon collections for markers")

    def get_icon_count(self):  # noqa: D102
        return self.icons.all().count()

    get_icon_count.short_description = _("Icon count")

    def get_count_of_active_icons(self):  # noqa: D102
        return self.icons.filter(active=True).count()

    get_count_of_active_icons.short_description = _("Count of active icons")

    def get_export_file_btn(self):  # noqa: D102
        url = reverse("djeym:export_icon_collection", kwargs={"slug": self.slug})
        link_html = '<a href="{}" class="export_icon_collection_link">{} <div></div></a>'.format(
            url,
            _("Export Collection"),
        )
        return mark_safe(link_html)  # noqa: S308

    get_export_file_btn.short_description = _("Get a collection of icons")


class MarkerIcon(models.Model):
    """Icon for marker."""

    icon_collection = models.ForeignKey(
        IconCollection,
        verbose_name=_("Icon Collection"),
        related_name="icons",
        on_delete=models.CASCADE,
    )

    svg = models.FileField(
        _("Icon"),
        upload_to=make_upload_path,
        null=True,
        help_text=_("Only SVG files."),
    )

    title = models.CharField(_("Icon name"), max_length=60, default="", help_text=_("Example: Airport"))

    size_width = models.PositiveSmallIntegerField(_("Icon width"), default=0)
    size_height = models.PositiveSmallIntegerField(_("Icon height"), default=0)

    offset_x = models.DecimalField(
        _("Offset by axis - X"),
        max_digits=3,
        decimal_places=1,
        default=Decimal(".0"),
        help_text=_("Left, right - First time is automatically calculated."),
    )

    offset_y = models.DecimalField(
        _("Offset by axis - Y"),
        max_digits=3,
        decimal_places=1,
        default=Decimal(".0"),
        help_text=_("Up, down - First time is automatically calculated."),
    )

    active = models.BooleanField(
        _("Active icon ?"),
        default=True,
        help_text=_("If the project uses 2-3 icons, it makes sense to disable the rest to optimize the download."),
    )

    slug = models.SlugField(max_length=255, blank=True, null=True)

    @property
    def upload_dir(self):  # noqa: D102
        return "djeym/marker_icons"

    def __str__(self):  # noqa: D105
        return str(self.title)

    def admin_thumbnail(self):  # noqa: D102
        if bool(self.svg):
            img_html = f'<img src="{self.svg.url}" height="40" alt="Icon">'
            return mark_safe(img_html)  # noqa: S308
        return ""

    admin_thumbnail.short_description = _("Icon")

    class Meta:  # noqa: D106
        ordering = ("title", "id")
        verbose_name = ngettext_lazy("Icon for marker", "Icons for markers", 5)
        verbose_name_plural = ngettext_lazy("Icon for marker", "Icons for markers", 2)

    def __init__(self, *args, **kwargs):  # noqa: D107
        super().__init__(*args, **kwargs)
        self.__old_image = self.svg

    def save(self, *args, **kwargs):  # noqa: D102
        self.slug = slugify(str(self.title))  # pyrefly: ignore[bad-assignment]
        old_image = self.__old_image
        new_image = self.svg
        if not bool(old_image) or (bool(old_image) and bool(new_image) and old_image.name != new_image.name):
            self.__old_image = new_image
            self.size_width = 0  # pyrefly: ignore[bad-assignment]
            self.size_height = 0  # pyrefly: ignore[bad-assignment]
            self.offset_x = Decimal(".0")  # pyrefly: ignore[bad-assignment]
            self.offset_y = Decimal(".0")  # pyrefly: ignore[bad-assignment]
        super().save(*args, **kwargs)

    def clean(self):  # noqa: D102
        slug = slugify(str(self.title))

        if bool(self.pk):
            slug_in_db = MarkerIcon.objects.get(pk=self.pk).slug
            maps = Map.objects.filter(icon_collection__pk=self.icon_collection.pk)
            if (slug != slug_in_db) and maps.count() > 0:
                msg = _("You cannot change the title of the icon if the collection is tied to a map.")
                raise ValidationError({"title": msg})

        icon_count = MarkerIcon.objects.filter(slug=slug, icon_collection=self.icon_collection).count()
        if not bool(self.slug) and icon_count > 0:
            msg = _("For the selected collection, there is already an icon with a similar name.")
            raise ValidationError({"title": msg})

    def get_collection_name(self):  # noqa: D102
        return str(self.icon_collection.title)

    get_collection_name.short_description = _("Collection name")

    def get_size(self):  # noqa: D102
        return f"[{self.size_width},{self.size_height}]"

    def get_offset(self):  # noqa: D102
        return f"[{self.offset_x:f},{self.offset_y:f}]"


class LoadIndicator(models.Model):
    """Load Indicator."""

    svg = models.FileField(_("Icon"), upload_to=make_upload_path, null=True)

    title = models.CharField(_("Title"), unique=True, max_length=60, default="")

    slug = models.SlugField(max_length=255, blank=True, null=True)

    @property
    def upload_dir(self):  # noqa: D102
        return "djeym/load_indicators"

    def __str__(self):  # noqa: D105
        return str(self.title)

    class Meta:  # noqa: D106
        ordering = ("title", "id")
        verbose_name = _("Load indicator")
        verbose_name_plural = _("Load indicators")

    def save(self, *args, **kwargs):  # noqa: D102
        self.slug = slugify(str(self.title))  # pyrefly: ignore[bad-assignment]
        super().save(*args, **kwargs)

    def clean(self):  # noqa: D102
        slug = slugify(str(self.title))
        if slug == "default":
            msg = _("Default - Reserved name for the indicator. Choose another name.")
            raise ValidationError({"title": msg})

    def admin_thumbnail(self):  # noqa: D102
        if bool(self.svg):
            img_html = f'<img src="{self.svg.url}" height="40" alt="Icon">'
            return mark_safe(img_html)  # noqa: S308
        return ""

    admin_thumbnail.short_description = _("Icon")


class Statistics(models.Model):
    """Statistics."""

    obj_type = models.CharField("Object type", max_length=255, default="")
    obj_id = models.PositiveIntegerField("Object ID", default=0)
    ip = models.GenericIPAddressField("IP-address", null=True)
    likes = models.BooleanField("Likes", default=False)
    timestamp = models.DateTimeField("Date and Time", default=timezone.now)

    def __str__(self):  # noqa: D105
        return str(self.obj_type)

    class Meta:  # noqa: D106
        verbose_name = _("Record")
        verbose_name_plural = _("Statistics")


class BannedIP(models.Model):
    """Banned IP address."""

    ip = models.GenericIPAddressField("IP-address", null=True, unique=True)
    timestamp = models.DateTimeField("Date and Time", default=timezone.now)

    def __str__(self):  # noqa: D105
        return str(self.ip)

    class Meta:  # noqa: D106
        verbose_name = _("Banned IP address")
        verbose_name_plural = _("Banned IP addresses")


class GeotagStatus(models.Model):
    """Geotag status.

    Geotag - Geolocation sent by the user on the site page.
    """

    status = models.CharField(
        _("Status"),
        max_length=60,
        unique=True,
        default="",
        help_text=_("Examples: Offer accepted | The Offer is being processed | Offer completed"),
    )
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def __str__(self):  # noqa: D105
        return str(self.status)

    class Meta:  # noqa: D106
        ordering = ("-status", "-id")
        verbose_name = _("Geotag status")
        verbose_name_plural = _("Geotag statuses")

    def save(self, *args, **kwargs):  # noqa: D102
        self.slug = slugify(str(self.status))  # pyrefly: ignore[bad-assignment]
        super().save(*args, **kwargs)


# SIGNALS
# ------------------------------------------------------------------------------

# Cluster Icons - Size correction and offset correction.
post_save.connect(icon_cluster_size_correction, sender=ClusterIcon)

# Marker Icons - Size correction and offset correction.
post_save.connect(icon_marker_size_correction, sender=MarkerIcon)

# Refresh JSON-code if change Subcategories.
m2m_changed.connect(refresh_json_code, sender=Placemark.subcategories.through)
m2m_changed.connect(refresh_json_code, sender=Polyline.subcategories.through)
m2m_changed.connect(refresh_json_code, sender=Polygon.subcategories.through)


# Delete orphaned presets.
pre_delete.connect(placemark_delete_statistics, sender=Placemark)
pre_delete.connect(polyline_delete_statistics, sender=Polyline)
pre_delete.connect(polygon_delete_statistics, sender=Polygon)

# Refresh icon (slug) in placemarks after refreshing icon in MarkerIcon.
post_save.connect(refresh_icon, sender=MarkerIcon)

# Converting and updating all settings of Maps to JSON.
post_save.connect(convert_all_settings_to_json, sender=MarkerIcon)
post_save.connect(convert_all_settings_to_json, sender=TileSource)
post_save.connect(convert_all_settings_to_json, sender=GeneralSettings)
post_save.connect(convert_all_settings_to_json, sender=MapControls)
post_save.connect(convert_all_settings_to_json, sender=HeatmapSettings)
post_save.connect(convert_all_settings_to_json, sender=LoadIndicator)
post_save.connect(convert_all_settings_to_json, sender=Preset)
post_save.connect(convert_all_settings_to_json, sender=ClusterIcon)
post_save.connect(convert_all_settings_to_json, sender=CategoryPlacemark)
post_save.connect(convert_all_settings_to_json, sender=SubCategoryPlacemark)
post_save.connect(convert_all_settings_to_json, sender=CategoryPolyline)
post_save.connect(convert_all_settings_to_json, sender=SubCategoryPolyline)
post_save.connect(convert_all_settings_to_json, sender=CategoryPolygon)
post_save.connect(convert_all_settings_to_json, sender=SubCategoryPolygon)

post_delete.connect(convert_all_settings_to_json, sender=MarkerIcon)
post_delete.connect(convert_all_settings_to_json, sender=TileSource)
post_delete.connect(convert_all_settings_to_json, sender=LoadIndicator)
post_delete.connect(convert_all_settings_to_json, sender=Preset)
post_delete.connect(convert_all_settings_to_json, sender=CategoryPlacemark)
post_delete.connect(convert_all_settings_to_json, sender=SubCategoryPlacemark)
post_delete.connect(convert_all_settings_to_json, sender=CategoryPolyline)
post_delete.connect(convert_all_settings_to_json, sender=SubCategoryPolyline)
post_delete.connect(convert_all_settings_to_json, sender=CategoryPolygon)
post_delete.connect(convert_all_settings_to_json, sender=SubCategoryPolygon)
