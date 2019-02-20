# -*- coding: utf-8 -*-
from decimal import Decimal

from django.test import TestCase

from .models import (CategoryPlacemark, CategoryPolygon, CategoryPolyline,
                     CounterID, CustomClusterIcon, CustomMarkerIcon,
                     ExternalModules, GeneralSettings, HeatmapSettings,
                     HeatPoint, IconCollection, Map, MapControls, Placemark,
                     Polygon, Polyline, Preset, Statistics,
                     SubCategoryPlacemark, TileSource)


class ModelsTest(TestCase):
    """
    Testing models - Integrity check on the default state.
    Тестирование моделей - Проверка целостности по дефолтному состоянию.
    """

    def setUp(self):
        # Map
        self.title_map = "Супермаркеты Харькова"
        self.slug_map = "supermarkety-kharkova"

        # CategoryPlacemark
        self.title_category_placemark_1 = "Шевченковский район"
        self.title_category_placemark_2 = "Холодногорский район"

        # SubCategoryPlacemark
        self.title_subcategory_placemark_1 = "Автопарковка"
        self.title_subcategory_placemark_2 = "Банкомат"

        # CategoryPolyline
        self.title_category_polyline_1 = "Маршруты марафонов"
        self.title_category_polyline_2 = "Туристические маршруты"

        # CategoryPolygon
        self.title_category_polygon_1 = "Ботанический Сад"
        self.title_category_polygon_2 = "Новобаварский район"

        # Placemark
        self.header_placemark_1 = "<p>Test placemark 1</p>"
        self.header_placemark_2 = "<p>Test placemark 2</p>"

        # Polyline
        self.header_polyline_1 = "<p>Test polyline 1</p>"
        self.header_polyline_2 = "<p>Test polyline 2</p>"

        # Polygon
        self.header_polygon_1 = "<p>Test polygon 1</p>"
        self.header_polygon_2 = "<p>Test polygon 2</p>"

        # CustomClusterIcon
        self.title_cluster_icon = "Test Cluster Icon"

        # IconCollection
        self.title_icon_collection = "Test Icon Collection"

        # CustomMarkerIcon
        self.custom_marker_icon_1 = "Test Custom Marker Icon 1"
        self.custom_marker_icon_2 = "Test Custom Marker Icon 2"

        # TileSource
        self.title_tile = "OpenTopoMap"

    def test_tile_source(self):
        """
        Test the model of the TileSource with the default settings.
        Тестирование модели TileSource с настройками по умолчанию.
        """
        title_tile = self.title_tile = "OpenTopoMap"
        test_tile = TileSource.objects.create(title=title_tile)

        self.assertTrue(TileSource._meta.get_field('title').unique)
        self.assertFalse(TileSource._meta.get_field('title').blank)
        self.assertEqual(TileSource._meta.get_field('title').default, "")

        self.assertFalse(TileSource._meta.get_field('maxzoom').blank)
        self.assertEqual(TileSource._meta.get_field('maxzoom').default, 12)

        self.assertFalse(TileSource._meta.get_field('minzoom').blank)
        self.assertEqual(TileSource._meta.get_field('minzoom').default, 0)

        self.assertFalse(TileSource._meta.get_field('source').blank)
        self.assertEqual(TileSource._meta.get_field('source').default, "")

        self.assertFalse(TileSource._meta.get_field('screenshot').blank)
        self.assertTrue(TileSource._meta.get_field('screenshot').null)

        self.assertTrue(TileSource._meta.get_field('copyrights').blank)
        self.assertEqual(TileSource._meta.get_field('copyrights').default, "")

        self.assertTrue(TileSource._meta.get_field('site').blank)
        self.assertEqual(TileSource._meta.get_field('site').default, "")

        self.assertTrue(TileSource._meta.get_field('apikey').blank)
        self.assertEqual(TileSource._meta.get_field('apikey').default, "")

        self.assertTrue(TileSource._meta.get_field('note').blank)
        self.assertEqual(TileSource._meta.get_field('note').default, "")

        self.assertTrue(TileSource._meta.get_field('slug').unique)
        self.assertTrue(TileSource._meta.get_field('slug').blank)
        self.assertTrue(TileSource._meta.get_field('slug').null)

        self.assertEqual(test_tile.upload_dir, "djeym_tile_screenshot")
        self.assertEqual(test_tile.__str__(), "OpenTopoMap")

        self.assertEqual(test_tile.title, "OpenTopoMap")
        self.assertEqual(test_tile.maxzoom, 12)
        self.assertEqual(test_tile.minzoom, 0)
        self.assertEqual(test_tile.source, "")
        self.assertEqual(bool(test_tile.screenshot), False)
        self.assertEqual(test_tile.copyrights, "")
        self.assertEqual(test_tile.site, "")
        self.assertEqual(test_tile.apikey, "")
        self.assertEqual(test_tile.note, "")
        self.assertEqual(test_tile.slug, "opentopomap")
        self.assertEqual(test_tile.admin_thumbnail(), "")

    def test_map_controls(self):
        """
        Test the model of the MapControls with the default settings.
        Тестирование модели MapControls с настройками по умолчанию.
        """
        test_map_controls = MapControls.objects.create()
        result = "['geolocationControl', 'searchControl', 'routeButtonControl'," \
                 " 'trafficControl', 'typeSelector', 'fullscreenControl'," \
                 " 'zoomControl', 'rulerControl']"

        self.assertEqual(MapControls._meta.get_field(
            'ymap').get_internal_type(), "OneToOneField")
        self.assertFalse(MapControls._meta.get_field('ymap').blank)
        self.assertTrue(MapControls._meta.get_field('ymap').null)

        self.assertFalse(MapControls._meta.get_field('geolocation').blank)
        self.assertTrue(MapControls._meta.get_field('geolocation').default)

        self.assertFalse(MapControls._meta.get_field('search').blank)
        self.assertTrue(MapControls._meta.get_field('search').default)

        self.assertFalse(MapControls._meta.get_field('provider').blank)
        self.assertTrue(MapControls._meta.get_field('provider').default)

        self.assertFalse(MapControls._meta.get_field('route').blank)
        self.assertTrue(MapControls._meta.get_field('route').default)

        self.assertFalse(MapControls._meta.get_field('traffic').blank)
        self.assertTrue(MapControls._meta.get_field('traffic').default)

        self.assertFalse(MapControls._meta.get_field('typeselector').blank)
        self.assertTrue(MapControls._meta.get_field('typeselector').default)

        self.assertFalse(MapControls._meta.get_field('fullscreen').blank)
        self.assertTrue(MapControls._meta.get_field('fullscreen').default)

        self.assertFalse(MapControls._meta.get_field('zoom').blank)
        self.assertTrue(MapControls._meta.get_field('zoom').default)

        self.assertFalse(MapControls._meta.get_field('ruler').blank)
        self.assertTrue(MapControls._meta.get_field('ruler').default)

        self.assertEqual(MapControls._meta.get_field(
            'maptype').get_internal_type(), 'CharField')
        self.assertFalse(MapControls._meta.get_field('maptype').blank)
        self.assertEqual(MapControls._meta.get_field('maptype').default, 'yandex#map')
        self.assertEqual(test_map_controls.maptype, 'yandex#map')

        self.assertEqual(test_map_controls.get_control_list(), result)

    def test_external_modules(self):
        """
        Test the model of the ExternalModules with the default settings.
        Тестирование модели ExternalModules с настройками по умолчанию.
        """
        test_external_modules = ExternalModules.objects.create()

        self.assertEqual(ExternalModules._meta.get_field(
            'ymap').get_internal_type(), "OneToOneField")
        self.assertFalse(ExternalModules._meta.get_field('ymap').blank)
        self.assertTrue(ExternalModules._meta.get_field('ymap').null)

        self.assertEqual(ExternalModules._meta.get_field(
            'roundtheme').get_internal_type(), 'BooleanField')
        self.assertFalse(ExternalModules._meta.get_field('roundtheme').blank)
        self.assertFalse(ExternalModules._meta.get_field('roundtheme').default)
        self.assertFalse(test_external_modules.roundtheme)

        self.assertEqual(ExternalModules._meta.get_field(
            'heatmap').get_internal_type(), 'BooleanField')
        self.assertFalse(ExternalModules._meta.get_field('heatmap').blank)
        self.assertFalse(ExternalModules._meta.get_field('heatmap').default)
        self.assertFalse(test_external_modules.heatmap)

        self.assertEqual(ExternalModules._meta.get_field(
            'areacalculation').get_internal_type(), 'BooleanField')
        self.assertFalse(ExternalModules._meta.get_field(
            'areacalculation').blank)
        self.assertTrue(ExternalModules._meta.get_field(
            'areacalculation').default)
        self.assertTrue(test_external_modules.areacalculation)

    def test_heatmap_settings(self):
        """
        Test the model of the HeatmapSettings with the default settings.
        Тестирование модели HeatmapSettings с настройками по умолчанию.
        """
        test_heatmap_settings = HeatmapSettings.objects.create()

        self.assertEqual(HeatmapSettings._meta.get_field(
            'ymap').get_internal_type(), 'OneToOneField')
        self.assertFalse(HeatmapSettings._meta.get_field('ymap').blank)
        self.assertTrue(HeatmapSettings._meta.get_field('ymap').null)

        self.assertEqual(HeatmapSettings._meta.get_field(
            'radius').get_internal_type(), 'PositiveIntegerField')
        self.assertFalse(HeatmapSettings._meta.get_field('radius').blank)
        self.assertEqual(HeatmapSettings._meta.get_field('radius').default, 10)
        self.assertEqual(test_heatmap_settings.radius, 10)

        self.assertEqual(HeatmapSettings._meta.get_field(
            'dissipating').get_internal_type(), 'BooleanField')
        self.assertFalse(HeatmapSettings._meta.get_field('dissipating').blank)
        self.assertFalse(
            HeatmapSettings._meta.get_field('dissipating').default)
        self.assertFalse(test_heatmap_settings.dissipating)

        self.assertEqual(HeatmapSettings._meta.get_field(
            'opacity').get_internal_type(), 'CharField')
        self.assertFalse(HeatmapSettings._meta.get_field('opacity').blank)
        self.assertEqual(HeatmapSettings._meta.get_field(
            'opacity').default, '0.8')
        self.assertEqual(test_heatmap_settings.opacity, '0.8')

        self.assertEqual(HeatmapSettings._meta.get_field(
            'intensity').get_internal_type(), 'CharField')
        self.assertFalse(HeatmapSettings._meta.get_field('intensity').blank)
        self.assertEqual(HeatmapSettings._meta.get_field(
            'intensity').default, '0.2')
        self.assertEqual(test_heatmap_settings.intensity, '0.2')

        self.assertEqual(HeatmapSettings._meta.get_field(
            'gradient_color1').get_internal_type(), 'CharField')
        self.assertFalse(HeatmapSettings._meta.get_field(
            'gradient_color1').blank)
        self.assertEqual(HeatmapSettings._meta.get_field(
            'gradient_color1').default, '#56db40b3')
        self.assertEqual(test_heatmap_settings.gradient_color1, '#56db40b3')

        self.assertEqual(HeatmapSettings._meta.get_field(
            'gradient_color2').get_internal_type(), 'CharField')
        self.assertFalse(HeatmapSettings._meta.get_field(
            'gradient_color2').blank)
        self.assertEqual(HeatmapSettings._meta.get_field(
            'gradient_color2').default, '#ffd21ecc')
        self.assertEqual(test_heatmap_settings.gradient_color2, '#ffd21ecc')

        self.assertEqual(HeatmapSettings._meta.get_field(
            'gradient_color3').get_internal_type(), 'CharField')
        self.assertFalse(HeatmapSettings._meta.get_field(
            'gradient_color3').blank)
        self.assertEqual(HeatmapSettings._meta.get_field(
            'gradient_color3').default, '#ed4543e6')
        self.assertEqual(test_heatmap_settings.gradient_color3, '#ed4543e6')

        self.assertEqual(HeatmapSettings._meta.get_field(
            'gradient_color4').get_internal_type(), 'CharField')
        self.assertFalse(HeatmapSettings._meta.get_field(
            'gradient_color4').blank)
        self.assertEqual(HeatmapSettings._meta.get_field(
            'gradient_color4').default, '#b22222')
        self.assertEqual(test_heatmap_settings.gradient_color4, '#b22222')

        self.assertIn(test_heatmap_settings.__str__(),
                      ('Settings', 'Настройки'))

    def test_heat_point(self):
        """
        Test the model of the HeatPoint with the default settings.
        Тестирование модели HeatPoint с настройками по умолчанию.
        """
        title_map = self.title_map
        text_json_1 = '{"type": "Feature", "id": 0, "geometry": {"type": "Point", ' \
                      '"coordinates": []}, "properties": {"weight": 0}}'
        text_json_2 = '{"type": "Feature", "id": 1, "geometry": {"type": "Point", ' \
                      '"coordinates": [0, 0]}, "properties": {"weight": 0}}'
        test_map = Map.objects.create(title=title_map)
        test_heat_point = HeatPoint.objects.create(ymap=test_map)

        self.assertEqual(HeatPoint._meta.get_field(
            'ymap').get_internal_type(), 'ForeignKey')
        self.assertFalse(HeatPoint._meta.get_field('ymap').blank)
        self.assertFalse(HeatPoint._meta.get_field('ymap').null)

        self.assertEqual(HeatPoint._meta.get_field(
            'title').get_internal_type(), 'CharField')
        self.assertTrue(HeatPoint._meta.get_field(
            'title').blank)
        self.assertEqual(HeatPoint._meta.get_field(
            'title').default, "")
        self.assertIn(test_heat_point.title,
                      ('Heat Point - 1', 'Тепловая точка - 1'))

        self.assertEqual(HeatPoint._meta.get_field(
            'weight').get_internal_type(), 'PositiveIntegerField')
        self.assertTrue(HeatPoint._meta.get_field(
            'weight').blank)
        self.assertEqual(HeatPoint._meta.get_field(
            'weight').default, 0)
        self.assertEqual(test_heat_point.weight, 0)

        self.assertEqual(HeatPoint._meta.get_field(
            'coordinates').get_internal_type(), 'CharField')
        self.assertFalse(HeatPoint._meta.get_field(
            'coordinates').blank)
        self.assertEqual(HeatPoint._meta.get_field(
            'coordinates').default, '[0,0]')
        self.assertEqual(test_heat_point.coordinates, '[0,0]')

        self.assertEqual(HeatPoint._meta.get_field(
            'active').get_internal_type(), 'BooleanField')
        self.assertFalse(HeatPoint._meta.get_field(
            'active').blank)
        self.assertTrue(HeatPoint._meta.get_field(
            'active').default)
        self.assertTrue(test_heat_point.active)

        self.assertEqual(HeatPoint._meta.get_field(
            'json_code').get_internal_type(), 'TextField')
        self.assertTrue(HeatPoint._meta.get_field(
            'json_code').blank)
        self.assertEqual(HeatPoint._meta.get_field(
            'json_code').default, text_json_1)
        self.assertEqual(test_heat_point.json_code, text_json_2)

        self.assertIn(test_heat_point.__str__(),
                      ('Heat Point - 1', 'Тепловая точка - 1'))

    def test_preset(self):
        """
        Test the model of the Preset with the default settings.
        Тестирование модели Preset с настройками по умолчанию.
        """
        title_map = self.title_map
        title = 'iPreset'
        ymap = Map.objects.create(title=title_map)
        preset = Preset.objects.create(ymap=ymap, title=title)

        self.assertEqual(Preset._meta.get_field(
            'title').get_internal_type(), 'CharField')
        self.assertEqual(Preset._meta.get_field(
            'title').max_length, 60)
        self.assertFalse(Preset._meta.get_field(
            'title').unique)
        self.assertFalse(Preset._meta.get_field(
            'title').blank)
        self.assertEqual(Preset._meta.get_field(
            'title').default, "")
        self.assertEqual(preset.title, title)

        self.assertEqual(Preset._meta.get_field(
            'icon').get_internal_type(), 'CharField')
        self.assertEqual(Preset._meta.get_field(
            'icon').max_length, 255)
        self.assertFalse(Preset._meta.get_field(
            'icon').unique)
        self.assertTrue(Preset._meta.get_field(
            'icon').blank)
        self.assertEqual(Preset._meta.get_field(
            'icon').default, '<i class="far fa-smile"></i>')
        self.assertEqual(preset.icon, '<i class="far fa-smile"></i>')

        self.assertEqual(Preset._meta.get_field(
            'html').get_internal_type(), 'TextField')
        self.assertFalse(Preset._meta.get_field(
            'html').unique)
        self.assertFalse(Preset._meta.get_field(
            'html').blank)
        self.assertEqual(Preset._meta.get_field(
            'html').default, '<p style="color:#e91e63;">iPreset</p>')
        self.assertEqual(preset.html, '<p style="color:#e91e63;">iPreset</p>')

        self.assertEqual(Preset._meta.get_field(
            'js').get_internal_type(), 'TextField')
        self.assertFalse(Preset._meta.get_field(
            'js').unique)
        self.assertTrue(Preset._meta.get_field(
            'js').blank)
        self.assertEqual(Preset._meta.get_field(
            'js').default, "")
        self.assertEqual(preset.js, "")

        self.assertEqual(Preset._meta.get_field(
            'description').get_internal_type(), 'TextField')
        self.assertFalse(Preset._meta.get_field(
            'description').unique)
        self.assertFalse(Preset._meta.get_field(
            'description').blank)
        self.assertEqual(Preset._meta.get_field(
            'description').default, """<div>Описание</div>
<div style="color:#607D8B;">Description</div>""")
        self.assertEqual(preset.description, """<div>Описание</div>
<div style="color:#607D8B;">Description</div>""")

        self.assertEqual(Preset._meta.get_field(
            'autoheader').get_internal_type(), 'BooleanField')
        self.assertFalse(Preset._meta.get_field(
            'autoheader').unique)
        self.assertFalse(Preset._meta.get_field(
            'autoheader').blank)
        self.assertFalse(Preset._meta.get_field(
            'autoheader').default)
        self.assertFalse(preset.autoheader)

        self.assertEqual(Preset._meta.get_field(
            'autobody').get_internal_type(), 'BooleanField')
        self.assertFalse(Preset._meta.get_field(
            'autobody').unique)
        self.assertFalse(Preset._meta.get_field(
            'autobody').blank)
        self.assertFalse(Preset._meta.get_field(
            'autobody').default)
        self.assertFalse(preset.autobody)

        self.assertEqual(Preset._meta.get_field(
            'autofooter').get_internal_type(), 'BooleanField')
        self.assertFalse(Preset._meta.get_field(
            'autofooter').unique)
        self.assertFalse(Preset._meta.get_field(
            'autofooter').blank)
        self.assertFalse(Preset._meta.get_field(
            'autofooter').default)
        self.assertFalse(preset.autofooter)

        self.assertEqual(Preset._meta.get_field(
            'placemark').get_internal_type(), 'BooleanField')
        self.assertFalse(Preset._meta.get_field(
            'placemark').unique)
        self.assertFalse(Preset._meta.get_field(
            'placemark').blank)
        self.assertTrue(Preset._meta.get_field(
            'placemark').default)
        self.assertTrue(preset.placemark)

        self.assertEqual(Preset._meta.get_field(
            'polyline').get_internal_type(), 'BooleanField')
        self.assertFalse(Preset._meta.get_field(
            'polyline').unique)
        self.assertFalse(Preset._meta.get_field(
            'polyline').blank)
        self.assertTrue(Preset._meta.get_field(
            'polyline').default)
        self.assertTrue(preset.polyline)

        self.assertEqual(Preset._meta.get_field(
            'polygon').get_internal_type(), 'BooleanField')
        self.assertFalse(Preset._meta.get_field(
            'polygon').unique)
        self.assertFalse(Preset._meta.get_field(
            'polygon').blank)
        self.assertTrue(Preset._meta.get_field(
            'polygon').default)
        self.assertTrue(preset.polygon)

        self.assertEqual(Preset._meta.get_field(
            'position').get_internal_type(), 'PositiveSmallIntegerField')
        self.assertFalse(Preset._meta.get_field(
            'position').unique)
        self.assertTrue(Preset._meta.get_field(
            'position').blank)
        self.assertEqual(Preset._meta.get_field(
            'position').default, 0)
        self.assertEqual(preset.position, 0)

    def test_general_settings(self):
        """
        Test the model of the GeneralSettings with the default settings.
        Тестирование модели GeneralSettings с настройками по умолчанию.
        """
        title_map = self.title_map
        ymap = Map.objects.create(title=title_map)
        general_settings = ymap.general_settings

        self.assertEqual(GeneralSettings._meta.get_field(
            'ymap').get_internal_type(), 'OneToOneField')
        self.assertFalse(GeneralSettings._meta.get_field('ymap').blank)
        self.assertTrue(GeneralSettings._meta.get_field('ymap').null)

        self.assertEqual(GeneralSettings._meta.get_field(
            'clustering_edit').get_internal_type(), 'BooleanField')
        self.assertFalse(GeneralSettings._meta.get_field(
            'clustering_edit').unique)
        self.assertFalse(GeneralSettings._meta.get_field(
            'clustering_edit').blank)
        self.assertTrue(GeneralSettings._meta.get_field(
            'clustering_edit').default)
        self.assertTrue(general_settings.clustering_edit)

        self.assertEqual(GeneralSettings._meta.get_field(
            'clustering_site').get_internal_type(), 'BooleanField')
        self.assertFalse(GeneralSettings._meta.get_field(
            'clustering_site').unique)
        self.assertFalse(GeneralSettings._meta.get_field(
            'clustering_site').blank)
        self.assertTrue(GeneralSettings._meta.get_field(
            'clustering_site').default)
        self.assertTrue(general_settings.clustering_site)

        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_layout').get_internal_type(), 'CharField')
        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_layout').max_length, 255)
        self.assertFalse(GeneralSettings._meta.get_field(
            'cluster_layout').unique)
        self.assertFalse(GeneralSettings._meta.get_field(
            'cluster_layout').blank)
        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_layout').default, "cluster#balloonTwoColumns")
        self.assertEqual(general_settings.cluster_layout,
                         "cluster#balloonTwoColumns")

        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_icon_content').get_internal_type(), 'BooleanField')
        self.assertFalse(GeneralSettings._meta.get_field(
            'cluster_icon_content').unique)
        self.assertFalse(GeneralSettings._meta.get_field(
            'cluster_icon_content').blank)
        self.assertTrue(GeneralSettings._meta.get_field(
            'cluster_icon_content').default)
        self.assertTrue(general_settings.cluster_icon_content)

        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_icon_content_bg_color').get_internal_type(), 'CharField')
        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_icon_content_bg_color').max_length, 255)
        self.assertFalse(GeneralSettings._meta.get_field(
            'cluster_icon_content_bg_color').unique)
        self.assertFalse(GeneralSettings._meta.get_field(
            'cluster_icon_content_bg_color').blank)
        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_icon_content_bg_color').default, "#ffffff")
        self.assertEqual(
            general_settings.cluster_icon_content_bg_color, "#ffffff")

        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_icon_content_txt_color').get_internal_type(), 'CharField')
        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_icon_content_txt_color').max_length, 255)
        self.assertFalse(GeneralSettings._meta.get_field(
            'cluster_icon_content_txt_color').unique)
        self.assertFalse(GeneralSettings._meta.get_field(
            'cluster_icon_content_txt_color').blank)
        self.assertEqual(GeneralSettings._meta.get_field(
            'cluster_icon_content_txt_color').default, "#333333")
        self.assertEqual(
            general_settings.cluster_icon_content_txt_color, "#333333")

        self.assertEqual(GeneralSettings._meta.get_field(
            'disable_site_panel').get_internal_type(), 'BooleanField')
        self.assertFalse(GeneralSettings._meta.get_field(
            'disable_site_panel').unique)
        self.assertFalse(GeneralSettings._meta.get_field(
            'disable_site_panel').blank)
        self.assertFalse(GeneralSettings._meta.get_field(
            'disable_site_panel').default)
        self.assertFalse(general_settings.disable_site_panel)

    def test_map(self):
        """
        Test the model of the Map with the default settings.
        Тестирование модели Map с настройками по умолчанию.
        """
        title_map = self.title_map
        test_map = Map.objects.create(title=title_map)

        self.assertTrue(Map._meta.get_field('title').unique)
        self.assertFalse(Map._meta.get_field('title').blank)

        self.assertFalse(Map._meta.get_field('icon_cluster').blank)
        self.assertTrue(Map._meta.get_field('icon_cluster').null)
        self.assertEqual(Map._meta.get_field('icon_cluster')
                         .get_internal_type(), "ForeignKey")

        self.assertFalse(Map._meta.get_field('icon_collection').blank)
        self.assertTrue(Map._meta.get_field('icon_collection').null)
        self.assertEqual(Map._meta.get_field('icon_collection')
                         .get_internal_type(), "ForeignKey")

        self.assertTrue(Map._meta.get_field('tile').blank)
        self.assertTrue(Map._meta.get_field('tile').null)
        self.assertEqual(Map._meta.get_field('tile')
                         .get_internal_type(), "ForeignKey")

        self.assertTrue(hasattr(test_map, 'controls'))

        self.assertEqual(test_map.title, title_map)
        self.assertEqual(test_map.latitude, "0")
        self.assertEqual(test_map.longitude, "0")
        self.assertFalse(bool(test_map.icon_collection))
        self.assertTrue(test_map.active)
        self.assertEqual(test_map.zoom, 3)
        self.assertEqual(test_map.slug, "supermarkety-kharkova")

        self.assertEqual(test_map.__str__(), title_map)

        self.assertEqual(Map._meta.ordering, ('title',))

        self.assertEqual(test_map.get_absolute_url(),
                         "/djeym/ymeditor/supermarkety-kharkova/")

        self.assertEqual(test_map.get_custom_cluster(), "")
        self.assertEqual(test_map.get_custom_marker_icon(), "")
        self.assertEqual(test_map.get_tile_screenshot(
        ), '<img src="/static/djeym/img/default_tile.png" height="60" alt="Screenshot">')

    def test_category_placemark(self):
        """
        Test the model of the CategoryPlacemark with the default settings.
        Тестирование модели CategoryPlacemark с настройками по умолчанию.
        """
        title_map = self.title_map
        title_category_placemark_1 = self.title_category_placemark_1
        title_category_placemark_2 = self.title_category_placemark_2

        test_map = Map.objects.create(title=title_map)
        category_1 = CategoryPlacemark.objects.create(
            ymap=test_map,
            title=title_category_placemark_1)
        category_2 = CategoryPlacemark.objects.create(
            ymap=test_map,
            title=title_category_placemark_2)

        self.assertEqual(test_map.category_placemark.count(), 2)
        self.assertEqual(CategoryPlacemark._meta.get_field('ymap')
                         .get_internal_type(), "ForeignKey")

        self.assertFalse(CategoryPlacemark._meta.get_field('title').unique)
        self.assertFalse(CategoryPlacemark._meta.get_field('title').blank)

        self.assertEqual(category_1.title, title_category_placemark_1)
        self.assertTrue(category_1.active)
        self.assertEqual(category_1.ymap.slug, test_map.slug)
        self.assertEqual(category_1.get_map_name(), test_map.title)
        self.assertEqual(category_1.get_title(), title_category_placemark_1)
        self.assertEqual(category_1.category_icon, "")
        self.assertEqual(category_1.category_color, "#00bfff")

        self.assertEqual(category_1.get_category_icon(), "")

        self.assertEqual(
            category_1.get_category_color(),
            "<div class=\"djeym_category_color\" style=\"background:#00bfff;\"></div>")

        self.assertEqual(category_2.title, title_category_placemark_2)
        self.assertTrue(category_2.active)
        self.assertEqual(category_2.ymap.slug, test_map.slug)
        self.assertEqual(category_2.get_map_name(), test_map.title)
        self.assertEqual(category_2.get_title(), title_category_placemark_2)
        self.assertEqual(category_2.category_icon, "")
        self.assertEqual(category_2.category_color, "#00bfff")

        self.assertEqual(category_2.get_category_icon(), "")

        self.assertEqual(
            category_2.get_category_color(),
            "<div class=\"djeym_category_color\" style=\"background:#00bfff;\"></div>")

        self.assertEqual(CategoryPlacemark._meta.ordering, ('title',))

    def test_subcategory_placemark(self):
        """
        Test the model of the SubCategoryPlacemark with the default settings.
        Тестирование модели SubCategoryPlacemark с настройками по умолчанию.
        """
        title_map = self.title_map
        title_subcategory_placemark_1 = self.title_subcategory_placemark_1
        title_subcategory_placemark_2 = self.title_subcategory_placemark_2

        test_map = Map.objects.create(title=title_map)
        subcategory_1 = SubCategoryPlacemark.objects.create(
            ymap=test_map,
            title=title_subcategory_placemark_1)
        subcategory_2 = SubCategoryPlacemark.objects.create(
            ymap=test_map,
            title=title_subcategory_placemark_2)

        self.assertEqual(test_map.subcategory_placemark.all().count(), 2)
        self.assertEqual(SubCategoryPlacemark._meta.get_field('ymap')
                         .get_internal_type(), "ForeignKey")

        self.assertFalse(SubCategoryPlacemark._meta.get_field('title').unique)
        self.assertFalse(SubCategoryPlacemark._meta.get_field('title').blank)

        self.assertEqual(subcategory_1.title, title_subcategory_placemark_1)
        self.assertEqual(subcategory_1.category_icon, "")
        self.assertEqual(subcategory_1.category_color, "#ffcc00")
        self.assertTrue(subcategory_1.active)
        self.assertEqual(subcategory_1.ymap.slug, test_map.slug)
        self.assertEqual(subcategory_1.get_map_name(), test_map.title)
        self.assertEqual(subcategory_1.get_title(),
                         title_subcategory_placemark_1)

        self.assertEqual(subcategory_1.get_category_icon(), "")

        self.assertEqual(
            subcategory_1.get_category_color(),
            "<div class=\"djeym_category_color\" style=\"background:#ffcc00;\"></div>")

        self.assertEqual(subcategory_2.title, title_subcategory_placemark_2)
        self.assertEqual(subcategory_2.category_icon, "")
        self.assertEqual(subcategory_2.category_color, "#ffcc00")
        self.assertTrue(subcategory_2.active)
        self.assertEqual(subcategory_2.ymap.slug, test_map.slug)
        self.assertEqual(subcategory_2.get_map_name(), test_map.title)
        self.assertEqual(subcategory_2.get_title(),
                         title_subcategory_placemark_2)

        self.assertEqual(subcategory_2.get_category_icon(), "")

        self.assertEqual(
            subcategory_2.get_category_color(),
            "<div class=\"djeym_category_color\" style=\"background:#ffcc00;\"></div>")

        self.assertEqual(SubCategoryPlacemark._meta.ordering, ('title',))

    def test_category_polyline(self):
        """
        Test the model of the CategoryPolyline with the default settings.
        Тестирование модели CategoryPolyline с настройками по умолчанию.
        """
        title_map = self.title_map
        title_category_polyline_1 = self.title_category_polyline_1
        title_category_polyline_2 = self.title_category_polyline_2

        test_map = Map.objects.create(title=title_map)

        category_1 = CategoryPolyline.objects.create(
            ymap=test_map,
            title=title_category_polyline_1)
        category_2 = CategoryPolyline.objects.create(
            ymap=test_map,
            title=title_category_polyline_2)

        self.assertEqual(test_map.category_polyline.count(), 2)
        self.assertEqual(CategoryPolyline._meta.get_field('ymap')
                         .get_internal_type(), "ForeignKey")

        self.assertFalse(CategoryPolyline._meta.get_field('title').unique)
        self.assertFalse(CategoryPolyline._meta.get_field('title').blank)

        self.assertEqual(category_1.title, title_category_polyline_1)
        self.assertEqual(category_1.category_icon, "")
        self.assertEqual(category_1.category_color, "#00bfff")
        self.assertTrue(category_1.active)
        self.assertEqual(category_1.ymap.slug, test_map.slug)
        self.assertEqual(category_1.get_map_name(), test_map.title)
        self.assertEqual(category_1.get_title(), title_category_polyline_1)

        self.assertEqual(category_1.get_category_icon(), "")

        self.assertEqual(
            category_1.get_category_color(),
            "<div class=\"djeym_category_color\" style=\"background:#00bfff;\"></div>")

        self.assertEqual(category_2.title, title_category_polyline_2)
        self.assertEqual(category_2.category_icon, "")
        self.assertEqual(category_2.category_color, "#00bfff")
        self.assertTrue(category_2.active)
        self.assertEqual(category_2.ymap.slug, test_map.slug)
        self.assertEqual(category_2.get_map_name(), test_map.title)
        self.assertEqual(category_2.get_title(), title_category_polyline_2)

        self.assertEqual(category_2.get_category_icon(), "")

        self.assertEqual(
            category_2.get_category_color(),
            "<div class=\"djeym_category_color\" style=\"background:#00bfff;\"></div>")

        self.assertEqual(CategoryPolyline._meta.ordering, ('title',))

    def test_category_polygon(self):
        """
        Test the model of the CategoryPolygon with the default settings.
        Тестирование модели CategoryPolygon с настройками по умолчанию.
        """
        title_map = self.title_map
        title_category_polygon_1 = self.title_category_polygon_1
        title_category_polygon_2 = self.title_category_polygon_2

        test_map = Map.objects.create(title=title_map)

        category_1 = CategoryPolygon.objects.create(
            ymap=test_map,
            title=title_category_polygon_1)
        category_2 = CategoryPolygon.objects.create(
            ymap=test_map,
            title=title_category_polygon_2)

        self.assertEqual(test_map.category_polygon.count(), 2)
        self.assertEqual(CategoryPolygon._meta.get_field('ymap')
                         .get_internal_type(), "ForeignKey")

        self.assertFalse(CategoryPolygon._meta.get_field('title').unique)
        self.assertFalse(CategoryPolygon._meta.get_field('title').blank)

        self.assertEqual(category_1.title, title_category_polygon_1)
        self.assertEqual(category_1.category_icon, "")
        self.assertEqual(category_1.category_color, "#00bfff")
        self.assertTrue(category_1.active)
        self.assertEqual(category_1.ymap.slug, test_map.slug)
        self.assertEqual(category_1.get_map_name(), test_map.title)
        self.assertEqual(category_1.get_title(), title_category_polygon_1)

        self.assertEqual(category_1.get_category_icon(), "")

        self.assertEqual(
            category_1.get_category_color(),
            "<div class=\"djeym_category_color\" style=\"background:#00bfff;\"></div>")

        self.assertEqual(category_2.title, title_category_polygon_2)
        self.assertEqual(category_2.category_icon, "")
        self.assertEqual(category_2.category_color, "#00bfff")
        self.assertTrue(category_2.active)
        self.assertEqual(category_2.ymap.slug, test_map.slug)
        self.assertEqual(category_2.get_map_name(), test_map.title)
        self.assertEqual(category_2.get_title(), title_category_polygon_2)

        self.assertEqual(category_1.get_category_icon(), "")

        self.assertEqual(
            category_1.get_category_color(),
            "<div class=\"djeym_category_color\" style=\"background:#00bfff;\"></div>")

        self.assertEqual(CategoryPolygon._meta.ordering, ('title',))

    def test_placemark(self):
        """
        Test the model of the Placemark with the default settings.
        Тестирование модели Placemark с настройками по умолчанию.
        """
        title_map = self.title_map
        title_category_placemark_1 = self.title_category_placemark_1
        title_subcategory_placemark_1 = self.title_subcategory_placemark_1
        title_subcategory_placemark_2 = self.title_subcategory_placemark_2
        header_placemark_1 = self.header_placemark_1
        header_placemark_2 = self.header_placemark_2
        custom_marker_icon = self.custom_marker_icon_1
        title_icon_collection = self.title_icon_collection

        collection = IconCollection.objects.create(title=title_icon_collection)

        icon_marker = CustomMarkerIcon.objects.create(
            icon_collection=collection,
            title=custom_marker_icon,
            svg="test_marker.svg")

        test_map = Map.objects.create(title=title_map)
        category = CategoryPlacemark.objects.create(
            ymap=test_map,
            title=title_category_placemark_1)
        subcategory_1 = SubCategoryPlacemark.objects.create(
            ymap=test_map,
            title=title_subcategory_placemark_1)
        subcategory_2 = SubCategoryPlacemark.objects.create(
            ymap=test_map,
            title=title_subcategory_placemark_2)
        placemark_1 = Placemark.objects.create(
            ymap=test_map,
            category=category,
            header=header_placemark_1,
            icon_name=icon_marker.slug)
        placemark_1.subcategories.add(subcategory_1, subcategory_2)
        placemark_2 = Placemark.objects.create(
            ymap=test_map,
            category=category,
            header=header_placemark_2,
            icon_name=icon_marker.slug)
        placemark_2.subcategories.add(subcategory_1, subcategory_2)

        self.assertEqual(test_map.placemark_map.all().count(), 2)
        self.assertEqual(category.placemark_category.all().count(), 2)
        self.assertEqual(
            subcategory_1.placemark_subcategories.all().count(), 2)
        self.assertEqual(
            subcategory_2.placemark_subcategories.all().count(), 2)

        self.assertEqual(Placemark._meta.get_field('ymap')
                         .get_internal_type(), "ForeignKey")
        self.assertEqual(Placemark._meta.get_field('category')
                         .get_internal_type(), "ChainedForeignKey")
        self.assertEqual(Placemark._meta.get_field('subcategories')
                         .get_internal_type(), "ChainedManyToManyField")

        self.assertFalse(Placemark._meta.get_field('header').blank)

        self.assertEqual(placemark_1.ymap.pk, test_map.pk)
        self.assertEqual(placemark_1.category.pk, category.pk)
        self.assertEqual(placemark_1.subcategories.get(
            pk=1).pk, subcategory_1.pk)
        self.assertEqual(placemark_1.subcategories.get(
            pk=2).pk, subcategory_2.pk)
        self.assertEqual(placemark_1.header, "<p>Test placemark 1</p>")
        self.assertEqual(placemark_1.__str__(), "<p>Test placemark 1</p>")
        self.assertEqual(placemark_1.body, "")
        self.assertEqual(placemark_1.footer, "")
        self.assertEqual(placemark_1.icon_name, icon_marker.slug)
        self.assertEqual(placemark_1.coordinates, "[0,0]")
        self.assertEqual(placemark_1.like, 0)
        self.assertEqual(placemark_1.dislike, 0)
        self.assertTrue(placemark_1.active)
        self.assertEqual(placemark_1.ymap.slug, test_map.slug)

        self.assertEqual(placemark_2.ymap.pk, test_map.pk)
        self.assertEqual(placemark_2.category.pk, category.pk)
        self.assertEqual(placemark_2.subcategories.get(
            pk=1).pk, subcategory_1.pk)
        self.assertEqual(placemark_2.subcategories.get(
            pk=2).pk, subcategory_2.pk)
        self.assertEqual(placemark_2.header, "<p>Test placemark 2</p>")
        self.assertEqual(placemark_2.__str__(), "<p>Test placemark 2</p>")
        self.assertEqual(placemark_2.body, "")
        self.assertEqual(placemark_2.footer, "")
        self.assertEqual(placemark_2.icon_name, icon_marker.slug)
        self.assertEqual(placemark_2.coordinates, "[0,0]")
        self.assertEqual(placemark_2.like, 0)
        self.assertEqual(placemark_2.dislike, 0)
        self.assertTrue(placemark_2.active)
        self.assertEqual(placemark_2.ymap.slug, test_map.slug)

        self.assertEqual(Placemark._meta.ordering, ("-id",))

    def test_polyline(self):
        """
        Test the model of the Polyline with the default settings.
        Тестирование модели Polyline с настройками по умолчанию.
        """
        title_map = self.title_map
        title_category_polyline_1 = self.title_category_polyline_1
        header_polyline_1 = self.header_polyline_1
        header_polyline_2 = self.header_polyline_2
        coordinates = '[[0,0],[11,11]]'

        test_map = Map.objects.create(title=title_map)
        category = CategoryPolyline.objects.create(
            ymap=test_map,
            title=title_category_polyline_1)
        polyline_1 = Polyline.objects.create(
            ymap=test_map,
            category=category,
            header=header_polyline_1,
            coordinates=coordinates)
        polyline_2 = Polyline.objects.create(
            ymap=test_map,
            category=category,
            header=header_polyline_2,
            coordinates=coordinates)

        self.assertEqual(Polyline._meta.get_field('ymap')
                         .get_internal_type(), "ForeignKey")
        self.assertEqual(Polyline._meta.get_field('category')
                         .get_internal_type(), "ChainedForeignKey")

        self.assertEqual(test_map.polyline_map.all().count(), 2)
        self.assertEqual(category.polyline_category.all().count(), 2)

        self.assertFalse(Polyline._meta.get_field('header').blank)

        self.assertEqual(polyline_1.ymap.pk, test_map.pk)
        self.assertEqual(polyline_1.category.pk, category.pk)
        self.assertEqual(polyline_1.header, "<p>Test polyline 1</p>")
        self.assertEqual(polyline_1.__str__(), "<p>Test polyline 1</p>")
        self.assertEqual(polyline_1.body, "")
        self.assertEqual(polyline_1.footer, "")
        self.assertEqual(polyline_1.stroke_width, 5)
        self.assertEqual(polyline_1.stroke_color, "#1e98ff")
        self.assertEqual(polyline_1.stroke_opacity, '0.9')
        self.assertEqual(polyline_1.coordinates, coordinates)
        self.assertEqual(polyline_1.like, 0)
        self.assertEqual(polyline_1.dislike, 0)
        self.assertTrue(polyline_1.active)

        self.assertEqual(polyline_2.ymap.pk, test_map.pk)
        self.assertEqual(polyline_2.category.pk, category.pk)
        self.assertEqual(polyline_2.header, "<p>Test polyline 2</p>")
        self.assertEqual(polyline_2.__str__(), "<p>Test polyline 2</p>")
        self.assertEqual(polyline_2.body, "")
        self.assertEqual(polyline_2.footer, "")
        self.assertEqual(polyline_2.stroke_width, 5)
        self.assertEqual(polyline_2.stroke_color, "#1e98ff")
        self.assertEqual(polyline_2.stroke_opacity, '0.9')
        self.assertEqual(polyline_2.coordinates, coordinates)
        self.assertEqual(polyline_2.like, 0)
        self.assertEqual(polyline_2.dislike, 0)
        self.assertTrue(polyline_2.active)

        self.assertEqual(Polyline._meta.ordering, ("-id",))

    def test_polygon(self):
        """
        Test the model of the Polygon with the default settings.
        Тестирование модели Polygon с настройками по умолчанию.
        """
        title_map = self.title_map
        title_category_polygon_1 = self.title_category_polygon_1
        header_polygon_1 = self.header_polygon_1
        header_polygon_2 = self.header_polygon_2
        coordinates = '[[0,0],[11,11],[22,22],[33,33]]'

        test_map = Map.objects.create(title=title_map)
        category = CategoryPolygon.objects.create(
            ymap=test_map,
            title=title_category_polygon_1)
        polygon_1 = Polygon.objects.create(
            ymap=test_map,
            category=category,
            header=header_polygon_1,
            coordinates=coordinates)
        polygon_2 = Polygon.objects.create(
            ymap=test_map,
            category=category,
            header=header_polygon_2,
            coordinates=coordinates)

        self.assertEqual(Polygon._meta.get_field('ymap')
                         .get_internal_type(), "ForeignKey")
        self.assertEqual(Polygon._meta.get_field('category')
                         .get_internal_type(), "ChainedForeignKey")

        self.assertEqual(test_map.polygon_map.all().count(), 2)
        self.assertEqual(category.polygon_category.all().count(), 2)

        self.assertFalse(Polygon._meta.get_field('header').blank)

        self.assertEqual(polygon_1.ymap.pk, test_map.pk)
        self.assertEqual(polygon_1.category.pk, category.pk)
        self.assertEqual(polygon_1.header, "<p>Test polygon 1</p>")
        self.assertEqual(polygon_1.__str__(), "<p>Test polygon 1</p>")
        self.assertEqual(polygon_1.body, "")
        self.assertEqual(polygon_1.footer, "")
        self.assertEqual(polygon_1.stroke_width, 2)
        self.assertEqual(polygon_1.stroke_color, "#1e98ff")
        self.assertEqual(polygon_1.stroke_opacity, '0.9')
        self.assertEqual(polygon_1.fill_color, "#1e98ff")
        self.assertEqual(polygon_1.fill_opacity, '0.9')
        self.assertEqual(polygon_1.coordinates, coordinates)
        self.assertEqual(polygon_1.like, 0)
        self.assertEqual(polygon_1.dislike, 0)
        self.assertTrue(polygon_1.active)

        self.assertEqual(polygon_2.ymap.pk, test_map.pk)
        self.assertEqual(polygon_2.category.pk, category.pk)
        self.assertEqual(polygon_2.header, "<p>Test polygon 2</p>")
        self.assertEqual(polygon_2.__str__(), "<p>Test polygon 2</p>")
        self.assertEqual(polygon_2.body, "")
        self.assertEqual(polygon_2.footer, "")
        self.assertEqual(polygon_2.stroke_width, 2)
        self.assertEqual(polygon_2.stroke_color, "#1e98ff")
        self.assertEqual(polygon_2.stroke_opacity, '0.9')
        self.assertEqual(polygon_2.fill_color, "#1e98ff")
        self.assertEqual(polygon_2.fill_opacity, '0.9')
        self.assertEqual(polygon_2.coordinates, coordinates)
        self.assertEqual(polygon_2.like, 0)
        self.assertEqual(polygon_2.dislike, 0)
        self.assertTrue(polygon_2.active)

        self.assertEqual(Polygon._meta.ordering, ("-id",))

    def test_cluster_icon_check_without_image(self):
        """
        Test the model of the CustomClusterIcon with the default settings.
        Тестирование модели CustomClusterIcon с настройками по умолчанию.
        """
        title_cluster_icon = self.title_cluster_icon

        cluster_icon = CustomClusterIcon.objects.create(
            title=title_cluster_icon)

        self.assertTrue(CustomClusterIcon._meta.get_field('title').unique)
        self.assertFalse(CustomClusterIcon._meta.get_field('title').blank)
        self.assertFalse(CustomClusterIcon._meta.get_field('svg').blank)

        self.assertEqual(cluster_icon.title, "Test Cluster Icon")
        self.assertFalse(bool(cluster_icon.svg))
        self.assertEqual(cluster_icon.size_width, 0)
        self.assertEqual(cluster_icon.size_height, 0)
        self.assertEqual(cluster_icon.offset_x, Decimal(".0"))
        self.assertEqual(cluster_icon.offset_y, Decimal(".0"))
        self.assertEqual(cluster_icon.slug, "test-cluster-icon")

        self.assertEqual(cluster_icon.upload_dir, "djeym_custom_icons")
        self.assertEqual(cluster_icon.__str__(), "Test Cluster Icon")
        self.assertEqual(cluster_icon.admin_thumbnail(), "")

        self.assertEqual(CustomClusterIcon._meta.ordering, ("title", "id"))

        self.assertEqual(cluster_icon.get_size(), "[0,0]")
        self.assertEqual(cluster_icon.get_offset(), "[0.0,0.0]")

    def test_cluster_icon_check_with_image(self):
        """
        Test the model of the CustomClusterIcon with the default settings.
        Тестирование модели CustomClusterIcon с настройками по умолчанию.
        """
        title_cluster_icon = self.title_cluster_icon

        cluster_icon = CustomClusterIcon.objects.create(
            title=title_cluster_icon, svg="test_cluster.svg")

        self.assertTrue(CustomClusterIcon._meta.get_field('title').unique)
        self.assertFalse(CustomClusterIcon._meta.get_field('title').blank)
        self.assertFalse(CustomClusterIcon._meta.get_field('svg').blank)

        self.assertEqual(cluster_icon.title, "Test Cluster Icon")
        self.assertTrue(bool(cluster_icon.svg))
        self.assertEqual(cluster_icon.size_width, 60)
        self.assertEqual(cluster_icon.size_height, 60)
        self.assertEqual(cluster_icon.offset_x, Decimal("-30.0"))
        self.assertEqual(cluster_icon.offset_y, Decimal("-30.0"))
        self.assertEqual(cluster_icon.slug, "test-cluster-icon")

        self.assertEqual(cluster_icon.upload_dir, "djeym_custom_icons")
        self.assertEqual(cluster_icon.__str__(), "Test Cluster Icon")

        self.assertEqual(
            cluster_icon.admin_thumbnail(),
            "<img src=\"/media/test_cluster.svg\" height=\"60\" alt=\"Icon\">")

        self.assertEqual(CustomClusterIcon._meta.ordering, ("title", "id"))

        self.assertEqual(cluster_icon.get_size(), "[60,60]")
        self.assertEqual(cluster_icon.get_offset(), "[-30.0,-30.0]")

    def test_icon_collection(self):
        """
        Test the model of the IconCollection with the default settings.
        Тестирование модели IconCollection с настройками по умолчанию.
        """
        title_icon_collection = self.title_icon_collection

        collection = IconCollection.objects.create(title=title_icon_collection)

        self.assertTrue(IconCollection._meta.get_field('title').unique)
        self.assertFalse(IconCollection._meta.get_field('title').blank)
        self.assertEqual(IconCollection._meta.get_field(
            'title').max_length, 60)

        self.assertEqual(collection.__str__(), title_icon_collection)
        self.assertEqual(collection.admin_thumbnail(), "")
        self.assertEqual(IconCollection._meta.ordering, ("title", "id"))
        self.assertEqual(collection.get_icon_count(), 0)
        self.assertEqual(collection.get_count_of_active_icons(), 0)

    def test_custom_marker_icon(self):
        """
        Test the model of the CustomMarkerIcon with the default settings.
        Тестирование модели CustomMarkerIcon с настройками по умолчанию.
        """
        custom_marker_icon = self.custom_marker_icon_1
        title_icon_collection = self.title_icon_collection

        collection = IconCollection.objects.create(title=title_icon_collection)

        icon_marker = CustomMarkerIcon.objects.create(
            icon_collection=collection,
            title=custom_marker_icon,
            svg="test_marker.svg")

        self.assertEqual(collection.icons.count(), 1)
        self.assertEqual(icon_marker.icon_collection.icons.count(), 1)

        self.assertFalse(CustomMarkerIcon._meta.get_field('title').unique)
        self.assertFalse(CustomMarkerIcon._meta.get_field('title').blank)
        self.assertEqual(CustomMarkerIcon._meta.get_field(
            'title').max_length, 60)

        self.assertTrue(bool(icon_marker.svg))
        self.assertEqual(icon_marker.size_width, 46)
        self.assertEqual(icon_marker.size_height, 60)
        self.assertEqual(icon_marker.offset_x, Decimal("-23.0"))
        self.assertEqual(icon_marker.offset_y, Decimal(-60))
        self.assertTrue(icon_marker.active)
        self.assertEqual(icon_marker.__str__(), custom_marker_icon)
        self.assertEqual(CustomMarkerIcon._meta.ordering, ("title", "id"))
        self.assertEqual(icon_marker.get_collection_name(),
                         title_icon_collection)

        self.assertEqual(icon_marker.get_collection_name(),
                         title_icon_collection)
        self.assertIsNone(icon_marker.clean())

        self.assertEqual(icon_marker.get_size(), "[46,60]")
        self.assertEqual(icon_marker.get_offset(), '[-23.0,-60]')

    def test_icon_collection_full(self):
        """
        Testing IconCollection model with Map and CustomMarkerIcon models.
        Тестирование модели IconCollection с моделями Map и CustomMarkerIcon.
        """
        title_icon_collection = self.title_icon_collection
        custom_marker_icon_1 = self.custom_marker_icon_1
        custom_marker_icon_2 = self.custom_marker_icon_2
        title_map = self.title_map

        icon_collection = IconCollection.objects.create(
            title=title_icon_collection)

        icon_marker_1 = CustomMarkerIcon.objects.create(
            icon_collection=icon_collection,
            title=custom_marker_icon_1,
            svg="test_marker.svg")

        icon_marker_2 = CustomMarkerIcon.objects.create(
            icon_collection=icon_collection,
            title=custom_marker_icon_2,
            svg="test_marker.svg")

        test_map = Map.objects.create(
            title=title_map, icon_collection=icon_collection)

        self.assertEqual(icon_collection.icons.count(), 2)
        self.assertEqual(icon_collection.map_icon_collection.count(), 1)

        self.assertEqual(icon_marker_1.icon_collection.title,
                         title_icon_collection)
        self.assertEqual(icon_marker_2.icon_collection.title,
                         title_icon_collection)
        self.assertEqual(test_map.icon_collection.title, title_icon_collection)

        self.assertEqual(icon_marker_1.get_size(), "[46,60]")
        self.assertEqual(icon_marker_1.get_offset(), '[-23.0,-60]')

        self.assertEqual(icon_marker_2.get_size(), "[46,60]")
        self.assertEqual(icon_marker_2.get_offset(), '[-23.0,-60]')

        self.assertEqual(
            icon_collection.map_icon_collection.all().first().title, title_map)
        self.assertEqual(icon_collection.icons.all()[
                         0].title, custom_marker_icon_1)
        self.assertEqual(icon_collection.icons.all()[
                         1].title, custom_marker_icon_2)

    def test_counter_id(self):
        """
        Testing CounterID model.
        Тестирование модели CounterID.
        """
        counter_id = CounterID.objects.create()

        self.assertFalse(CounterID._meta.get_field('num_id').blank)
        self.assertEqual(CounterID._meta.get_field('num_id').default, 1)
        self.assertEqual(counter_id.num_id, 1)

    def test_statistics(self):
        """
        Testing Statistics model.
        Тестирование модели Statistics.
        """
        obj_type = 'Point'
        obj_id = 1
        ip = '127.0.0.1'
        likes = True

        statistics = Statistics.objects.create(
            obj_type=obj_type,
            obj_id=obj_id,
            ip=ip,
            likes=likes
        )

        self.assertEqual(Statistics._meta.get_field(
            'obj_type').get_internal_type(), 'CharField')
        self.assertFalse(Statistics._meta.get_field(
            'obj_type').blank)
        self.assertEqual(Statistics._meta.get_field(
            'obj_type').default, "")
        self.assertEqual(statistics.obj_type, obj_type)

        self.assertEqual(Statistics._meta.get_field(
            'obj_id').get_internal_type(), 'PositiveIntegerField')
        self.assertFalse(Statistics._meta.get_field(
            'obj_id').blank)
        self.assertEqual(Statistics._meta.get_field(
            'obj_id').default, 0)
        self.assertEqual(statistics.obj_id, obj_id)

        self.assertEqual(Statistics._meta.get_field(
            'ip').get_internal_type(), 'GenericIPAddressField')
        self.assertFalse(Statistics._meta.get_field(
            'ip').blank)
        self.assertTrue(Statistics._meta.get_field(
            'ip').null)
        self.assertEqual(statistics.ip, ip)

        self.assertEqual(Statistics._meta.get_field(
            'likes').get_internal_type(), 'BooleanField')
        self.assertFalse(Statistics._meta.get_field(
            'likes').blank)
        self.assertFalse(Statistics._meta.get_field(
            'likes').default)
        self.assertEqual(statistics.likes, likes)

        self.assertEqual(Statistics._meta.get_field(
            'timestamp').get_internal_type(), 'DateTimeField')
        self.assertFalse(Statistics._meta.get_field(
            'timestamp').blank)
