# -*- coding: utf-8 -*-
import json
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import (m2m_changed, post_save, pre_delete,
                                      pre_save)
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from slugify import slugify
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField

from .raw_presets import raw_presets
from .utils import (DJEYM_YMAPS_ICONS_MAX_SIZE, cleaning_files_pre_delete,
                    cleaning_files_pre_save, get_size_correction,
                    get_size_from_svg, make_upload_path, validate_coordinates,
                    validate_hex_color, validate_image, validate_svg,
                    validate_transparency)

ZOOM_CHOICES = [(num, num) for num in range(24)]

# Load indicator animation speed
ANIMATION_SPEED = (
    ('0.3', '0.3'),
    ('0.4', '0.4'),
    ('0.5', '0.5'),
    ('0.6', '0.6'),
    ('0.7', '0.7'),
    ('0.8', '0.8'),
    ('0.9', '0.9'),
    ('1', '1'),
    ('1.1', '1.1'),
    ('1.2', '1.2'),
    ('1.3', '1.3'),
    ('1.4', '1.4'),
    ('1.5', '1.5'),
    ('1.6', '1.6'),
    ('1.7', '1.7'),
    ('1.8', '1.8'),
)

TRANSPARENCY_CHOICES = (
    ('0', '0'),
    ('0.1', '0.1'),
    ('0.2', '0.2'),
    ('0.3', '0.3'),
    ('0.4', '0.4'),
    ('0.5', '0.5'),
    ('0.6', '0.6'),
    ('0.7', '0.7'),
    ('0.8', '0.8'),
    ('0.9', '0.9'),
    ('1', '1')
)

CLUSTER_BALLOON_CONTENT_LAYOUT_CHOICES = (
    ('cluster#balloonTwoColumns', _('Two Columns')),
    ('cluster#balloonCarousel', _('Carousel'))
)

MAP_TYPE_CHOICES = (
    ('yandex#map', _('Scheme')),
    ('yandex#satellite', _('Satellite')),
    ('yandex#hybrid', _('Hybrid'))
)

LOAD_INDICATOR_SIZE_CHOICES = (
    (64, "64"),
    (96, "96"),
    (128, "128")
)

FEATURE_POINT = {
    "type": "Feature",
    "id": 0,
    "geometry": {
        "type": "Point",
        "coordinates": []
    },
    "properties": {
        "balloonContentHeader": "",
        "balloonContentBody": "",
        "balloonContentFooter": "",
        "id": 0,
        "categoryID": 0,
        "subCategoryIDs": [],
        "iconName": ""
    },
    "options": {
        "iconLayout": "default#image",
        "iconImageHref": "",
        "iconImageSize": [],
        "iconImageOffset": []
    }
}

FEATURE_LINE = {
    "type": "Feature",
    "id": 0,
    "geometry": {
        "type": "LineString",
        "coordinates": []
    },
    "properties": {
        "balloonContentHeader": "",
        "balloonContentBody": "",
        "balloonContentFooter": "",
        "id": 0,
        "categoryID": 0
    },
    "options": {
        "strokeWidth": 5,
        "strokeColor": "#1e98ff",
        "strokeOpacity": 0.9
    }
}

FEATURE_POLYGON = {
    "type": "Feature",
    "id": 0,
    "geometry": {
        "type": "Polygon",
        "coordinates": []
    },
    "properties": {
        "balloonContentHeader": "",
        "balloonContentBody": "",
        "balloonContentFooter": "",
        "id": 0,
        "categoryID": 0
    },
    "options": {
        "strokeWidth": 2,
        "strokeColor": "#1e98ff",
        "strokeOpacity": 0.9,
        "fillColor": "#1e98ff",
        "fillOpacity": 0.9
    }
}

FEATURE_HEAT_POINT = {
    "type": "Feature",
    "id": 0,
    "geometry": {
        "type": "Point",
        "coordinates": []
    },
    "properties": {
        "weight": 0
    }
}


class TileSource(models.Model):
    """Source tile layer"""

    title = models.CharField(
        _('Title'), max_length=255, unique=True, default="")

    maxzoom = models.PositiveSmallIntegerField(
        _('Maximum zoom'), choices=ZOOM_CHOICES, default=12)

    minzoom = models.PositiveSmallIntegerField(
        _('Minimum zoom'), choices=ZOOM_CHOICES, default=0)

    source = models.TextField(_('Source'), default="")

    screenshot = models.ImageField(
        _('Screenshot'),
        upload_to=make_upload_path,
        validators=[validate_image],
        null=True,
        help_text=_('Recommended size - Width=360 x Height=180'))

    copyrights = models.TextField(
        _('Copyrights'), blank=True, default="")

    site = models.URLField(_('Site'), blank=True, default="")

    apikey = models.CharField(
        _('API Key'),
        max_length=255,
        blank=True,
        default="",
        help_text=_('API key or access_token'))

    note = models.TextField(_('Note'), blank=True, default="")
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    middle = ImageSpecField(
        [ResizeToFill(360, 180, upscale=True)], source='screenshot')

    @property
    def upload_dir(self):
        return 'djeym_tile_screenshot'

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('title',)
        verbose_name = _('Tile Source')
        verbose_name_plural = _('Tile Sources')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(TileSource, self).save(*args, **kwargs)

    def admin_thumbnail(self):
        if bool(self.screenshot):
            return mark_safe('<img src="{0}" height="{1}" alt="Screenshot">'
                             .format(self.screenshot.url, 60))
        else:
            return ""
    admin_thumbnail.short_description = _('Screenshot')


class MapControls(models.Model):
    """Map Controls"""

    ymap = models.OneToOneField(
        'Map',
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='controls',
        null=True,
        on_delete=models.CASCADE
    )

    geolocation = models.BooleanField(_('Geolocation'), default=True)
    search = models.BooleanField(_('Search by map'), default=True)
    provider = models.BooleanField(
        _('Search by organization name'), default=True)
    route = models.BooleanField(_('Routing panel'), default=True)
    traffic = models.BooleanField(_('Traffic jams'), default=True)
    typeselector = models.BooleanField(_('Map Layer Switch'), default=True)
    fullscreen = models.BooleanField(_('Full screen mode'), default=True)
    zoom = models.BooleanField(_('Zoom'), default=True)
    ruler = models.BooleanField(_('Ruler'), default=True)
    maptype = models.CharField(
        _('Map type'),
        max_length=255,
        choices=MAP_TYPE_CHOICES,
        default='yandex#map')

    def __str__(self):
        return '{}'.format(_('Map Controls'))

    class Meta:
        verbose_name_plural = _('Map Controls')

    def get_control_list(self):
        """Get a list of selected controls."""
        controls_dict = {
            'geolocation': 'geolocationControl',
            'search': 'searchControl',
            'route': 'routeButtonControl',
            'traffic': 'trafficControl',
            'typeselector': 'typeSelector',
            'fullscreen': 'fullscreenControl',
            'zoom': 'zoomControl',
            'ruler': 'rulerControl'
        }
        return repr([val for key, val in controls_dict.items() if getattr(self, key)])


class ExternalModules(models.Model):
    """External modules - Plugins"""

    ymap = models.OneToOneField(
        'Map',
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='external_modules',
        null=True,
        on_delete=models.CASCADE
    )

    roundtheme = models.BooleanField(
        _('Round map controls theme'), default=False)

    heatmap = models.BooleanField(ungettext_lazy(
        'Heatmap', 'Heat maps', 1), default=False)

    areacalculation = models.BooleanField(
        _('Area Calculation'), default=True)

    def __str__(self):
        return '{}'.format(_('Enable'))

    class Meta:
        verbose_name = _('External modules')
        verbose_name_plural = _('External modules')


class HeatmapSettings(models.Model):
    """Heatmap settings"""

    ymap = models.OneToOneField(
        'Map',
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='heatmap_settings',
        null=True,
        on_delete=models.CASCADE
    )

    radius = models.PositiveIntegerField(
        _('Point radius of influence (px)'),
        default=10)

    dissipating = models.BooleanField(
        _('Disperse points'),
        default=False,
        help_text=_("Enable - Disperse points on higher zoom levels according to radius. "
                    "Disable - Don't disperse."))

    opacity = models.CharField(
        _('Transparency of heat layer'),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default='0.8')

    intensity = models.CharField(
        _('Intensity of median point'),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default='0.2')

    gradient_color1 = models.CharField(
        'gradient color 1',
        max_length=255,
        default='#56db40b3')

    gradient_color2 = models.CharField(
        'gradient color 2',
        max_length=255,
        default='#ffd21ecc')

    gradient_color3 = models.CharField(
        'gradient color 3',
        max_length=255,
        default='#ed4543e6')

    gradient_color4 = models.CharField(
        'gradient color 4',
        max_length=255,
        default='#b22222')

    def __str__(self):
        return '{}'.format(_('Settings'))

    class Meta:
        verbose_name = ungettext_lazy('Heatmap', 'Heat maps', 1)
        verbose_name_plural = ungettext_lazy('Heatmap', 'Heat maps', 1)


class Preset(models.Model):
    """Preset custom solution"""

    ymap = models.ForeignKey(
        'Map',
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='presets',
        null=True,
        on_delete=models.CASCADE)

    title = models.CharField(_('Title'), max_length=60, default="")

    icon = models.CharField(
        _('Icon (html tag)'),
        max_length=255,
        blank=True,
        default='<i class="far fa-smile"></i>',
        help_text=_('https://fontawesome.com/icons?d=gallery&m=free - '
                    'Example: &lt;i class="fab fa-android"&gt;&lt;/i&gt;'))

    html = models.TextField(
        'HTML', default='<p style="color:#e91e63;">iPreset</p>')

    js = models.TextField('JS', blank=True, default="",
                          help_text='JavaScript and jQuery')

    description = models.TextField(
        _('Description'),
        default="""<div>Описание</div>
<div style="color:#607D8B;">Description</div>""",
        help_text=_('Brief description of the preset.'))

    autoheader = models.BooleanField(
        _('Automatically add to end of header'), default=False)
    autobody = models.BooleanField(
        _('Automatically add to end of description'), default=False)
    autofooter = models.BooleanField(
        _('Automatically add to end of footer'), default=False)

    placemark = models.BooleanField(_('Markers'), default=True)
    polyline = models.BooleanField(_('Routes'), default=True)
    polygon = models.BooleanField(ungettext_lazy(
        'Territory', 'Territorys', 2), default=True)

    position = models.PositiveSmallIntegerField(
        _('Position'), default=0, blank=True)

    slug = models.SlugField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('position',)
        verbose_name = _('Preset')
        verbose_name_plural = _('Presets')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Preset, self).save(*args, **kwargs)

    def clean(self):
        ymap = self.ymap
        raw_slug = slugify(self.title)
        if not bool(self.pk) and Preset.objects.filter(ymap=ymap, slug=raw_slug).count() > 0:
            raise ValidationError(
                {'title': _('A preset with this name already exists for this map.')})


class GeneralSettings(models.Model):
    """General map settings"""

    ymap = models.OneToOneField(
        'Map',
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='general_settings',
        null=True,
        on_delete=models.CASCADE
    )

    clustering_edit = models.BooleanField(
        _('Сlustering in editor'), default=True)

    clustering_site = models.BooleanField(
        _('Сlustering on site'), default=True)

    cluster_layout = models.CharField(
        _('Layout for the cluster information window'),
        max_length=255,
        choices=CLUSTER_BALLOON_CONTENT_LAYOUT_CHOICES,
        default='cluster#balloonTwoColumns')

    cluster_icon_content = models.BooleanField(
        _('Display the number of objects in the cluster icon'), default=True)

    cluster_icon_content_bg_color = models.CharField(
        _('Background color'),
        max_length=255,
        default='#ffffff',
        validators=[validate_hex_color])

    cluster_icon_content_txt_color = models.CharField(
        _('Text color'),
        max_length=255,
        default='#333333',
        validators=[validate_hex_color])

    disable_site_panel = models.BooleanField(
        _('Disable the panel on the site (button with the image of '
          'the gear and the eye in the center)'),
        default=False)

    def __str__(self):
        return '{}'.format(_('Settings'))

    class Meta:
        verbose_name = _('General settings')
        verbose_name_plural = _('General settings')


class Map(models.Model):
    """Create a map"""

    title = models.CharField(
        _('Title'),
        max_length=60,
        unique=True,
        help_text=_('Examples: Supermarkets of the city of Kharkov or '
                    'Hawaii - Oahu Island or Luxury hotels in Honolulu or '
                    'Parking of primitive people, etc.'))

    icon_cluster = models.ForeignKey(
        'CustomClusterIcon',
        verbose_name=ungettext_lazy(
            'Icon for cluster', 'Icons for clusters', 1),
        related_name='placemark_custom_cluster',
        null=True,
        on_delete=models.SET_NULL)

    icon_collection = models.ForeignKey(
        'IconCollection',
        verbose_name=ungettext_lazy('Icon collection for markers',
                                    'Icon collections for markers', 1),
        related_name='map_icon_collection',
        null=True,
        on_delete=models.SET_NULL
    )

    tile = models.ForeignKey(
        TileSource,
        verbose_name=_('Tile Source'),
        related_name='maptile',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    load_indicator = models.ForeignKey(
        'LoadIndicator',
        verbose_name=_('Load indicator'),
        related_name='map_load_indicator',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_(
            'https://github.com/genkosta/django-editor-ymaps/blob/master/Spinner.zip')
    )

    load_indicator_size = models.PositiveSmallIntegerField(
        _('Load indicator size'),
        choices=LOAD_INDICATOR_SIZE_CHOICES,
        default=64
    )

    animation_speed = models.CharField(
        _('Load indicator animation speed'),
        max_length=255,
        choices=ANIMATION_SPEED,
        default='0.8')

    disable_indicator_animation = models.BooleanField(
        _('Disable loading indicator animation'),
        default=False,
        help_text=_(
            'It may be useful for the abbreviation or logo of the company, '
            'if it does not make sense to animate them.')
    )

    active = models.BooleanField(_('Active map'), default=True)

    zoom = models.PositiveSmallIntegerField(
        _('Zoom'), choices=ZOOM_CHOICES, default=3)

    latitude = models.CharField(_('Latitude'), max_length=255, default='0',
                                validators=[validate_coordinates],
                                help_text=_('Latitude center of the map.'))

    longitude = models.CharField(_('Longitude'), max_length=255, default='0',
                                 validators=[validate_coordinates],
                                 help_text=_('Longitude center of the map.'))

    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('title',)
        verbose_name = ungettext_lazy('Map', 'Map', 5)
        verbose_name_plural = ungettext_lazy('Map', 'Map', 2)

    def clean(self):
        """
        We check the presence in the collection of at least one active icon.
        Проверяем наличие в коллекции хотя бы одной активной иконки.
        """
        if bool(self.icon_collection) and \
                self.icon_collection.icons.filter(active=True).count() == 0:
            raise ValidationError({'icon_collection':
                                   _('The collection must have at least one active icon.')})

    @staticmethod
    def create_preset(ymap, raw_preset):
        Preset.objects.create(
            ymap=ymap,
            title=raw_preset['title'],
            icon=raw_preset['icon'],
            html=raw_preset['html'],
            js=raw_preset['js'],
            description=raw_preset['description']
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Map, self).save(*args, **kwargs)
        if not hasattr(self, 'controls'):
            MapControls.objects.create(ymap=self)
        if not hasattr(self, 'external_modules'):
            ExternalModules.objects.create(ymap=self)
        if not hasattr(self, 'heatmap_settings'):
            HeatmapSettings.objects.create(ymap=self)
        if not hasattr(self, 'general_settings'):
            GeneralSettings.objects.create(ymap=self)
        if hasattr(self, 'presets'):
            ymap = Map.objects.get(pk=self.pk)
            slugs = [item.slug for item in ymap.presets.all()]
            if len(slugs) > 0:
                for raw_preset in raw_presets:
                    if raw_preset['slug'] not in slugs:
                        self.create_preset(ymap, raw_preset)
            else:
                for raw_preset in raw_presets:
                    self.create_preset(ymap, raw_preset)

    def get_custom_cluster(self):
        if bool(self.icon_cluster):
            return mark_safe('<img src="{0}" height="{1}" alt="Cluster Icon">'
                             .format(self.icon_cluster.svg.url, DJEYM_YMAPS_ICONS_MAX_SIZE))
        else:
            return ""
    get_custom_cluster.short_description = _('Cluster Icon')

    def get_custom_marker_icon(self):
        icon = CustomMarkerIcon.objects.filter(
            icon_collection=self.icon_collection).first()
        if icon is not None:
            return mark_safe('<img src="{0}" height="{1}" alt="Icon">'
                             .format(icon.svg.url, DJEYM_YMAPS_ICONS_MAX_SIZE))
        else:
            return ""
    get_custom_marker_icon.short_description = _(
        'Example icon from collection')

    def get_tile_screenshot(self):
        if bool(self.tile):
            return mark_safe('<img src="{0}" height="60" alt="Screenshot">'
                             .format(self.tile.screenshot.url))
        else:
            return mark_safe(
                '<img src="/static/djeym/img/default_tile.png" height="60" alt="Screenshot">')
    get_tile_screenshot.short_description = _('Tile screenshot')

    def get_status_heatmap(self):
        if hasattr(self, 'heatmap_settings') and self.external_modules.heatmap:
            return mark_safe(
                '<img src="/static/djeym/img/red_check.svg/" height="30" alt="Icon">')
        else:
            return mark_safe(
                '<img src="/static/djeym/img/colder_minus.svg/" height="30" alt="Icon">')
    get_status_heatmap.short_description = _('Heat map status')

    def get_load_indicator(self):
        if bool(self.load_indicator):
            return mark_safe('<img src="{0}" height="{1}" alt="Icon">'
                             .format(self.load_indicator.svg.url, DJEYM_YMAPS_ICONS_MAX_SIZE))
        else:
            return ""
    get_load_indicator.short_description = _('Load indicator')

    def get_absolute_url(self):
        return reverse('djeym:editor_ymap', args=(self.slug,))


class CategoryPlacemark(models.Model):
    """Category of placemark"""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='category_placemark',
        on_delete=models.CASCADE)

    title = models.CharField(
        _('Title'),
        max_length=60,
        help_text=_('Name of any geographic area - Country Name or '
                    'City Name or District Name or The name of the resort coast, etc.'))

    category_icon = models.CharField(
        _('Category Icon (html tag)'),
        max_length=255,
        blank=True,
        default="",
        help_text=_('https://fontawesome.com/icons?d=gallery&m=free - '
                    'Example: &lt;i class="fab fa-android"&gt;&lt;/i&gt;'))

    category_color = models.CharField(
        _("Category color"),
        max_length=255,
        default='#00bfff',
        validators=[validate_hex_color],
        help_text=_('Applies to Checkboxes and Radio Buttons.'))

    active = models.BooleanField(_('Active category'), default=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('title',)
        verbose_name = ungettext_lazy(
            'Category of placemark', 'Category of placemarks', 5)
        verbose_name_plural = ungettext_lazy(
            'Category of placemark', 'Category of placemarks', 2)

    def clean(self):
        count_category = CategoryPlacemark.objects.filter(
            ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _(
                'A category with this name already exists for the selected map.')
            raise ValidationError({'title': msg})

    def get_map_name(self):
        return "{}".format(self.ymap.title)
    get_map_name.short_description = ungettext_lazy('Map', 'Map', 1)

    def get_title(self):
        return "{}".format(self.title)
    get_title.short_description = _("Category name")

    def get_category_icon(self):
        if bool(self.category_icon):
            return mark_safe('<div class="category_icon">{}</div>'.format(self.category_icon))
        else:
            return ""
    get_category_icon.short_description = _('Category Icon')

    def get_category_color(self):
        return mark_safe("<div class=\"djeym_category_color\" "
                         "style=\"background:{};\"></div>".format(self.category_color))
    get_category_color.short_description = _("Category color")


class SubCategoryPlacemark(models.Model):
    """Subcategory of placemark"""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='subcategory_placemark',
        on_delete=models.CASCADE)

    title = models.CharField(
        _('Title'),
        max_length=60,
        help_text=_('Subcategory - This is what complements the categories of markers. '
                    'Examples: Parking or Bicycle Parking or ATM or '
                    'Cafe or Wi-Fi or Playground, etc.'))

    category_icon = models.CharField(
        _('Category Icon (html tag)'),
        max_length=255,
        blank=True,
        default="",
        help_text=_('https://fontawesome.com/icons?d=gallery&m=free - '
                    'Example: &lt;i class="fab fa-android"&gt;&lt;/i&gt;'))

    category_color = models.CharField(
        _("Category color"),
        max_length=255,
        default='#ffcc00',
        validators=[validate_hex_color],
        help_text=_('Applies to Checkboxes and Radio Buttons.'))

    active = models.BooleanField(_('Active category'), default=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('title',)
        verbose_name = ungettext_lazy(
            'Subcategory of placemark', 'Subcategory of placemarks', 5)
        verbose_name_plural = ungettext_lazy(
            'Subcategory of placemark', 'Subcategory of placemarks', 2)

    def clean(self):
        count_category = SubCategoryPlacemark.objects.filter(
            ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _(
                'A category with this name already exists for the selected map.')
            raise ValidationError({'title': msg})

    def get_map_name(self):
        return "{}".format(self.ymap.title)
    get_map_name.short_description = ungettext_lazy('Map', 'Map', 1)

    def get_title(self):
        return "{}".format(self.title)
    get_title.short_description = _("Category name")

    def get_category_icon(self):
        if bool(self.category_icon):
            return mark_safe('<div class="category_icon">{}</div>'.format(self.category_icon))
        else:
            return ""
    get_category_icon.short_description = _('Icon')

    def get_category_color(self):
        return mark_safe("<div class=\"djeym_category_color\" "
                         "style=\"background:{};\"></div>".format(self.category_color))
    get_category_color.short_description = _("Category color")


class CategoryPolyline(models.Model):
    """Category of route"""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='category_polyline',
        on_delete=models.CASCADE)

    title = models.CharField(
        _('Title'),
        max_length=60,
        help_text=_('Examples: Tourist routes or Marathon routes etc.'))

    category_icon = models.CharField(
        _('Category Icon (html tag)'),
        max_length=255,
        blank=True,
        default="",
        help_text=_('https://fontawesome.com/icons?d=gallery&m=free - '
                    'Example: &lt;i class="fab fa-android"&gt;&lt;/i&gt;'))

    category_color = models.CharField(
        _("Category color"),
        max_length=255,
        default='#00bfff',
        validators=[validate_hex_color],
        help_text=_('Applies to Checkboxes and Radio Buttons.'))

    active = models.BooleanField(_('Active category'), default=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('title',)
        verbose_name = ungettext_lazy(
            'Category of route', 'Category of routes', 5)
        verbose_name_plural = ungettext_lazy(
            'Category of route', 'Category of routes', 2)

    def clean(self):
        count_category = CategoryPolyline.objects.filter(
            ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _(
                'A category with this name already exists for the selected map.')
            raise ValidationError({'title': msg})

    def get_map_name(self):
        return "{}".format(self.ymap.title)
    get_map_name.short_description = ungettext_lazy('Map', 'Map', 1)

    def get_title(self):
        return "{}".format(self.title)
    get_title.short_description = _("Category name")

    def get_category_icon(self):
        if bool(self.category_icon):
            return mark_safe('<div class="category_icon">{}</div>'.format(self.category_icon))
        else:
            return ""
    get_category_icon.short_description = _('Category Icon')

    def get_category_color(self):
        return mark_safe("<div class=\"djeym_category_color\" "
                         "style=\"background:{};\"></div>".format(self.category_color))
    get_category_color.short_description = _("Category color")


class CategoryPolygon(models.Model):
    """Category of territory"""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='category_polygon',
        on_delete=models.CASCADE)

    title = models.CharField(
        _('Title'),
        max_length=60,
        help_text=_('The name of the aggregate of any geographic area. '
                    'Examples: Honduran cities or Hawaiian beaches or '
                    'Residential complexes in Antarctica.'))

    category_icon = models.CharField(
        _('Category Icon (html tag)'),
        max_length=255,
        blank=True,
        default="",
        help_text=_('https://fontawesome.com/icons?d=gallery&m=free - '
                    'Example: &lt;i class="fab fa-android"&gt;&lt;/i&gt;'))

    category_color = models.CharField(
        _("Category color"),
        max_length=255,
        default='#00bfff',
        validators=[validate_hex_color],
        help_text=_('Applies to Checkboxes and Radio Buttons.'))

    active = models.BooleanField(_('Active category'), default=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('title',)
        verbose_name = ungettext_lazy(
            'Category of territory', 'Category of territories', 5)
        verbose_name_plural = ungettext_lazy(
            'Category of territory', 'Category of territories', 2)

    def clean(self):
        count_category = CategoryPolygon.objects.filter(
            ymap=self.ymap, title=self.title).count()
        if not bool(self.pk) and count_category > 0:
            msg = _(
                'A category with this name already exists for the selected map.')
            raise ValidationError({'title': msg})

    def get_map_name(self):
        return "{}".format(self.ymap.title)
    get_map_name.short_description = ungettext_lazy('Map', 'Map', 1)

    def get_title(self):
        return "{}".format(self.title)
    get_title.short_description = _("Category name")

    def get_category_icon(self):
        if bool(self.category_icon):
            return mark_safe('<div class="category_icon">{}</div>'.format(self.category_icon))
        else:
            return ""
    get_category_icon.short_description = _('Category Icon')

    def get_category_color(self):
        return mark_safe("<div class=\"djeym_category_color\" "
                         "style=\"background:{};\"></div>".format(self.category_color))
    get_category_color.short_description = _("Category color")


class Placemark(models.Model):
    """Placemark"""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='placemark_map',
        on_delete=models.CASCADE)

    category = ChainedForeignKey(
        CategoryPlacemark,
        verbose_name=_('Category'),
        related_name='placemark_category',
        chained_field="ymap",
        chained_model_field="ymap",
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE)

    subcategories = ChainedManyToManyField(
        SubCategoryPlacemark,
        verbose_name=_('Subcategories'),
        related_name='placemark_subcategories',
        chained_field="ymap",
        chained_model_field="ymap",
        blank=True,
        auto_choose=False)

    header = models.TextField(_('Place name'), default="")
    body = models.TextField(_('Content'), blank=True, default="")
    footer = models.TextField(_('Footer'), blank=True, default="")
    icon_name = models.CharField(
        _('Icon name'), max_length=255, default="")

    coordinates = models.CharField(
        _('Coordinates'), max_length=255, default='[0,0]')

    like = models.PositiveIntegerField('Like', default=0, blank=True)
    dislike = models.PositiveIntegerField('Dislike', default=0, blank=True)
    active = models.BooleanField(_('Active placemark'), default=True)

    json_code = models.TextField(
        _('JSON'), blank=True, default=json.dumps(FEATURE_POINT))

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return mark_safe('{}'.format(self.header))

    class Meta:
        ordering = ("-id",)
        verbose_name = _('Placemark')
        verbose_name_plural = _('Placemarks')


class Polyline(models.Model):
    """Polyline"""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='polyline_map',
        on_delete=models.CASCADE)

    category = ChainedForeignKey(
        CategoryPolyline,
        verbose_name=_('Category'),
        related_name='polyline_category',
        chained_field="ymap",
        chained_model_field="ymap",
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE)

    header = models.TextField(_('Route name'), default="")
    body = models.TextField(_('Content'), blank=True, default="")
    footer = models.TextField(_('Footer'), blank=True, default="")
    stroke_width = models.PositiveIntegerField(_('Stroke width'), default=5)

    stroke_color = models.CharField(
        _('Line color'),
        max_length=255,
        default='#1e98ff',
        validators=[validate_hex_color])

    stroke_opacity = models.CharField(
        _('Opacity line'),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default='0.9')

    coordinates = models.TextField(_('Coordinates'), default="")
    like = models.PositiveIntegerField('Like', default=0, blank=True)
    dislike = models.PositiveIntegerField('Dislike', default=0, blank=True)
    active = models.BooleanField(_('Active route'), default=True)

    json_code = models.TextField(
        _('JSON'), blank=True, default=json.dumps(FEATURE_LINE))

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return mark_safe('{}'.format(self.header))

    class Meta:
        ordering = ("-id",)
        verbose_name = _('Route')
        verbose_name_plural = _('Routes')


class Polygon(models.Model):
    """Polygon"""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='polygon_map',
        on_delete=models.CASCADE)

    category = ChainedForeignKey(
        CategoryPolygon,
        verbose_name=_('Category'),
        related_name='polygon_category',
        chained_field="ymap",
        chained_model_field="ymap",
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE)

    header = models.TextField(_('Territory name'), default='')
    body = models.TextField(_('Content'), blank=True, default="",)
    footer = models.TextField(_('Footer'), blank=True, default="")
    stroke_width = models.PositiveIntegerField(_('Stroke width'), default=2)

    stroke_color = models.CharField(
        _('Line color'),
        max_length=255,
        default='#1e98ff',
        validators=[validate_hex_color])

    stroke_opacity = models.CharField(
        _('Opacity line'),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default='0.9')

    fill_color = models.CharField(
        _('Fill color'),
        max_length=255,
        default='#1e98ff',
        validators=[validate_hex_color])

    fill_opacity = models.CharField(
        _('Fill opacity'),
        max_length=255,
        choices=TRANSPARENCY_CHOICES,
        validators=[validate_transparency],
        default='0.9')

    coordinates = models.TextField(_('Coordinates'), default="")
    like = models.PositiveIntegerField('Like', default=0, blank=True)
    dislike = models.PositiveIntegerField('Dislike', default=0, blank=True)
    active = models.BooleanField(_('Active territory'), default=True)

    json_code = models.TextField(
        _('JSON'), blank=True, default=json.dumps(FEATURE_POLYGON))

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return mark_safe('{}'.format(self.header))

    class Meta:
        ordering = ("-id",)
        verbose_name = ungettext_lazy('Territory', 'Territorys', 5)
        verbose_name_plural = ungettext_lazy('Territory', 'Territorys', 2)


class HeatPoint(models.Model):
    """Heat Point"""

    ymap = models.ForeignKey(
        Map,
        verbose_name=ungettext_lazy('Map', 'Map', 1),
        related_name='heat_point',
        on_delete=models.CASCADE)

    title = models.CharField(
        _('Place name'),
        max_length=60,
        blank=True,
        default="")

    weight = models.PositiveIntegerField(
        _('Weight'),
        default=0,
        blank=True,
        help_text=_('Examples: Average property value on a district site or '
                    'Number of cameras installed on a building, etc.'))

    coordinates = models.CharField(
        _('Coordinates'), max_length=255, default='[0,0]')

    active = models.BooleanField(_('Active heat point'), default=True)

    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    json_code = models.TextField(
        _('JSON'), blank=True, default=json.dumps(FEATURE_HEAT_POINT))

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = ungettext_lazy('Heat Point', 'Thermal points', 5)
        verbose_name_plural = ungettext_lazy('Heat Point', 'Thermal points', 2)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(HeatPoint, self).save(*args, **kwargs)
        if len(self.title) == 0:
            self.title = '{0} - {1}'.format(ungettext_lazy(
                'Heat Point', 'Thermal points', 1), self.pk)
            self.save()


class CustomClusterIcon(models.Model):
    """Custom Cluster Icons"""

    svg = models.FileField(
        _('Icon'),
        upload_to=make_upload_path,
        validators=[validate_svg],
        null=True,
        help_text=_('Only SVG files.'))

    title = models.CharField(
        _('Cluster name'),
        max_length=60,
        default="",
        unique=True,
        help_text=_('Example: Green Garden'))

    size_width = models.PositiveSmallIntegerField(_('Icon width'), default=0)
    size_height = models.PositiveSmallIntegerField(_('Icon height'), default=0)

    offset_x = models.DecimalField(
        _('Offset by axis - X'),
        max_digits=3,
        decimal_places=1,
        default=Decimal(".0"))

    offset_y = models.DecimalField(
        _('Offset by axis - Y'),
        max_digits=3,
        decimal_places=1,
        default=Decimal(".0"))

    @property
    def upload_dir(self):
        return 'djeym_custom_icons'

    def __str__(self):
        return '{}'.format(self.title)

    def admin_thumbnail(self):
        if bool(self.svg):
            return mark_safe('<img src="{0}" height="{1}" alt="Icon">'
                             .format(self.svg.url, DJEYM_YMAPS_ICONS_MAX_SIZE))
        else:
            return ""
    admin_thumbnail.short_description = _('Icon')

    class Meta:
        ordering = ("title", "id")
        verbose_name = ungettext_lazy(
            'Icon for cluster', 'Icons for clusters', 5)
        verbose_name_plural = ungettext_lazy(
            'Icon for cluster', 'Icons for clusters', 2)

    def __init__(self, *args, **kwargs):
        super(CustomClusterIcon, self).__init__(*args, **kwargs)
        self.__old_image = self.svg

    def save(self, *args, **kwargs):
        self.slug = slugify("{}".format(self.title))
        old_image = self.__old_image
        new_image = self.svg
        if not bool(old_image) or (bool(old_image) and bool(new_image) and
                                   old_image.name != new_image.name):
            self.__old_image = new_image
            self.size_width = 0
            self.size_height = 0
            self.offset_x = Decimal(".0")
            self.offset_y = Decimal(".0")
        super(CustomClusterIcon, self).save(*args, **kwargs)

    def get_size(self):
        return '[{0},{1}]'.format(self.size_width, self.size_height)

    def get_offset(self):
        return '[{0:f},{1:f}]'.format(self.offset_x, self.offset_y)


class IconCollection(models.Model):
    """Icon collection"""

    title = models.CharField(
        _('Collection name'),
        max_length=60,
        default="",
        unique=True,
        help_text=_('Example: Light golden Avocado'))

    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(IconCollection, self).save(*args, **kwargs)

    def admin_thumbnail(self):
        icon = self.icons.all().first()
        if icon is not None:
            return mark_safe('<img src="{0}" height="{1}" alt="Icon">'
                             .format(icon.svg.url, DJEYM_YMAPS_ICONS_MAX_SIZE))
        else:
            return ""
    admin_thumbnail.short_description = _('Sample Icon')

    class Meta:
        ordering = ("title", "id")
        verbose_name = ungettext_lazy('Icon collection for markers',
                                      'Icon collections for markers', 5)
        verbose_name_plural = _('Icon collections for markers')

    def get_icon_count(self):
        return self.icons.all().count()
    get_icon_count.short_description = _('Icon count')

    def get_count_of_active_icons(self):
        return self.icons.filter(active=True).count()
    get_count_of_active_icons.short_description = _('Count of active icons')

    def get_export_file_btn(self):
        url = reverse('djeym:export_icon_collection',
                      kwargs={'slug': self.slug})
        return mark_safe('<a href="{0}" class="export_icon_collection_link">{1} '
                         '<div></div></a>'.format(url, _('Export Collection')))
    get_export_file_btn.short_description = _('Get a collection of icons')


class CustomMarkerIcon(models.Model):
    """Custom marker icon"""

    icon_collection = models.ForeignKey(
        IconCollection,
        verbose_name=_("Icon Collection"),
        related_name='icons',
        on_delete=models.CASCADE)

    title = models.CharField(
        _('Icon name'),
        max_length=60,
        default="",
        help_text=_('Example: Airport'))

    svg = models.FileField(
        _('Icon'),
        upload_to=make_upload_path,
        validators=[validate_svg],
        null=True,
        help_text=_('Only SVG files.'))

    size_width = models.PositiveSmallIntegerField(_('Icon width'), default=0)
    size_height = models.PositiveSmallIntegerField(_('Icon height'), default=0)

    offset_x = models.DecimalField(
        _('Offset by axis - X'),
        max_digits=3,
        decimal_places=1,
        default=Decimal(".0"),
        help_text=_('Left, right - First time is automatically calculated.'))

    offset_y = models.DecimalField(
        _('Offset by axis - Y'),
        max_digits=3,
        decimal_places=1,
        default=Decimal(".0"),
        help_text=_('Up, down - First time is automatically calculated.'))

    active = models.BooleanField(
        _('Active icon'),
        default=True,
        help_text=_("If the project uses 2-3 icons, "
                    "it makes sense to disable the rest to optimize the download."))

    slug = models.SlugField(max_length=255, blank=True, null=True)

    @property
    def upload_dir(self):
        return 'djeym_custom_icons'

    def __str__(self):
        return '{}'.format(self.title)

    def admin_thumbnail(self):
        if bool(self.svg):
            return mark_safe('<img src="{0}" height="{1}" alt="Icon">'
                             .format(self.svg.url, self.size_height))
        else:
            return ""
    admin_thumbnail.short_description = _('Icon')

    class Meta:
        ordering = ("title", "id")
        verbose_name = ungettext_lazy(
            'Icon for marker', 'Icons for markers', 5)
        verbose_name_plural = ungettext_lazy(
            'Icon for marker', 'Icons for markers', 2)

    def __init__(self, *args, **kwargs):
        super(CustomMarkerIcon, self).__init__(*args, **kwargs)
        self.__old_image = self.svg

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + "-" + self.icon_collection.title)
        old_image = self.__old_image
        new_image = self.svg
        if not bool(old_image) or (bool(old_image) and bool(new_image) and
                                   old_image.name != new_image.name):
            self.__old_image = new_image
            self.size_width = 0
            self.size_height = 0
            self.offset_x = Decimal(".0")
            self.offset_y = Decimal(".0")
        super(CustomMarkerIcon, self).save(*args, **kwargs)

    def clean(self):
        slug = slugify(self.title + "-" + self.icon_collection.title)
        icon_count = CustomMarkerIcon.objects.filter(slug=slug).count()
        if not bool(self.slug) and icon_count > 0:
            msg = _(
                'For the selected collection, there is already an icon with a similar name.')
            raise ValidationError({'title': msg})

    def get_collection_name(self):
        return "{}".format(self.icon_collection.title)
    get_collection_name.short_description = _('Collection name')

    def get_size(self):
        return '[{0},{1}]'.format(self.size_width, self.size_height)

    def get_offset(self):
        return '[{0:f},{1:f}]'.format(self.offset_x, self.offset_y)


class CounterID(models.Model):
    """Count of geo objects not a point type."""
    num_id = models.PositiveIntegerField('ID', default=1)


class Statistics(models.Model):
    """Statistics"""
    obj_type = models.CharField('Object type', max_length=255, default="")
    obj_id = models.PositiveIntegerField('Object ID', default=0)
    ip = models.GenericIPAddressField('IP-address', null=True)
    likes = models.BooleanField('Likes', default=False)
    timestamp = models.DateTimeField('Date and Time', default=timezone.now)

    def __str__(self):
        return '{}'.format(self.obj_type)

    class Meta:
        verbose_name = _('Record')
        verbose_name_plural = _('Statistics')


class LoadIndicator(models.Model):
    """Load Indicator"""
    svg = models.FileField(
        _('Icon'),
        upload_to=make_upload_path,
        validators=[validate_svg],
        null=True,
        help_text=_(
            'https://github.com/genkosta/django-editor-ymaps/blob/master/Spinner.zip')
    )

    title = models.CharField(_('Title'), unique=True,
                             max_length=60, default="")

    slug = models.SlugField(max_length=255, blank=True, null=True)

    @property
    def upload_dir(self):
        return 'djeym_load_indicators'

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ("title", "id")
        verbose_name = _('Load indicator')
        verbose_name_plural = _('Load indicators')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(LoadIndicator, self).save(*args, **kwargs)

    def clean(self):
        slug = slugify(self.title)
        if slug == 'default':
            msg = _('Default - Reserved name for the indicator. Choose another name.')
            raise ValidationError({'title': msg})

    def admin_thumbnail(self):
        if bool(self.svg):
            return mark_safe('<img src="{0}" height="60" alt="Icon">'.format(self.svg.url))
        else:
            return ""
    admin_thumbnail.short_description = _('Icon')


# Signals ------------------------------------------------------------------------------------------

def custom_icon_cluster_size_correction(instance, **kwargs):
    """
    Custom Cluster Icons - Size correction and offset correction.
    Пользовательская иконки кластера - Корректировка размера и коррекция смещения.
    """
    image = instance.svg
    size_width = instance.size_width
    size_height = instance.size_height

    if bool(image) and (size_width == 0 or size_height == 0):
        sizes_svg = get_size_from_svg(image)
        width = sizes_svg["width"]
        height = sizes_svg["height"]
        sizes = get_size_correction(width, height)
        width = sizes[0]
        height = sizes[1]

        instance.size_width = width
        instance.size_height = height

        instance.offset_x = ((Decimal(width) / Decimal(2))
                             .quantize(Decimal(".0"))) * Decimal(-1)
        instance.offset_y = ((Decimal(height) / Decimal(2))
                             .quantize(Decimal(".0"))) * Decimal(-1)
        instance.save()


def custom_icon_marker_size_correction(instance, **kwargs):
    """
    Custom Marker Icon - Size correction and offset correction.
    Пользовательская иконка маркера - Корректировка размера и коррекция смещения.
    """
    image = instance.svg
    size_width = instance.size_width
    size_height = instance.size_height

    if bool(image) and (size_width == 0 or size_height == 0):
        sizes_svg = get_size_from_svg(image)
        width = sizes_svg["width"]
        height = sizes_svg["height"]
        sizes = get_size_correction(width, height)
        width = sizes[0]
        height = sizes[1]

        instance.size_width = width
        instance.size_height = height

        instance.offset_x = ((Decimal(width) / Decimal(2))
                             .quantize(Decimal(".0"))) * Decimal(-1)
        instance.offset_y = Decimal(height) * Decimal(-1)

        instance.save()


def placemark_update_json_code(instance, **kwargs):
    """Update json code in Placemark"""
    primary_json_code = json.loads(instance.json_code)
    json_code = json.loads(instance.json_code)

    if primary_json_code["id"] == 0:
        primary_json_code["id"] = instance.id
        json_code["id"] = instance.id

    primary_json_code = json.dumps(primary_json_code, ensure_ascii=False)
    json_code['geometry']['coordinates'] = json.loads(instance.coordinates)
    json_code["properties"]["id"] = instance.id
    json_code["properties"]["categoryID"] = instance.category.id
    json_code["properties"]["subCategoryIDs"] = [
        item.id for item in instance.subcategories.all()]
    json_code["properties"]["iconName"] = instance.icon_name
    icon_marker = CustomMarkerIcon.objects.get(slug=instance.icon_name)
    json_code["options"]['iconImageHref'] = icon_marker.svg.url
    json_code["options"]['iconImageSize'] = json.loads(icon_marker.get_size())
    json_code["options"]['iconImageOffset'] = json.loads(
        icon_marker.get_offset())
    json_code = json.dumps(json_code, ensure_ascii=False)

    if primary_json_code != json_code:
        instance.json_code = json_code
        instance.save()


def polyline_update_json_code(instance, **kwargs):
    """Update json code in Polyline"""
    primary_json_code = json.loads(instance.json_code)
    json_code = json.loads(instance.json_code)

    if primary_json_code["id"] == 0:
        counter_id = CounterID.objects.first()

        if counter_id is None:
            counter_id = CounterID.objects.create()

        num_id = counter_id.num_id
        primary_json_code["id"] = num_id
        json_code["id"] = num_id
        counter_id.num_id += 1
        counter_id.save()

    primary_json_code = json.dumps(primary_json_code, ensure_ascii=False)
    json_code['geometry']['coordinates'] = json.loads(instance.coordinates)
    json_code["properties"]["id"] = instance.pk
    json_code["properties"]["categoryID"] = instance.category.id
    json_code["options"]["strokeWidth"] = float(instance.stroke_width)
    json_code["options"]["strokeColor"] = instance.stroke_color
    json_code["options"]["strokeOpacity"] = float(instance.stroke_opacity)
    json_code = json.dumps(json_code, ensure_ascii=False)

    if primary_json_code != json_code:
        instance.json_code = json_code
        instance.save()


def polygon_update_json_code(instance, **kwargs):
    """Update json code in Polygon"""
    primary_json_code = json.loads(instance.json_code)
    json_code = json.loads(instance.json_code)

    if primary_json_code["id"] == 0:
        counter_id = CounterID.objects.first()

        if counter_id is None:
            counter_id = CounterID.objects.create()

        num_id = counter_id.num_id
        primary_json_code["id"] = num_id
        json_code["id"] = num_id
        counter_id.num_id += 1
        counter_id.save()

    primary_json_code = json.dumps(primary_json_code, ensure_ascii=False)
    json_code['geometry']['coordinates'] = json.loads(instance.coordinates)
    json_code["properties"]["id"] = instance.pk
    json_code["properties"]["categoryID"] = instance.category.pk
    json_code["options"]["strokeWidth"] = float(instance.stroke_width)
    json_code["options"]["strokeColor"] = instance.stroke_color
    json_code["options"]["strokeOpacity"] = float(instance.stroke_opacity)
    json_code["options"]["fillColor"] = instance.fill_color
    json_code["options"]["fillOpacity"] = float(instance.fill_opacity)
    json_code = json.dumps(json_code, ensure_ascii=False)

    if primary_json_code != json_code:
        instance.json_code = json_code
        instance.save()


def heatpoint_update_json_code(instance, **kwargs):
    """Update json code in HeatPoint"""
    primary_json_code = json.loads(instance.json_code)
    json_code = json.loads(instance.json_code)

    if primary_json_code["id"] == 0:
        primary_json_code["id"] = instance.id
        json_code["id"] = instance.id

    primary_json_code = json.dumps(primary_json_code, ensure_ascii=False)
    json_code['geometry']['coordinates'] = json.loads(instance.coordinates)
    json_code["properties"]["weight"] = int(instance.weight)
    json_code = json.dumps(json_code, ensure_ascii=False)

    if primary_json_code != json_code:
        instance.json_code = json_code
        instance.save()


def placemark_delete_statistics(instance, **kwargs):
    """Delete orphaned statistics - Placemark"""
    Statistics.objects.filter(obj_type='Point', obj_id=instance.pk).delete()


def polyline_delete_statistics(instance, **kwargs):
    """Delete orphaned statistics - Polyline"""
    Statistics.objects.filter(obj_type='LineString',
                              obj_id=instance.pk).delete()


def polygon_delete_statistics(instance, **kwargs):
    """Delete orphaned statistics - Polygon"""
    Statistics.objects.filter(obj_type='Polygon', obj_id=instance.pk).delete()


# Resize icons
post_save.connect(custom_icon_cluster_size_correction,
                  sender=CustomClusterIcon)
post_save.connect(custom_icon_marker_size_correction, sender=CustomMarkerIcon)

# Update json code
post_save.connect(placemark_update_json_code, sender=Placemark)
m2m_changed.connect(placemark_update_json_code,
                    sender=Placemark.subcategories.through)
post_save.connect(polyline_update_json_code, sender=Polyline)
post_save.connect(polygon_update_json_code, sender=Polygon)
post_save.connect(heatpoint_update_json_code, sender=HeatPoint)

# Clean old icons
pre_save.connect(cleaning_files_pre_save, sender=CustomClusterIcon)
pre_delete.connect(cleaning_files_pre_delete, sender=CustomClusterIcon)
pre_save.connect(cleaning_files_pre_save, sender=CustomMarkerIcon)
pre_delete.connect(cleaning_files_pre_delete, sender=CustomMarkerIcon)
pre_save.connect(cleaning_files_pre_save, sender=LoadIndicator)
pre_delete.connect(cleaning_files_pre_delete, sender=LoadIndicator)

# Clean old screenshots
pre_save.connect(cleaning_files_pre_save, sender=TileSource)
pre_delete.connect(cleaning_files_pre_delete, sender=TileSource)

# Delete orphaned presets
pre_delete.connect(placemark_delete_statistics, sender=Placemark)
pre_delete.connect(polyline_delete_statistics, sender=Polyline)
pre_delete.connect(polygon_delete_statistics, sender=Polygon)
