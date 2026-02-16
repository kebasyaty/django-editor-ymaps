"""Utils."""

from __future__ import annotations

import json
import math
import uuid
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from lxml import etree
from xloft import to_human_size

from .globals import DJEYM_YMAPS_ICONS_MAX_SIZE

# SIZE CORRECTION
# --------------------------------------------------------------------------------------------------


def get_size_correction(width, height):
    """Get size correction of image."""
    size_width, size_height = Decimal(width), Decimal(height)

    if size_width > DJEYM_YMAPS_ICONS_MAX_SIZE or size_height > DJEYM_YMAPS_ICONS_MAX_SIZE:
        size_width = math.ceil(size_width * (DJEYM_YMAPS_ICONS_MAX_SIZE / size_height))
        size_height = DJEYM_YMAPS_ICONS_MAX_SIZE
    return (size_width, size_height)


def get_size_from_svg(svg):
    """Get width and height from SVG file."""
    xml_content = Path(svg.path).read_bytes()
    root = etree.XML(xml_content)
    width = root.get("width")
    height = root.get("height")

    if width is None or height is None:
        view_box_list = root.get("viewBox").split(" ")
        width = view_box_list[2]
        height = view_box_list[3]

    return {"width": int(Decimal(width)), "height": int(Decimal(height))}


# VALIDATORS
# --------------------------------------------------------------------------------------------------


def validate_svg(svg):
    extension = Path(svg.name).suffix.lower()

    if extension != ".svg":
        raise ValidationError(_("Only SVG (file_name.svg) files."))

    if hasattr(svg, "temporary_file_path"):
        svg_path = svg.temporary_file_path()
    else:
        svg_path = BytesIO(svg.read()) if hasattr(svg, "read") else BytesIO(svg["content"])

    if bool(svg_path):
        xml_content = svg_path.read()
        try:
            root = etree.XML(xml_content)
        except etree.XMLSyntaxError as err:
            svg_path.close()
            raise ValidationError(
                _("This is an invalid SVG file. Open this file in the vector editor and try to fix it."),
            ) from err
        tag = root.tag
        if bool(tag):
            if root.get("viewBox") is None:
                svg_path.close()
                raise ValidationError(_("There are no `viewBox` attribute in the `svg` tag."))
        else:
            svg_path.close()
            raise ValidationError(
                _("This is an invalid SVG file. Open this file in the vector editor and try to fix it."),
            )
    else:
        svg_path.close()
        raise ValidationError(_("Unable to read file attributes. The file may be damaged."))


def validate_image(image):
    extension_list = [".jpg", ".jpeg", ".png"]
    size = image.size
    extension = Path(image.name).suffix.lower()
    max_size = 524288  # 0.5 MB

    if extension not in extension_list:
        raise ValidationError(_("Only JPG or PNG format files."))
    elif not size:  # noqa: RET506
        raise ValidationError(_("Image cannot be 0.0 MB."))
    elif size > max_size:
        err_msg = _("Maximum image size {}.").format(to_human_size(max_size))
        raise ValidationError(err_msg)


def validate_image_geo_object(image):
    extension_list = [".jpg", ".jpeg", ".png"]
    size = image.size
    extension = Path(image.name).suffix.lower()
    max_size = settings.MAX_SIZE_IMAGE_GEO_OBJECT

    if extension not in extension_list:
        raise ValidationError(_("Only JPG or PNG format files."))
    elif not size:  # noqa: RET506
        raise ValidationError(_("Image cannot be 0.0 MB."))
    elif size > max_size:
        err_msg = _("Maximum image size {}.").format(to_human_size(max_size))
        raise ValidationError(err_msg)


def validate_coordinates(coordinate):
    try:
        float(coordinate)
    except ValueError:
        raise ValidationError(_("To determine the coordinates a numeric value is required."))  # noqa: B904


def validate_transparency(coordinate):
    try:
        float(coordinate)
    except ValueError:
        raise ValidationError(_("To determine the transparency a numeric value is required."))  # noqa: B904


def get_errors_form(*args):
    err_dict = {}
    detail = ""

    for form in args:
        for item in list(form):
            if item.errors:
                err_dict[item.name] = True
                detail += f"{item.label}: {item.errors}<br>"
            else:
                err_dict[item.name] = False

    return {"err_dict": err_dict, "detail": detail}


# GET UPLOAD PATH
# --------------------------------------------------------------------------------------------------


def make_upload_path(instance, filename):
    extension = Path(filename).suffix
    return Path(instance.upload_dir) / f"{uuid.uuid4()}{extension}"


# REFRESH JSON-CODE
# --------------------------------------------------------------------------------------------------


def placemark_update_json_code(instance):
    """Refresh json code for Placemark."""
    json_code = json.loads(instance.json_code)

    if json_code["id"] == 0:
        json_code["id"] = instance.pk

    json_code["geometry"]["coordinates"] = json.loads(instance.coordinates)
    json_code["properties"]["id"] = instance.pk
    json_code["properties"]["categoryID"] = instance.category.pk
    json_code["properties"]["subCategoryIDs"] = list(instance.subcategories.all().values_list("pk", flat=True))
    json_code["properties"]["iconSlug"] = instance.icon_slug

    if instance.icon_slug != "djeym-marker-default":
        icon_collection = instance.ymap.icon_collection
        icon_marker = apps.get_model("djeym", "MarkerIcon").objects.get(
            icon_collection=icon_collection,
            slug=instance.icon_slug,
        )
        json_code["options"]["iconImageHref"] = icon_marker.svg.url
        json_code["options"]["iconImageSize"] = json.loads(icon_marker.get_size())
        json_code["options"]["iconImageOffset"] = json.loads(icon_marker.get_offset())
    else:
        json_code["options"]["iconImageHref"] = static("djeym/img/center.svg")
        json_code["options"]["iconImageSize"] = [32, 60]
        json_code["options"]["iconImageOffset"] = [-16, -60]
    return json.dumps(json_code, ensure_ascii=False)


def polyline_update_json_code(instance):
    """Refresh json code for Polyline."""
    json_code = json.loads(instance.json_code)

    if json_code["id"] == 0:
        json_code["id"] = instance.pk

    json_code["geometry"]["coordinates"] = json.loads(instance.coordinates)
    json_code["properties"]["id"] = instance.pk
    json_code["properties"]["categoryID"] = instance.category.pk
    json_code["properties"]["subCategoryIDs"] = list(instance.subcategories.all().values_list("pk", flat=True))
    json_code["options"]["strokeWidth"] = float(instance.stroke_width)
    json_code["options"]["strokeColor"] = instance.stroke_color
    json_code["options"]["strokeStyle"] = instance.stroke_style
    json_code["options"]["strokeOpacity"] = float(instance.stroke_opacity)
    return json.dumps(json_code, ensure_ascii=False)


def polygon_update_json_code(instance):
    """Refresh json code for Polygon."""
    json_code = json.loads(instance.json_code)

    if json_code["id"] == 0:
        json_code["id"] = instance.pk

    json_code["geometry"]["coordinates"] = json.loads(instance.coordinates)
    json_code["properties"]["id"] = instance.pk
    json_code["properties"]["categoryID"] = instance.category.pk
    json_code["properties"]["subCategoryIDs"] = list(instance.subcategories.all().values_list("pk", flat=True))
    json_code["options"]["strokeWidth"] = float(instance.stroke_width)
    json_code["options"]["strokeColor"] = instance.stroke_color
    json_code["options"]["strokeStyle"] = instance.stroke_style
    json_code["options"]["strokeOpacity"] = float(instance.stroke_opacity)
    json_code["options"]["fillColor"] = instance.fill_color
    json_code["options"]["fillOpacity"] = float(instance.fill_opacity)
    return json.dumps(json_code, ensure_ascii=False)


def heatpoint_update_json_code(instance):
    """Refresh json code for HeatPoint."""
    json_code = json.loads(instance.json_code)

    if json_code["id"] == 0:
        json_code["id"] = instance.id

    json_code["geometry"]["coordinates"] = json.loads(instance.coordinates)
    json_code["properties"]["weight"] = int(instance.weight)
    return json.dumps(json_code, ensure_ascii=False)
