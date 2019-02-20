# -*- coding: utf-8 -*-
import math
import os
import re
import shutil
import uuid
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FileDescriptor, ImageFileDescriptor
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from lxml import etree

# Maximum size of icons for markers and clusters of Yandex maps.
# (Максимальный размер иконок для маркеров и кластеров Яндекс карт.)
DJEYM_YMAPS_ICONS_MAX_SIZE = 60


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


def validate_hex_color(color):
    if re.match(r'^#[0-9a-f]{3,8}$', color, re.I) is None:
        raise ValidationError(_('Color does not match the hex standard.'))


def get_icon_font_plugin():
    """Get plug-in files for icon font."""
    icons_default_bool = False
    ymaps_icons_for_categories_css = getattr(
        settings, 'DJEYM_YMAPS_ICONS_FOR_CATEGORIES_CSS', None)
    ymaps_icons_for_categories_js = getattr(
        settings, 'DJEYM_YMAPS_ICONS_FOR_CATEGORIES_JS', None)
    if not bool(ymaps_icons_for_categories_css) or not bool(ymaps_icons_for_categories_js):
        icons_default_bool = True
        ymaps_icons_for_categories_css = [
            '/static/djeym/plugins/fontawesome/css/all.min.css']
        ymaps_icons_for_categories_js = [
            '/static/djeym/plugins/fontawesome/js/all.min.js']
    return ymaps_icons_for_categories_css, ymaps_icons_for_categories_js, icons_default_bool


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


def make_upload_path(instance, filename):
    extension = Path(filename).suffix
    return os.path.join(instance.upload_dir, '{0}{1}'.format(uuid.uuid4(), extension))


def get_filename(filename):
    """CKEditor - Filename Generator"""
    extension = Path(filename).suffix
    return '{0}{1}'.format(uuid.uuid4(), extension)


def cleaning_files_pre_save(sender, instance, **kwargs):
    """Remove old files"""
    old_status = sender.objects.filter(pk=instance.pk)
    dir_name_list = dir(sender)

    if old_status:
        for dir_name in dir_name_list:
            field = getattr(sender, dir_name, None)

            if field and (isinstance(field, FileDescriptor) or
                          isinstance(field, ImageFileDescriptor) or
                          isinstance(field, ImageSpecField)):

                old_field = getattr(old_status[0], dir_name)
                updated_field = getattr(instance, dir_name)

                if getattr(old_field, 'name', None) != getattr(updated_field, 'name', None):

                    try:
                        path = getattr(old_field, 'path')

                        if path and os.path.exists(path):
                            if isinstance(field, ImageSpecField):
                                pattern = re.compile(
                                    r'(/[-_\w()]+\.[a-zA-Z]{3,4}$)')
                                shutil.rmtree(pattern.sub('', path))
                            else:
                                os.remove(path)
                    except (FileNotFoundError, ValueError):
                        pass


def cleaning_files_pre_delete(sender, instance, **kwargs):
    """Delete orphan files"""
    dir_name_list = dir(sender)

    for dir_name in dir_name_list:
        field = getattr(sender, dir_name, None)

        if field and (isinstance(field, FileDescriptor) or
                      isinstance(field, ImageFileDescriptor) or
                      isinstance(field, ImageSpecField)):

            target_field = getattr(instance, dir_name)

            try:
                path = getattr(target_field, 'path', None)

                if path and os.path.exists(path):
                    if isinstance(field, ImageSpecField):
                        pattern = re.compile(r'(/[-_\w()]+\.[a-zA-Z]{3,4}$)')
                        shutil.rmtree(pattern.sub('', path))
                    else:
                        os.remove(path)
            except (FileNotFoundError, ValueError):
                pass
