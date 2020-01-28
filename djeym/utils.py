# -*- coding: utf-8 -*-
import json
import math
import os
import re
import shutil
import uuid
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FileDescriptor, ImageFileDescriptor
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from lxml import etree

from .globals import DJEYM_YMAPS_ICONS_MAX_SIZE

# SIZE CORRECTION ----------------------------------------------------------------------------------


def get_size_correction(width, height):
    """Get size correction of image."""
    size_width, size_height = Decimal(width), Decimal(height)

    if size_width > DJEYM_YMAPS_ICONS_MAX_SIZE or size_height > DJEYM_YMAPS_ICONS_MAX_SIZE:
        size_width = math.ceil(
            (size_width * (DJEYM_YMAPS_ICONS_MAX_SIZE / size_height)))
        size_height = DJEYM_YMAPS_ICONS_MAX_SIZE
    return [size_width, size_height]


def get_size_from_svg(svg):
    """Get width and height from SVG file."""
    with open(svg.path, mode="rb") as svg_file:
        xml_content = svg_file.read()
        root = etree.XML(xml_content)
        result = {
            "width": int(Decimal(root.get('width'))),
            "height": int(Decimal(root.get('height')))
        }
    return result


# VALIDATORS ---------------------------------------------------------------------------------------

def validate_image(image):
    extension_list = ['.jpg', '.jpeg', '.png']
    size = image.size
    extension = Path(image.name).suffix.lower()

    if extension not in extension_list:
        raise ValidationError(_('Only JPG or PNG format files.'))
    elif not size:
        raise ValidationError(_('Image cannot be 0.0 mb.'))
    elif not size or size > 524288:
        raise ValidationError(_('Maximum image size 0.5 mb.'))


def validate_svg(svg):
    extension_list = ('.svg',)
    extension = Path(svg.name).suffix.lower()

    if extension not in extension_list:
        raise ValidationError(_('Only SVG (file_name.svg) files.'))

    if hasattr(svg, 'temporary_file_path'):
        svg_path = svg.temporary_file_path()
    else:
        if hasattr(svg, 'read'):
            svg_path = BytesIO(svg.read())
        else:
            svg_path = BytesIO(svg['content'])

    if bool(svg_path):
        xml_content = svg_path.read()
        try:
            root = etree.XML(xml_content)
        except etree.XMLSyntaxError:
            svg_path.close()
            raise ValidationError(_('This is an invalid SVG file. Open this file in '
                                    'the vector editor and try to fix it.'))
        tag = root.tag
        if bool(tag) and tag == "{http://www.w3.org/2000/svg}svg":
            if root.get('width') is not None and root.get('height') is not None:
                if root.get('viewBox') is None:
                    svg_path.close()
                    raise ValidationError(_('Missing viewBox attribute'))
            else:
                svg_path.close()
                raise ValidationError(
                    _('There are no width and height attributes in the SVG tag.'))
        else:
            svg_path.close()
            raise ValidationError(_('This is an invalid SVG file. Open this file in '
                                    'the vector editor and try to fix it.'))
    else:
        svg_path.close()
        raise ValidationError(
            _('Unable to read file attributes. The file may be damaged.'))


def validate_coordinates(coordinate):
    try:
        float(coordinate)
    except ValueError:
        raise ValidationError(
            _('To determine the coordinates a numeric value is required.'))


def validate_transparency(coordinate):
    try:
        float(coordinate)
    except ValueError:
        raise ValidationError(
            _('To determine the transparency a numeric value is required.'))


def get_errors_form(*args):
    err_dict = {}
    detail = ''

    for form in args:
        for item in list(form):
            if item.errors:
                err_dict[item.name] = True
                detail += u'{0}: {1}<br>'.format(item.label, item.errors)
            else:
                err_dict[item.name] = False

    return {'err_dict': err_dict, 'detail': detail}


# GET FILENAME -------------------------------------------------------------------------------------

def make_upload_path(instance, filename):
    extension = Path(filename).suffix
    return os.path.join(instance.upload_dir, '{0}{1}'.format(uuid.uuid4(), extension))


def get_filename(filename):
    """CKEditor - Filename Generator"""
    return re.sub(r'\s+', '_', filename).lower()


# CLEANING ORPHAN FILES ----------------------------------------------------------------------------

def cleaning_files_pre_save(sender, instance, **kwargs):
    """Remove old files"""
    old_status = sender.objects.filter(pk=instance.pk)
    dir_name_list = dir(sender)

    if old_status.count() > 0:
        for dir_name in dir_name_list:
            field = getattr(sender, dir_name, None)

            if bool(field) and (isinstance(field, FileDescriptor) or
                                isinstance(field, ImageFileDescriptor) or
                                isinstance(field, ImageSpecField)):

                old_field = getattr(old_status[0], dir_name, None)
                updated_field = getattr(instance, dir_name, None)

                if getattr(old_field, 'name', None) != \
                        getattr(updated_field, 'name', None):
                    try:
                        path = getattr(old_field, 'path', None)

                        if bool(path) and os.path.exists(path):
                            if isinstance(field, ImageSpecField):
                                pattern = re.compile(
                                    r'(/[-_\w()]+\.[a-zA-Z]{3,4}$)')
                                shutil.rmtree(pattern.sub('', path))
                            else:
                                os.remove(path)
                    except (FileNotFoundError, ValueError, TypeError):
                        pass


def cleaning_files_pre_delete(sender, instance, **kwargs):
    """Delete orphan files"""
    dir_name_list = dir(sender)

    for dir_name in dir_name_list:
        field = getattr(sender, dir_name, None)

        if bool(field) and (isinstance(field, FileDescriptor) or
                            isinstance(field, ImageFileDescriptor) or
                            isinstance(field, ImageSpecField)):

            target_field = getattr(instance, dir_name, None)

            try:
                path = getattr(target_field, 'path', None)

                if bool(path) and os.path.exists(path):
                    if isinstance(field, ImageSpecField):
                        pattern = re.compile(
                            r'(/[-_\w()]+\.[a-zA-Z]{3,4}$)')
                        shutil.rmtree(pattern.sub('', path))
                    else:
                        os.remove(path)
            except (FileNotFoundError, ValueError, TypeError):
                pass


# REFRESH JSON-CODE --------------------------------------------------------------------------------

def placemark_update_json_code(instance):
    """Refresh json code for Placemark"""
    json_code = json.loads(instance.json_code)

    if json_code["id"] == 0:
        json_code["id"] = instance.pk

    json_code['geometry']['coordinates'] = json.loads(instance.coordinates)
    json_code["properties"]["id"] = instance.pk
    json_code["properties"]["categoryID"] = instance.category.pk
    json_code["properties"]["subCategoryIDs"] = list(
        instance.subcategories.all().values_list('pk', flat=True))
    json_code["properties"]["iconSlug"] = instance.icon_slug

    if instance.icon_slug != 'djeym-marker-default':
        icon_collection = instance.ymap.icon_collection
        icon_marker = apps.get_model('djeym', 'MarkerIcon').objects.get(
            icon_collection=icon_collection, slug=instance.icon_slug)
        json_code["options"]['iconImageHref'] = icon_marker.svg.url
        json_code["options"]['iconImageSize'] = json.loads(
            icon_marker.get_size())
        json_code["options"]['iconImageOffset'] = json.loads(
            icon_marker.get_offset())
    else:
        json_code["options"]['iconImageHref'] = '/static/djeym/img/center.svg'
        json_code["options"]['iconImageSize'] = [32, 60]
        json_code["options"]['iconImageOffset'] = [-16, -60]
    return json.dumps(json_code, ensure_ascii=False)


def polyline_update_json_code(instance):
    """Refresh json code for Polyline"""
    json_code = json.loads(instance.json_code)

    if json_code["id"] == 0:
        json_code["id"] = instance.pk

    json_code['geometry']['coordinates'] = json.loads(instance.coordinates)
    json_code["properties"]["id"] = instance.pk
    json_code["properties"]["categoryID"] = instance.category.pk
    json_code["properties"]["subCategoryIDs"] = list(
        instance.subcategories.all().values_list('pk', flat=True))
    json_code["options"]["strokeWidth"] = float(instance.stroke_width)
    json_code["options"]["strokeColor"] = instance.stroke_color
    json_code["options"]["strokeStyle"] = instance.stroke_style
    json_code["options"]["strokeOpacity"] = float(instance.stroke_opacity)
    return json.dumps(json_code, ensure_ascii=False)


def polygon_update_json_code(instance):
    """Refresh json code for Polygon"""
    json_code = json.loads(instance.json_code)

    if json_code["id"] == 0:
        json_code["id"] = instance.pk

    json_code['geometry']['coordinates'] = json.loads(instance.coordinates)
    json_code["properties"]["id"] = instance.pk
    json_code["properties"]["categoryID"] = instance.category.pk
    json_code["properties"]["subCategoryIDs"] = list(
        instance.subcategories.all().values_list('pk', flat=True))
    json_code["options"]["strokeWidth"] = float(instance.stroke_width)
    json_code["options"]["strokeColor"] = instance.stroke_color
    json_code["options"]["strokeStyle"] = instance.stroke_style
    json_code["options"]["strokeOpacity"] = float(instance.stroke_opacity)
    json_code["options"]["fillColor"] = instance.fill_color
    json_code["options"]["fillOpacity"] = float(instance.fill_opacity)
    return json.dumps(json_code, ensure_ascii=False)


def heatpoint_update_json_code(instance):
    """Refresh json code for HeatPoint"""
    json_code = json.loads(instance.json_code)

    if json_code["id"] == 0:
        json_code["id"] = instance.id

    json_code['geometry']['coordinates'] = json.loads(instance.coordinates)
    json_code["properties"]["weight"] = int(instance.weight)
    return json.dumps(json_code, ensure_ascii=False)
