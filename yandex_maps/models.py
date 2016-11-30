# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from slugify import slugify
from django.core.urlresolvers import reverse
import re
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit
from decimal import Decimal, Context, localcontext
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField

from .utils import validate_image, make_upload_path


@python_2_unicode_compatible
class Map(models.Model):

    ZOOM_CHOICES = []

    for num in range(0, 19):
        ZOOM_CHOICES.append((num, num))

    title = models.CharField(_('Title'), max_length=60, unique=True)
    latitude = models.CharField(_('Latitude'), max_length=20, default='0', help_text=_('Latitude center of the map'))
    longitude = models.CharField(_('Longitude'), max_length=20, default='0',
                                 help_text=_('Longitude center of the map'))
    image = models.ImageField(_('Custom icon for cluster'), upload_to=make_upload_path, validators=[validate_image],
                              blank=True, null=True)

    size_x = models.DecimalField(_('Size X'), max_digits=4, decimal_places=2, default=Decimal(0.0),
                                 help_text=_('Width - First time is automatically calculated.'))

    size_y = models.DecimalField(_('Size Y'), max_digits=4,  decimal_places=2, default=Decimal(0.0),
                                 help_text=_('Height - First time is automatically calculated.'))

    offset_x = models.DecimalField(_('Offset X'), max_digits=4, decimal_places=2, default=Decimal(0.0),
                                   help_text=_('Left, right - First time is automatically calculated.'))

    offset_y = models.DecimalField(_('Offset Y'), max_digits=4, decimal_places=2, default=Decimal(0.0),
                                   help_text=_('Up, down - First time is automatically calculated.'))
    slug = models.SlugField(unique=True,  blank=True, null=True)
    active = models.BooleanField(_('Active map'), default=True)

    zoom = models.PositiveIntegerField(_('Zoom'), choices=ZOOM_CHOICES, default=3)
    icon = models.CharField(_('Standard icon for cluster'), max_length=50, default='islands#blueClusterIcons')
    color = models.CharField(_('Color cluster'), max_length=7, default='#1e98ff',
                             help_text=_('Only for standard icons'))

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    @property
    def upload_dir(self):
        return 'custom_cluster_icons_ymap'

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['id']
        verbose_name = _('Map')
        verbose_name_plural = _('Maps')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Map, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('yandex_maps:map', args=(self.slug,))

    def get_coordinates(self):
        return '[{0},{1}]'.format(self.latitude, self.longitude)

    def get_size(self):
        return '[{0},{1}]'.format(self.size_x, self.size_y)

    def get_offset(self):
        return '[{0},{1}]'.format(self.offset_x, self.offset_y)


@python_2_unicode_compatible
class CategoryPlacemark(models.Model):
    map = models.ForeignKey(Map, verbose_name=_('Map'), related_name='category_placemark')
    title = models.CharField(_('Title'), max_length=60, unique=True, help_text=_('Example: Name of district city'))
    active = models.BooleanField(_('Active category'), default=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
        verbose_name = _('Category of placemark')
        verbose_name_plural = _('Categories of placemarks')


@python_2_unicode_compatible
class SubCategoryPlacemark(models.Model):
    map = models.ForeignKey(Map, verbose_name=_('Map'), related_name='subcategory', null=True)
    title = models.CharField(_('Title'), max_length=60, unique=True, help_text=_('Example: Shops, banks, cafes, ...'))
    active = models.BooleanField(_('Active category'), default=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
        verbose_name = _('Subcategory of placemark')
        verbose_name_plural = _('Subcategories of placemarks')


@python_2_unicode_compatible
class CategoryPolyline(models.Model):
    map = models.ForeignKey(Map, verbose_name=_('Map'), related_name='category_polyline')
    title = models.CharField(_('Title'), max_length=60, unique=True)
    active = models.BooleanField(_('Active category'), default=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
        verbose_name = _('Category of route')
        verbose_name_plural = _('Categories of routes')


@python_2_unicode_compatible
class CategoryPolygon(models.Model):
    map = models.ForeignKey(Map, verbose_name=_('Map'), related_name='category_polygon')
    title = models.CharField(_('Title'), max_length=60, unique=True)
    active = models.BooleanField(_('Active category'), default=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
        verbose_name = _('Category of territory')
        verbose_name_plural = _('Categories of territories')


@python_2_unicode_compatible
class Placemark(models.Model):
    map = models.ForeignKey(Map, verbose_name=_('Map'), related_name='placemark_map')

    category = ChainedForeignKey(CategoryPlacemark,
                                 verbose_name=_('Category'),
                                 related_name='placemark_category',
                                 chained_field='map',
                                 chained_model_field='map',
                                 show_all=False,
                                 auto_choose=True
                                 )
    subcategory = ChainedManyToManyField(SubCategoryPlacemark,
                                         verbose_name=_('Subcategory'),
                                         related_name='placemark_subcategory',
                                         chained_field='map',
                                         chained_model_field='map'
                                         )
    icon_content = models.CharField(_('Text on icon'), max_length=60, blank=True, default='')
    hint_content = models.TextField(_('Hint'), default='', max_length=255, unique=True)
    balloon_content = models.TextField(_('Extended information'), blank=True, default='')
    icon_name = models.CharField(_('Icon name'), max_length=50, default='islands#blueHomeIcon')
    color = models.CharField(_('Color'), max_length=7, default='#1e98ff')
    coordinates = models.CharField(_('Coordinates'), max_length=60, default='[0.0,0.0]')
    active = models.BooleanField(_('Active placemark'), default=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        pattern = re.compile(r'<.*?>|&.*?;')
        return '{}'.format(pattern.sub('', self.hint_content))

    class Meta:
        ordering = ['-id']
        verbose_name = _('Placemark')
        verbose_name_plural = _('Placemarks')

    def get_subcategory(self):
        return ' , '.join([c.title for c in self.subcategory.all()])
    get_subcategory.short_description = _('Subcategories')


@python_2_unicode_compatible
class Polyline(models.Model):

    STROKE_OPACITY_CHOICES = []

    for num in reversed([str(x * 0.1) for x in range(1, 11)]):
        STROKE_OPACITY_CHOICES.append((num, num))

    map = models.ForeignKey(Map, verbose_name=_('Map'), related_name='polyline_map')

    category = ChainedForeignKey(CategoryPolyline,
                                 verbose_name=_('Category'),
                                 related_name='polyline_category',
                                 chained_field='map',
                                 chained_model_field='map',
                                 show_all=False,
                                 auto_choose=True
                                 )
    hint_content = models.TextField(_('Route name'), default='', max_length=255, unique=True)
    balloon_content = models.TextField(_('Extended information'), blank=True, default='')
    stroke_width = models.PositiveIntegerField(_('Stroke width'), default=5)
    stroke_color = models.CharField(_('Line color'), max_length=7, default='#1e98ff')
    stroke_opacity = models.CharField(_('Opacity line'), max_length=3, choices=STROKE_OPACITY_CHOICES, default='1.0')
    coordinates = models.TextField(_('Coordinates'), default='')
    active = models.BooleanField(_('Active route'), default=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        pattern = re.compile(r'<.*?>|&.*?;')
        return '{}'.format(pattern.sub('', self.hint_content))

    class Meta:
        ordering = ['-id']
        verbose_name = _('Route')
        verbose_name_plural = _('Routes')


@python_2_unicode_compatible
class Polygon(models.Model):

    STROKE_OPACITY_CHOICES = []

    for num in reversed([str(x * 0.1) for x in range(1, 11)]):
        STROKE_OPACITY_CHOICES.append((num, num))

    map = models.ForeignKey(Map, verbose_name=_('Map'), related_name='polygon_map')
    category = ChainedForeignKey(CategoryPolygon,
                                 verbose_name=_('Category'),
                                 related_name='polygon_category',
                                 chained_field='map',
                                 chained_model_field='map',
                                 show_all=False,
                                 auto_choose=True
                                 )
    hint_content = models.TextField(_('Name of territory'), default='', max_length=255, unique=True)
    balloon_content = models.TextField(_('Extended information'), blank=True, default='',)
    stroke_width = models.PositiveIntegerField(_('Stroke width'), default=2)
    stroke_color = models.CharField(_('Line color'), max_length=7, default='#1e98ff')
    stroke_opacity = models.CharField(_('Opacity line'), max_length=3, choices=STROKE_OPACITY_CHOICES, default='1.0')
    fill_color = models.CharField(_('Fill color'), max_length=7, default='#1e98ff')
    fill_opacity = models.CharField(_('Fill opacity'), max_length=3, choices=STROKE_OPACITY_CHOICES, default='1.0')
    coordinates = models.TextField(_('Coordinates'), default='')
    active = models.BooleanField(_('Active territory'), default=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        pattern = re.compile(r'<.*?>|&.*?;')
        return '{}'.format(pattern.sub('', self.hint_content))

    class Meta:
        ordering = ['-id']
        verbose_name = _('Territory')
        verbose_name_plural = _('Territories')


@python_2_unicode_compatible
class CustomIcon(models.Model):
    title = models.CharField(_('Title'), max_length=30, default='', unique=True)
    image = models.ImageField(_('Image'), upload_to=make_upload_path, validators=[validate_image])

    size_x = models.DecimalField(_('Size X'), max_digits=4, decimal_places=2, default=Decimal(0.0),
                                 help_text=_('Width - First time is automatically calculated.'))

    size_y = models.DecimalField(_('Size Y'), max_digits=4, decimal_places=2, default=Decimal(0.0),
                                 help_text=_('Height - First time is automatically calculated.'))

    offset_x = models.DecimalField(_('Offset X'), max_digits=4, decimal_places=2, default=Decimal(0.0),
                                   help_text=_('Left, right - First time is automatically calculated.'))

    offset_y = models.DecimalField(_('Offset Y'), max_digits=4, decimal_places=2, default=Decimal(0.0),
                                   help_text=_('Up, down - First time is automatically calculated.'))

    active = models.BooleanField(_('Active icon'), default=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    thumbnail = ImageSpecField([ResizeToFit(height=60, upscale=True)], source='image')

    @property
    def upload_dir(self):
        return 'custom_icons_ymap'

    def __str__(self):
        return '{}'.format(self.title)

    def admin_thumbnail(self):
        if self.image:
            return '<img src="{}" />'.format(self.thumbnail.url)
        else:
            return ''
    admin_thumbnail.short_description = _('Image')
    admin_thumbnail.allow_tags = True

    def get_size(self):
        return '[{0},{1}]'.format(self.size_x, self.size_y)

    def get_offset(self):
        return '[{0},{1}]'.format(self.offset_x, self.offset_y)

    class Meta:
        ordering = ['id']
        verbose_name = _('Custom icon')
        verbose_name_plural = _('Custom icons')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(CustomIcon, self).save(*args, **kwargs)


# signals
def custom_icon_set_size(instance, **kwargs):

    if instance.size_x == Decimal(0.0) or instance.size_y == Decimal(0.0):

        instance.size_y = Decimal(instance.image.height) if Decimal(instance.image.height) < Decimal(61) else Decimal(60)
        instance.size_x = Decimal(instance.image.width) / (Decimal(instance.image.height) / instance.size_y)

        with localcontext(Context(4)):
            instance.size_x = instance.size_x.quantize(Decimal('0.00'))

        instance.offset_x = (instance.size_x / Decimal(2)) * Decimal(-1)
        instance.offset_y = instance.size_y * Decimal(-1)
        instance.save()


def map_set_icon(instance, **kwargs):

    color_icon = {
        '#82cdff': 'islands#lightBlueClusterIcons',
        '#1e98ff': 'islands#blueClusterIcons',
        '#177bc9': 'islands#darkBlueClusterIcons',
        '#0e4779': 'islands#nightClusterIcons',
        '#56db40': 'islands#greenClusterIcons',
        '#1bad03': 'islands#darkGreenClusterIcons',
        '#97a100': 'islands#oliveClusterIcons',
        '#595959': 'islands#blackClusterIcons',
        '#b3b3b3': 'islands#grayClusterIcons',
        '#f371d1': 'islands#pinkClusterIcons',
        '#b51eff': 'islands#violetClusterIcons',
        '#793d0e': 'islands#brownClusterIcons',
        '#ffd21e': 'islands#yellowClusterIcons',
        '#ff931e': 'islands#orangeClusterIcons',
        '#e6761b': 'islands#darkOrangeClusterIcons',
        '#ed4543': 'islands#redClusterIcons',
    }

    required_icon = color_icon[instance.color]

    if instance.icon != required_icon:
        instance.icon = required_icon
        instance.save()

    if instance.image and (instance.size_x == Decimal(0.0) or instance.size_y == Decimal(0.0)):

        instance.size_y = Decimal(instance.image.height) if Decimal(instance.image.height) < Decimal(61) else Decimal(60)
        instance.size_x = Decimal(instance.image.width) / (Decimal(instance.image.height) / instance.size_y)

        with localcontext(Context(4)):
            instance.size_x = instance.size_x.quantize(Decimal('0.00'))

        instance.offset_x = (instance.size_x / Decimal(2)) * Decimal(-1)
        instance.offset_y = (instance.size_y / Decimal(2)) * Decimal(-1)
        instance.save()

    elif not instance.image and (instance.size_x != Decimal(0.0) or instance.size_y != Decimal(0.0)):

        instance.size_x = Decimal(0.0)
        instance.size_y = Decimal(0.0)
        instance.offset_x = Decimal(0.0)
        instance.offset_y = Decimal(0.0)
        instance.save()


models.signals.post_save.connect(custom_icon_set_size,  sender=CustomIcon)
models.signals.post_save.connect(map_set_icon,  sender=Map)
