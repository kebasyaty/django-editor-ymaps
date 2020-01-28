# -*- coding: utf-8 -*-
import json
import re
from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

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

        instance.offset_x = ((Decimal(width) / Decimal(2))
                             .quantize(Decimal(".0"), ROUND_CEILING)) * Decimal(-1)
        instance.offset_y = ((Decimal(height) / Decimal(2))
                             .quantize(Decimal(".0"), ROUND_HALF_UP)) * Decimal(-1)
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

        instance.offset_x = ((Decimal(width) / Decimal(2))
                             .quantize(Decimal(".0"), ROUND_CEILING))
        instance.offset_y = Decimal(height) * Decimal(-1)

        if instance.offset_x.to_integral_exact() - instance.offset_x == 0.5:
            instance.offset_x += Decimal("0.1")
            instance.offset_x *= Decimal(-1)
        else:
            instance.offset_x *= Decimal(-1)

        instance.save()


def refresh_json_code(instance, **kwargs):
    """Refresh JSON-code if change Subcategories."""
    instance.save()


def placemark_delete_statistics(instance, **kwargs):
    """Placemark - Delete orphaned statistics"""
    apps.get_model('djeym', 'Statistics').objects.filter(
        obj_type='Point', obj_id=instance.pk).delete()


def polyline_delete_statistics(instance, **kwargs):
    """Polyline - Delete orphaned statistics"""
    apps.get_model('djeym', 'Statistics').objects.filter(obj_type='LineString',
                                                         obj_id=instance.pk).delete()


def polygon_delete_statistics(instance, **kwargs):
    """Polygon - Delete orphaned statistics"""
    apps.get_model('djeym', 'Statistics').objects.filter(
        obj_type='Polygon', obj_id=instance.pk).delete()


def refresh_icon(instance, **kwargs):
    """Refresh icon (slug) in placemarks after refreshing icon in MarkerIcon."""
    maps = apps.get_model('djeym', 'Map').objects.filter(
        icon_collection=instance.icon_collection)
    for map in maps:
        placemarks = apps.get_model('djeym', 'Placemark').objects.filter(
            ymap=map, icon_slug=instance.slug)
        for placemark in placemarks:
            placemark.save()


# Save all json settings
def save_json_settings(json_settings, editor):
    """Save all json settings"""
    generalSettings = editor['generalSettings']
    mapControls = editor['mapControls']
    heatmapSettings = editor['heatmapSettings']
    categories = editor['categories']
    gradient = heatmapSettings['panel2']['gradient']
    heatmap = {
        'isActive': heatmapSettings['panel1']['isActive'],
        'radius': heatmapSettings['panel2']['radius'],
        'dissipating': heatmapSettings['panel2']['dissipating'],
        'opacity': heatmapSettings['panel2']['opacity'],
        'intensity': heatmapSettings['panel2']['intensity'],
        'gradient': {
            'color1': gradient['color1'],
            'color2': gradient['color2'],
            'color3': gradient['color3'],
            'color4': gradient['color4']
        },
    }
    front = {
        'themeType': generalSettings['themeType'],
        'colorControls': generalSettings['colorControlsTheme'],
        'colorButtonsText': generalSettings['colorButtonsTextTheme'],
        'openPanel': generalSettings['controls']['panel3_71'][2]['isActive'],
        'widthPanel': generalSettings['controls']['panel3_71'][1]['widthPanelFront'],
        'mapCenter': editor['ymap']['mapCenter'],
        'mapZoom': editor['ymap']['mapZoom'],
        'cluster': editor['ymap']['cluster'],
        'activeControls': mapControls['activeControls'],
        'isSearchByOrganization': mapControls['controls'][2]['isActive'],
        'isRoundTheme': generalSettings['controls']['panel1_69'][0]['isActive'],
        'isPanorama': generalSettings['controls']['panel1_69'][1]['isActive'],
        'currentTile': editor['tileSources']['currentTile'],
        'heatmap': heatmap,
        'colorBackgroundCountObjects': generalSettings['colorBackgroundCountObjects'],
        'textColorCountObjects': generalSettings['textColorCountObjects'],
        'isClusterize': generalSettings['controls']['panel3_71'][0]['isActive'],
        'isIconContentLayout': generalSettings['controls']['panel1_69'][3]['isActive'],
        'balloonContentLayout': generalSettings['controls']['panel1_69'][2]['layout'],
        'сategoryIcons': [icon for icon in categories['tabIcons'].values()],
        'multiple': categories['multiple'],
        'filters': categories['filters'],
        'imgBgPanel': generalSettings['controls']['panel3_71'][3]['large'],
        'tinting': generalSettings['tintingPanelFront'],
        'hideGeoTypes': categories['hideGeoTypes'],
        'hideGroupNames': categories['hideGroupNames'],
        'centerGeoTypes': categories['centerGeoTypes'],
        'geoTypeNameMarker': categories['geoTypeNameMarker'],
        'geoTypeNameRoute': categories['geoTypeNameRoute'],
        'geoTypeNameTerritory': categories['geoTypeNameTerritory'],
        'groupNameCategories': categories['groupNameCategories'],
        'groupNameSubcategories': categories['groupNameSubcategories'],
        'controlsShape': categories['controlsShape'],
        'effectRipple': categories['effectRipple']
    }
    json_settings.editor = json.dumps(editor, ensure_ascii=False)
    json_settings.front = json.dumps(front, ensure_ascii=False)
    json_settings.save()


# Tile Sources - Add random subdomains. Add api key or access token.
def random_domain(source, apikey):
    """Tile Sources - Add random subdomains. Add api key or access token."""
    source = re.sub('\r?\n', "", source)
    count_elem = re.search(r'\[\[(.+)\]\]', source)

    if count_elem is not None:
        count_elem = len(eval(count_elem.group(0))[0])

    value = re.sub(r'\[(\[.+\])\]',
                   '" + \\1[ Math.round( Math.random() * {} ) ] + "'
                   .format(int(count_elem) - 1), source)
    if len(apikey) > 0:
        var_key = re.search(r'\{\{(.+)\}\}', value).group(0)
        clean_var_key = re.sub(r'{{|}}', "", var_key)
        value = value.replace(var_key, clean_var_key + apikey, 1)
    else:
        value = re.sub(r'\{\{.+\}\}', "", value)
    return value


def convert_all_settings_to_json(instance, **kwargs):
    """Converting and updating all settings of Maps to JSON."""

    class_name = instance.__class__.__name__
    is_map = class_name == 'Map'

    if is_map:
        ymaps = [instance]
    else:
        ymaps = apps.get_model('djeym', 'Map').objects.all()
        if class_name == 'MarkerIcon' and \
                ymaps.filter(icon_collection=instance.icon_collection).count() == 0:
            return
        elif class_name == 'GeneralSettings' \
                or class_name == 'Preset' \
                or class_name == 'MapControls' \
                or class_name == 'HeatmapSettings':
            try:
                ymaps = [ymaps.get(pk=instance.ymap.pk)]
            except ObjectDoesNotExist:
                ymaps = []

    for ymap in ymaps:
        if not hasattr(ymap, 'json_settings'):
            return

        json_settings = ymap.json_settings
        editor = json.loads(json_settings.editor)

        # Get Icon Collection
        if class_name == 'MarkerIcon' or is_map:
            icon_collection = ymap.icon_collection.icons.filter(active=True)
            icon_collection = [{
                'title': item.title,
                'slug': item.slug,
                'url': item.svg.url,
                'size': json.loads(item.get_size()),
                'offset': json.loads(item.get_offset())
            } for item in icon_collection]
            editor['iconCollection'] = icon_collection
            if not is_map:
                save_json_settings(json_settings, editor)
                continue

        # Get categories
        if bool(re.search(r'Category', class_name)) or is_map:
            default_filters = {
                'a': [],  # Categories of placemarks
                'b': [],  # Subcategories of placemarks
                'c': [],  # Categories of Routes
                'd': [],  # Subcategories of Routes
                'e': [],  # Categories of Territories
                'f': []  # Subcategories of Territories
            }

            if editor.get('categories') is None:
                categories = {
                    'multiple': True,
                    'tabIcons': {
                        'marker': 'mdi-map-marker',
                        'route': 'mdi-routes',
                        'territory': 'mdi-beach'
                    },
                    'centerGeoTypes': False,
                    'hideGeoTypes': False,
                    'geoTypeNameMarker': "",
                    'geoTypeNameRoute': "",
                    'geoTypeNameTerritory': "",
                    'hideGroupNames': False,
                    'groupNameCategories': "",
                    'groupNameSubcategories': "",
                    'controlsShape': 'shaped',
                    'effectRipple': True,
                    'filters': default_filters
                }
            else:
                categories = editor['categories']
                categories['filters'] = default_filters

            raw_categories = {
                'a': ymap.categories_placemark.filter(active=True),
                'b': ymap.subcategories_placemark.filter(active=True),
                'c': ymap.categories_polyline.filter(active=True),
                'd': ymap.subcategories_polyline.filter(active=True),
                'e': ymap.categories_polygon.filter(active=True),
                'f': ymap.subcategories_polygon.filter(active=True)
            }
            multiple = categories['multiple']
            flag = True

            for key, val in raw_categories.items():
                if bool(val):
                    lock = True
                    for item in val:
                        categories['filters'][key].append({
                            'id': item.pk,
                            'title': item.title,
                            'icon': item.category_icon,
                            'color': item.category_color,
                            'isActive': lock and flag
                        })
                        lock = multiple
                flag = not flag
            editor['categories'] = categories

        # Get tile sources
        if class_name == 'TileSource' or is_map:
            tile_list = [{
                'id': 0,
                'img': '{}djeym/img/default_tile.png'.format(settings.STATIC_URL),
                'title': 'Default',
                'maxZoom': 23,
                'isActive': not bool(ymap.tile)
            }]
            current_tile_id = ymap.tile.pk if bool(ymap.tile) else 0
            tiles = apps.get_model('djeym', 'TileSource').objects.all()
            current_tile = tiles.filter(pk=current_tile_id).first()
            if current_tile is not None:
                current_tile = {
                    'title': current_tile.title,
                    'maxZoom': current_tile.maxzoom,
                    'minZoom': current_tile.minzoom,
                    'copyrights': current_tile.copyrights,
                    'randomTileUrl': '"{}"'.format(random_domain(
                        current_tile.source, current_tile.apikey))
                }
            tile_list.extend(
                [{
                    'id': item.pk,
                    'img': item.middle.url,
                    'title': item.title,
                    'maxZoom': item.maxzoom,
                    'isActive': item.pk == current_tile_id
                } for item in tiles]
            )
            tile_sources = {
                'tiles': tile_list,
                'currentTile': current_tile
            }
            editor['tileSources'] = tile_sources
            if not is_map:
                save_json_settings(json_settings, editor)
                continue

        # Get general settings
        if class_name == 'GeneralSettings' or is_map:
            general_settings = ymap.general_settings
            general_settings = {
                'controls': {
                    'panel1_69': [
                        {'icon': 'mdi-alpha-t-circle-outline',
                            'isActive': general_settings.roundtheme},
                        {'icon': 'mdi-airplay',
                            'isActive': general_settings.panorama},
                        {'icon': 'mdi-comment-text-outline',
                            'layout': general_settings.cluster_layout},
                        {
                            'icon': 'mdi-alpha-s-circle-outline',
                            'count': None,
                            'isActive': general_settings.cluster_icon_content
                        },
                        {'icon': 'mdi-theme-light-dark', 'theme': None}
                    ],
                    'panel2_70': [
                        {'icon': 'mdi-chart-bubble',
                            'isActive': general_settings.clustering_edit},
                        {'icon': 'mdi-arrow-split-vertical',
                            'widthPanelEditor': general_settings.width_panel_editor}
                    ],
                    'panel3_71': [
                        {'icon': 'mdi-chart-bubble',
                            'isActive': general_settings.clustering_site},
                        {'icon': 'mdi-arrow-split-vertical',
                            'widthPanelFront': general_settings.width_panel_front},
                        {'icon': 'mdi-arrow-expand-right',
                         'isActive': general_settings.open_panel_front},
                        {'imgBgPanelFront': general_settings.img_bg_panel_front_thumb.url if
                         bool(general_settings.img_bg_panel_front) else None,
                         'large': general_settings.img_bg_panel_front_large.url if
                         bool(general_settings.img_bg_panel_front) else None},
                        {'icon': 'mdi-arrow-split-vertical',
                            'widthMapFront': general_settings.width_map_front},
                        {'icon': 'mdi-arrow-split-horizontal',
                            'heightMapFront': general_settings.height_map_front},
                    ]
                },
                'themeType': general_settings.theme_type,
                'colorControlsTheme': general_settings.controls_color,
                'colorButtonsTextTheme': general_settings.buttons_text_color,
                'colorBackgroundCountObjects': general_settings.cluster_icon_content_bg_color,
                'textColorCountObjects': general_settings.cluster_icon_content_txt_color,
                'tintingPanelFront': general_settings.tinting_panel_front
            }
            editor['generalSettings'] = general_settings
            if not is_map:
                save_json_settings(json_settings, editor)
                continue

        # Get Map controls
        if class_name == 'MapControls' or is_map:
            map_controls = ymap.map_controls
            map_controls = {
                'controls': [
                    {'img': settings.STATIC_URL + 'djeym/img/map_controls/geolocation.png',
                     'width': 96, 'isActive': map_controls.geolocation},
                    {'img': settings.STATIC_URL + 'djeym/img/map_controls/search.png',
                     'width': 264, 'isActive': map_controls.search},
                    {'img': settings.STATIC_URL + 'djeym/img/map_controls/provider.png',
                     'width': 335, 'isActive': map_controls.provider},
                    {'img': settings.STATIC_URL + 'djeym/img/map_controls/route.png',
                     'width': 339, 'isActive': map_controls.route},
                    {'img': settings.STATIC_URL + 'djeym/img/map_controls/traffic.png',
                     'width': 289, 'isActive': map_controls.traffic},
                    {'img': settings.STATIC_URL + 'djeym/img/map_controls/typeselector.png',
                     'width': 273, 'isActive': map_controls.typeselector},
                    {'img': settings.STATIC_URL + 'djeym/img/map_controls/fullscreen.png',
                     'width': 96, 'isActive': map_controls.fullscreen},
                    {'img': settings.STATIC_URL + 'djeym/img/map_controls/zoom.png',
                     'width': 99, 'isActive': map_controls.zoom},
                    {'img': settings.STATIC_URL + 'djeym/img/map_controls/ruler.png',
                     'width': 102, 'isActive': map_controls.ruler}
                ],
                'activeControls': map_controls.get_active_control_list()
            }
            editor['mapControls'] = map_controls
            if not is_map:
                save_json_settings(json_settings, editor)
                continue

        # Get Heatmap
        if class_name == 'HeatmapSettings' or is_map:
            heatmap_settings = ymap.heatmap_settings
            heatmap_settings = {
                'panel1': {'isActive': heatmap_settings.active},
                'panel2': {
                    'gradient': {
                        'color1': heatmap_settings.gradient_color1,
                        'color2': heatmap_settings.gradient_color2,
                        'color3': heatmap_settings.gradient_color3,
                        'color4': heatmap_settings.gradient_color4
                    },
                    'radius': heatmap_settings.radius,
                    'dissipating': heatmap_settings.dissipating,
                    'opacity': heatmap_settings.opacity,
                    'intensity': heatmap_settings.intensity
                }
            }
            editor['heatmapSettings'] = heatmap_settings
            if not is_map:
                save_json_settings(json_settings, editor)
                continue

        # Get load indicators
        if class_name == 'LoadIndicator' or is_map:
            load_indicators = apps.get_model(
                'djeym', 'LoadIndicator').objects.all()
            load_indicators = {
                'indicators': [{
                    'title': item.title,
                    'slug': item.slug,
                    'img': item.svg.url
                } for item in load_indicators],
                'size': ymap.load_indicator_size,
                'speed': ymap.animation_speed,
                'disableAnimation': ymap.disable_indicator_animation,
                'currentIndicator': ymap.load_indicator
                .slug if ymap.load_indicator is not None else ""
            }
            editor['loadIndicators'] = load_indicators
            if not is_map:
                save_json_settings(json_settings, editor)
                continue

        # Get Presets
        if class_name == 'Preset' or is_map:
            presets = ymap.presets.all()
            presets = [{
                'id': item.pk,
                'title': item.title,
                'icon': item.icon,
                'description': item.description,
                'autoheader': item.autoheader,
                'autobody': item.autobody,
                'autofooter': item.autofooter,
                'placemark': item.placemark,
                'polyline': item.polyline,
                'polygon': item.polygon,
                'position': item.position
            } for item in presets]
            editor['presets'] = presets
            if not is_map:
                save_json_settings(json_settings, editor)
                continue

        # Get settings for YMap and Cluster
        cluster = ymap.icon_cluster
        tmp_ymap = {
            'mapCenter': json.loads('[{0}, {1}]'.format(ymap.latitude, ymap.longitude)),
            'mapZoom': ymap.zoom,
            'cluster': {}
        }
        if cluster is not None:
            tmp_ymap['cluster'] = {
                'url': cluster.svg.url,
                'size': [cluster.size_width, cluster.size_height],
                'offset': json.loads('[{0:f}, {1:f}]'.format(
                    cluster.offset_x, cluster.offset_y))
            }
        editor['ymap'] = tmp_ymap

        # Save all json settings
        save_json_settings(json_settings, editor)
