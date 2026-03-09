"""Signals Func."""

from __future__ import annotations

from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal

from django.apps import apps

from .utils import get_size_correction, get_size_from_svg


def icon_cluster_size_correction(instance, **kwargs):
    """Cluster Icons - Size correction and offset correction."""
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

        instance.offset_x = ((Decimal(width) / Decimal(2)).quantize(Decimal(".0"), ROUND_CEILING)) * Decimal(-1)
        instance.offset_y = ((Decimal(height) / Decimal(2)).quantize(Decimal(".0"), ROUND_HALF_UP)) * Decimal(-1)
        instance.save()


def icon_marker_size_correction(instance, **kwargs):
    """Marker Icon - Size correction and offset correction."""
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

        instance.offset_x = (Decimal(width) / Decimal(2)).quantize(Decimal(".0"), ROUND_CEILING)
        instance.offset_y = Decimal(height) * Decimal(-1)

        if instance.offset_x.to_integral_exact() - instance.offset_x == Decimal("0.5"):
            instance.offset_x += Decimal("0.1")
            instance.offset_x *= Decimal(-1)
        else:
            instance.offset_x *= Decimal(-1)

        instance.save()


def refresh_json_code(instance, **kwargs):
    """Refresh JSON-code if change Subcategories."""
    instance.save()


def refresh_icon(instance, **kwargs):
    """Refresh icon (slug) in placemarks after refreshing icon in MarkerIcon."""
    maps = apps.get_model("djeym", "Map").objects.filter(icon_collection=instance.icon_collection)
    for map in maps:
        placemarks = apps.get_model("djeym", "Placemark").objects.filter(ymap=map, icon_slug=instance.slug)
        for placemark in placemarks:
            placemark.save()
