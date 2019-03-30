# -*- coding: utf-8 -*-
import base64
import copy
import io
import json
import re

from django.core.files import File
from django.core.files.base import ContentFile
from django.db import connection
from django.db.models import Q
from django.http import (FileResponse, HttpResponse, HttpResponseForbidden,
                         JsonResponse)
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, View
from ipware import get_client_ip
from slugify import slugify

from .__init__ import __version__
from .decorators import ajax_login_required_and_staff
from .forms import (CKEditorTextareaForm, GeneralSettingsForm,
                    GeoObjectsTransferForm, HeatmapSettingsForm, HeatPointForm,
                    MapControlsForm, PlacemarkForm, PolygonForm, PolylineForm,
                    PresetForm)
from .mixins import StaffRequiredMixin
from .models import (CustomClusterIcon, CustomMarkerIcon, HeatPoint,
                     IconCollection, LoadIndicator, Map, Placemark, Polygon,
                     Polyline, Preset, Statistics, TileSource)
from .utils import get_errors_form, get_icon_font_plugin

DJEYM_YMAPS_ICONS_FOR_CATEGORIES = get_icon_font_plugin()


class EditorYMap(StaffRequiredMixin, TemplateView):
    """
    Load the map to the editor page.
    Загрузить карту на страницу редактора.
    """
    template_name = "djeym/ymeditor.html"

    def get_context_data(self, **kwargs):
        slug = kwargs.get("slug")
        ymap = Map.objects.filter(slug=slug, active=True).first()
        context = super(EditorYMap, self).get_context_data(**kwargs)

        if ymap is not None:
            controls = ymap.controls

            if ymap.icon_collection is not None:
                icons = ymap.icon_collection.icons.filter(active=True)
            else:
                icons = None

            context['djeym_version'] = __version__
            context['form_geo'] = GeoObjectsTransferForm(ymap_id=ymap.pk)
            context['form_controls'] = MapControlsForm(instance=controls)
            context['cluster'] = ymap.icon_cluster
            context['icons'] = icons
            context['tile'] = ymap.tile
            context['presets'] = ymap.presets.all()
            context['tile_sources'] = TileSource.objects.all()
            context['controls'] = controls
            context['external_modules'] = ymap.external_modules
            context['heat_form'] = HeatmapSettingsForm(
                instance=ymap.heatmap_settings)
            context['general_settings'] = ymap.general_settings
            context['load_indicators'] = LoadIndicator.objects.all()
            context['selected_load_indicator'] = ymap.load_indicator
            context['load_indicator_size'] = ymap.load_indicator_size
            context['category_icons_css'] = [] if DJEYM_YMAPS_ICONS_FOR_CATEGORIES[2] else \
                DJEYM_YMAPS_ICONS_FOR_CATEGORIES[0]
            context['category_icons_js'] = [] if DJEYM_YMAPS_ICONS_FOR_CATEGORIES[2] else \
                DJEYM_YMAPS_ICONS_FOR_CATEGORIES[1]
            context['form_cke'] = CKEditorTextareaForm()
            context['category_placemarks'] = ymap.category_placemark.filter(
                active=True)
            context['category_submarks'] = ymap.subcategory_placemark.filter(
                active=True)
            context['category_polylines'] = ymap.category_polyline.filter(
                active=True)
            context['category_polygons'] = ymap.category_polygon.filter(
                active=True)

        context['ymap'] = ymap
        return context


class AjaxBalloonContent(View):
    """
    Ajax, load Balloon Content.
    Ajax, загрузить содержимое балуна.
    """

    @staticmethod
    def add_presets(presets, geoobject, geoobject_type, pk):
        for preset in presets:
            preset_html = preset.html.replace(
                'djeymObjectType', geoobject_type).replace('djeymObjectID', pk)
            if (geoobject_type == 'Point' and preset.placemark) or \
                (geoobject_type == 'LineString' and preset.polyline) or \
                    (geoobject_type == 'Polygon' and preset.polygon):
                if preset.autoheader:
                    geoobject.header += preset_html
                if preset.autobody:
                    geoobject.body += preset_html
                if preset.autofooter:
                    geoobject.footer += preset_html
        return geoobject

    def get(self, request, *args, **kwargs):
        response_data = {}
        pk = request.GET.get('objID')
        obj_type = request.GET.get('objType')
        ids = request.GET.get('ids')
        presets_bool = json.loads(request.GET.get('presetsBool'))
        presets = []
        sign_loading = '<div id="djeymSignLoaded"></div>'

        if presets_bool:
            presets = Preset.objects.filter(
                Q(autoheader=True) | Q(autobody=True) | Q(autofooter=True))

        if ids is None:
            if obj_type == 'Point':
                geoobject = Placemark.objects.filter(id=pk).only(
                    'header', 'body', 'footer').first()
            elif obj_type == 'LineString':
                geoobject = Polyline.objects.filter(id=pk).only(
                    'header', 'body', 'footer').first()
            elif obj_type == 'Polygon':
                geoobject = Polygon.objects.filter(id=pk).only(
                    'header', 'body', 'footer').first()

            if presets:
                geoobject = self.add_presets(presets, geoobject, obj_type, pk)

            geoobject.footer += sign_loading
            response_data = {
                'header': mark_safe(geoobject.header),
                'body': mark_safe(geoobject.body),
                'footer': mark_safe(geoobject.footer)
            }
        else:
            ids = json.loads(ids)
            placemarks = Placemark.objects.filter(id__in=ids)

            for placemark in placemarks:
                pk = placemark.pk
                if presets:
                    placemark = self.add_presets(
                        presets, placemark, obj_type, str(pk))
                placemark.footer += sign_loading
                response_data[pk] = {
                    'header': mark_safe(placemark.header),
                    'body': mark_safe(placemark.body),
                    'footer': mark_safe(placemark.footer)
                }

        return JsonResponse(response_data)

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxBalloonContent, self).dispatch(request, *args, **kwargs)


class AjaxGetGeoObjectsPlacemark(View):
    """
    Ajax - Get Placemark type geo-objects for a website page or editor page.
    Ajax - Получить геообъекты типа Placemark для страницы сайта или редактора.
    """

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('map_id'))
        offset = int(request.GET.get('offset'))
        limit = offset + 1000

        geoobjects = Placemark.objects.filter(ymap__pk=map_id).values_list(
            'json_code', flat=True)[offset:limit]

        response_data = '[' + ','.join(geoobjects) + ']'

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxGetGeoObjectsPlacemark, self).dispatch(request, *args, **kwargs)


class AjaxGetHeatPoints(View):
    """
    Ajax - Get geo-objects of type heat point for a site page or editor.
    Ajax - Получить геообъекты типа тепловая точка для страницы сайта или редактора.
    """

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('map_id'))
        offset = int(request.GET.get('offset'))
        limit = offset + 1000

        geoobjects = HeatPoint.objects.filter(ymap__pk=map_id).values_list(
            'json_code', flat=True)[offset:limit]

        response_data = '[' + ','.join(geoobjects) + ']'

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxGetHeatPoints, self).dispatch(request, *args, **kwargs)


class AjaxGetGeoObjectsPolyline(View):
    """
    Ajax - Get Polyline type geo-objects for a website page or editor page.
    Ajax - Получить геообъекты типа Polyline для страницы сайта или редактора.
    """

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('map_id'))
        offset = int(request.GET.get('offset'))
        limit = offset + 500

        geoobjects = Polyline.objects.filter(ymap__pk=map_id).values_list(
            'json_code', flat=True)[offset:limit]

        response_data = '[' + ','.join(geoobjects) + ']'

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxGetGeoObjectsPolyline, self).dispatch(request, *args, **kwargs)


class AjaxGetGeoObjectsPolygon(View):
    """
    Ajax - Get Polygon type geo-objects for a website page or editor page.
    Ajax - Получить геообъекты типа Polygon для страницы сайта или редактора.
    """

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('map_id'))
        offset = int(request.GET.get('offset'))
        limit = offset + 500

        geoobjects = Polygon.objects.filter(ymap__pk=map_id).values_list(
            'json_code', flat=True)[offset:limit]

        response_data = '[' + ','.join(geoobjects) + ']'

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxGetGeoObjectsPolygon, self).dispatch(request, *args, **kwargs)


class AjaxSaveGeoObjects(View):
    """
    Save geo-objects to database.
    Сохранить геообъекты в базу данных.
    """

    def post(self, request, *args, **kwargs):
        pk = int(request.POST.get('pk'))
        geo_type = request.POST.get('geo_type')
        action = request.POST.get('action')

        if geo_type == 'heatpoint':

            if action == 'save':

                if pk:
                    form = HeatPointForm(
                        request.POST, instance=HeatPoint.objects.get(id=pk))
                else:
                    form = HeatPointForm(request.POST)

                if form.is_valid():
                    heatpoint = form.save()
                    response_data = '[' + heatpoint.json_code + ']'
                else:
                    response_data = {'detail': get_errors_form(form)['detail']}
                    return JsonResponse(response_data, status=400)

            elif action == 'reload':
                json_code = HeatPoint.objects.get(pk=pk).json_code
                response_data = '[' + json_code + ']'

            elif action == 'delete':
                HeatPoint.objects.get(id=pk).delete()
                response_data = '[]'

        if geo_type == 'placemark':

            if action == 'save':

                if pk:
                    form = PlacemarkForm(
                        request.POST, instance=Placemark.objects.get(id=pk))
                else:
                    form = PlacemarkForm(request.POST)

                if form.is_valid():
                    placemark = form.save()
                    response_data = '[' + placemark.json_code + ']'
                else:
                    response_data = {'detail': get_errors_form(form)['detail']}
                    return JsonResponse(response_data, status=400)

            elif action == 'reload':
                json_code = Placemark.objects.get(pk=pk).json_code
                response_data = '[' + json_code + ']'

            elif action == 'delete':
                Placemark.objects.get(id=pk).delete()
                response_data = '[]'

        elif geo_type == 'polyline':

            if action == 'save':

                if pk:
                    form = PolylineForm(
                        request.POST, instance=Polyline.objects.get(id=pk))
                else:
                    form = PolylineForm(request.POST)

                if form.is_valid():
                    polyline = form.save()
                    response_data = '[' + polyline.json_code + ']'
                else:
                    response_data = {'detail': get_errors_form(form)['detail']}
                    return JsonResponse(response_data, status=400)

            elif action == 'reload':
                json_code = Polyline.objects.get(pk=pk).json_code
                response_data = '[' + json_code + ']'

            elif action == 'delete':
                Polyline.objects.get(id=pk).delete()
                response_data = '[]'

        elif geo_type == 'polygon':

            if action == 'save':

                if pk:
                    form = PolygonForm(
                        request.POST, instance=Polygon.objects.get(id=pk))
                else:
                    form = PolygonForm(request.POST)

                if form.is_valid():
                    polygon = form.save()
                    response_data = '[' + polygon.json_code + ']'
                else:
                    response_data = {'detail': get_errors_form(form)['detail']}
                    return JsonResponse(response_data, status=400)

            elif action == 'reload':
                json_code = Polygon.objects.get(pk=pk).json_code
                response_data = '[' + json_code + ']'

            elif action == 'delete':
                Polygon.objects.get(id=pk).delete()
                response_data = '[]'

        return HttpResponse(response_data, content_type="application/json")

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxSaveGeoObjects, self).dispatch(request, *args, **kwargs)


class AjaxCustomClusterIcon(View):
    """
    Ajax - Upload a custom cluster icon for admin panel.
    Ajax - Загрузка иконок пользовательского кластера для панели администратора.
    """

    @ajax_login_required_and_staff
    def dispatch(self, *args, **kwargs):
        request = self.request

        icon_id = request.GET.get("obj_id")
        icon = CustomClusterIcon.objects.filter(pk=icon_id).first()

        if icon is not None:
            return JsonResponse({"url": icon.svg.url})
        else:
            return JsonResponse({"detail": "Icon not found."}, status=404)


class AjaxLoadIndicatorIcon(View):
    """
    Ajax - Download icons for the download indicator, for the admin panel.U
    Ajax - Загрузка иконок для индикатора загрузки, для панели администратора.
    """

    @ajax_login_required_and_staff
    def dispatch(self, *args, **kwargs):
        request = self.request

        icon_id = request.GET.get("obj_id")
        icon = LoadIndicator.objects.filter(pk=icon_id).first()

        if icon is not None:
            return JsonResponse({"url": icon.svg.url})
        else:
            return JsonResponse({"detail": "Icon not found."}, status=404)


class AjaxCollectionExampleIcon(View):
    """
    Ajax - Upload a custom cluster icon for admin panel.
    Ajax - Загрузка иконки примера из коллекции для панели администратора.
    """

    @ajax_login_required_and_staff
    def dispatch(self, *args, **kwargs):
        request = self.request

        collection_id = request.GET.get("obj_id")
        icon = CustomMarkerIcon.objects.filter(
            icon_collection__pk=collection_id).first()

        if icon is not None:
            return JsonResponse({"url": icon.svg.url})
        else:
            return JsonResponse({"detail": "Icon not found."}, status=404)


class AjaxTileScreenshot(View):
    """
    Ajax - Upload a screenshot of the tile.
    Ajax - Загрузить скриншот плитки.
    """

    @ajax_login_required_and_staff
    def dispatch(self, *args, **kwargs):
        request = self.request

        source_id = request.GET.get("obj_id")
        tile_source = TileSource.objects.filter(pk=source_id).first()

        if tile_source is not None:
            return JsonResponse({"url": tile_source.screenshot.url})
        else:
            return JsonResponse({"detail": "Screenshot not found."}, status=404)


class AjaxTileSourceChange(View):
    """
    Ajax - Tile Source Change.
    Ajax - Смена источника тайлов.
    """

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('map_id')
        tile_id = int(request.POST.get('tile_id'))

        ymap = Map.objects.get(pk=map_id)
        ymap.tile = TileSource.objects.get(
            pk=tile_id) if tile_id != 0 else None
        ymap.save()

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxTileSourceChange, self).dispatch(request, *args, **kwargs)


class AjaxLoadIndicatorChange(View):
    """
    Ajax - Change the download indicator.
    Ajax - Изменить индикатор загрузки.
    """

    def post(self, request, *args, **kwargs):
        map_id = int(request.POST.get('map_id'))
        slug = request.POST.get('slug')
        size = int(request.POST.get('size'))
        speed = request.POST.get('speed')
        animation = request.POST.get('animation')

        ymap = Map.objects.get(pk=map_id)
        ymap.load_indicator = LoadIndicator.objects.filter(slug=slug).first()
        ymap.load_indicator_size = size
        ymap.animation_speed = speed
        ymap.disable_indicator_animation = animation
        ymap.save()

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxLoadIndicatorChange, self).dispatch(request, *args, **kwargs)


class AjaxGeneralSettings(View):
    """
    Ajax - Update general settings.
    Ajax - Обновите общие настройки.
    """

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('ymap')
        roundtheme_bool = True if request.POST.get(
            'roundtheme') is not None else False
        ymap = Map.objects.get(pk=map_id)
        form = GeneralSettingsForm(
            request.POST, instance=ymap.general_settings)

        if form.is_valid():
            form.save()
            external_modules = ymap.external_modules
            external_modules.roundtheme = roundtheme_bool
            external_modules.save()
        else:
            response_data = {'detail': get_errors_form(form)['detail']}
            return JsonResponse(response_data, status=400)

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxGeneralSettings, self).dispatch(request, *args, **kwargs)


class AjaxMapControls(View):
    """
    Ajax - Update selection of map controls.
    Ajax - Обновить выбор элементов управления картой.
    """

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('ymap')
        controls = Map.objects.get(pk=map_id).controls
        form = MapControlsForm(request.POST, instance=controls)

        if form.is_valid():
            form.save()
        else:
            response_data = {'detail': get_errors_form(form)['detail']}
            return JsonResponse(response_data, status=400)

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxMapControls, self).dispatch(request, *args, **kwargs)


class AjaxHeatmapSettings(View):
    """
    Ajax - Update heatmap settings.
    Ajax - Обновить настройки тепловой карты.
    """

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('ymap')
        ymap = Map.objects.get(pk=map_id)
        form = HeatmapSettingsForm(
            request.POST, instance=ymap.heatmap_settings)

        if form.is_valid():
            form.save()
        else:
            response_data = {'detail': get_errors_form(form)['detail']}
            return JsonResponse(response_data, status=400)

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxHeatmapSettings, self).dispatch(request, *args, **kwargs)


class AjaxActivateHeatmap(View):
    """
    Ajax - Activate Heatmap.
    Ajax - Активировать Тепловую карту.
    """

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('mapID')
        heatmap_bool = request.POST.get('heatmap')
        external_modules = Map.objects.get(pk=map_id).external_modules

        external_modules.heatmap = heatmap_bool
        external_modules.save()

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxActivateHeatmap, self).dispatch(request, *args, **kwargs)


class AjaxHeatmapUndoSettings(View):
    """
    Ajax - Heatmap, reset to default settings.
    Ajax - Тепловая карта, сброс к настройкам по умолчанию.
    """

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('map_id')
        heatmap_settings = Map.objects.get(pk=map_id).heatmap_settings

        heatmap_settings.radius = 10
        heatmap_settings.dissipating = False
        heatmap_settings.opacity = '0.8'
        heatmap_settings.intensity = '0.2'
        heatmap_settings.gradient_color1 = '#56db40b3'
        heatmap_settings.gradient_color2 = '#ffd21ecc'
        heatmap_settings.gradient_color3 = '#ed4543e6'
        heatmap_settings.gradient_color4 = '#b22222'
        heatmap_settings.save()

        response_data = {
            'radius': int(heatmap_settings.radius),
            'dissipating': heatmap_settings.dissipating,
            'opacity': float(heatmap_settings.opacity),
            'intensityOfMidpoint': float(heatmap_settings.intensity),
            'gradient_color1': heatmap_settings.gradient_color1,
            'gradient_color2': heatmap_settings.gradient_color2,
            'gradient_color3': heatmap_settings.gradient_color3,
            'gradient_color4': heatmap_settings.gradient_color4
        }
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxHeatmapUndoSettings, self).dispatch(request, *args, **kwargs)


class AjaxUpdateLikes(View):
    """
    Ajax - Update current value of likes.
    Ajax - Обновить текущее значения лайков.
    """

    def get(self, request, *args, **kwargs):
        obj_type = request.GET.get('djeymObjectType')
        obj_id = request.GET.get('djeymObjectID')

        if obj_type == 'Point':
            result = Placemark.objects.get(id=obj_id)
        elif obj_type == 'LineString':
            result = Polyline.objects.get(id=obj_id)
        elif obj_type == 'Polygon':
            result = Polygon.objects.get(id=obj_id)

        response_data = {
            'like': result.like,
            'dislike': result.dislike
        }

        return JsonResponse(response_data)

    def post(self, request, *args, **kwargs):
        obj_type = request.POST.get('djeymObjectType')
        obj_id = request.POST.get('djeymObjectID')
        target_action = request.POST.get('targetAction')
        client_ip, is_routable = get_client_ip(request)
        result = None

        if client_ip is not None:
            statistics = Statistics.objects.filter(
                obj_type=obj_type, obj_id=obj_id, ip=client_ip, likes=True).count()
            if statistics == 0:
                Statistics.objects.create(
                    obj_type=obj_type, obj_id=obj_id, ip=client_ip, likes=True)
                if obj_type == 'Point':
                    result = Placemark.objects.get(id=obj_id)
                    if target_action == 'id_djeym_hand_like':
                        result.like += 1
                        result.save()
                    elif target_action == 'id_djeym_hand_dislike':
                        result.dislike += 1
                        result.save()
                elif obj_type == 'LineString':
                    result = Polyline.objects.get(id=obj_id)
                    if target_action == 'id_djeym_hand_like':
                        result.like += 1
                        result.save()
                    elif target_action == 'id_djeym_hand_dislike':
                        result.dislike += 1
                        result.save()
                elif obj_type == 'Polygon':
                    result = Polygon.objects.get(id=obj_id)
                    if target_action == 'id_djeym_hand_like':
                        result.like += 1
                        result.save()
                    elif target_action == 'id_djeym_hand_dislike':
                        result.dislike += 1
                        result.save()

        if result is None:
            if obj_type == 'Point':
                result = Placemark.objects.get(id=obj_id)
            elif obj_type == 'LineString':
                result = Polyline.objects.get(id=obj_id)
            elif obj_type == 'Polygon':
                result = Polygon.objects.get(id=obj_id)

        response_data = {
            'like': result.like,
            'dislike': result.dislike
        }

        return JsonResponse(response_data)

    def dispatch(self, request, *args, **kwargs):
        return super(AjaxUpdateLikes, self).dispatch(request, *args, **kwargs)


class AjaxUpdatePresetSettings(View):
    """
    Ajax - Update Preset settings.
    Ajax - Обновить настройки Пресета.
    """

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('ymap')
        preset_id = request.POST.get('pk')
        preset = Preset.objects.get(pk=preset_id)
        form = PresetForm(request.POST, instance=preset)

        if form.is_valid():
            form.save()
            ymap = Map.objects.get(pk=map_id)
            presets = ymap.presets.all()
            rendered_presets = render_to_string(
                'djeym/includes/presets.html',
                {'presets': presets, 'ymap': ymap},
                request=request)
        else:
            response_data = {'detail': get_errors_form(form)['detail']}
            return JsonResponse(response_data, status=400)

        response_data = {'html': rendered_presets}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxUpdatePresetSettings, self).dispatch(request, *args, **kwargs)


class AjaxImportIconCollection(View):
    """
    Import the collection of icons from the json file to the database.
    Импортировать коллекцию иконок из файла json в базу данных.
    """

    def post(self, request, *args, **kwargs):
        with request.FILES.get('collection').file as json_file:
            collection_json = json_file.read()

        collection_json = json.loads(collection_json)
        title = collection_json['title']

        if IconCollection.objects.filter(slug=slugify(title)).count() != 0:
            msg = _('The {} collection already exists.')
            response_data = {'detail': msg.format(title)}
            return JsonResponse(response_data, status=400)

        collection = IconCollection.objects.create(title=title)
        icons = collection_json['icons']

        for icon in icons:
            with io.BytesIO(icon['svg'].encode('utf-8')) as svg:
                marker_icon = CustomMarkerIcon.objects.create(
                    icon_collection=collection,
                    title=icon['title'],
                    size_width=icon['size_width'],
                    size_height=icon['size_height'],
                    offset_x=icon['offset_x'],
                    offset_y=icon['offset_y']
                )
                marker_icon.svg.save('icon.svg', File(svg))

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxImportIconCollection, self).dispatch(request, *args, **kwargs)


class ExportIconCollection(StaffRequiredMixin, View):
    """
    Export a collection of icons from a database into a json file.
    Экспортировать коллекцию иконок из базы данных в файл json.
    """

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        collection = IconCollection.objects.get(slug=slug)
        icons = collection.icons.all()
        collection_json = {
            "title": collection.title,
            "icons": []
        }
        raw_icon_json = {
            "title": "",
            "svg": "",
            "size_width": 0,
            "size_height": 0,
            "offset_x": ".0",
            "offset_y": ".0"
        }

        for icon in icons:
            with open(icon.svg.path) as svg_file:
                svg = svg_file.read()
            icon_json = copy.deepcopy(raw_icon_json)
            icon_json["title"] = icon.title
            icon_json["svg"] = svg
            icon_json["size_width"] = icon.size_width
            icon_json["size_height"] = icon.size_height
            icon_json["offset_x"] = '{}'.format(icon.offset_x)
            icon_json["offset_y"] = '{}'.format(icon.offset_y)
            collection_json["icons"].append(icon_json)

        collection_json = json.dumps(
            collection_json, ensure_ascii=False).encode('utf-8')
        stream = io.BytesIO(collection_json)
        response = FileResponse(stream, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename={0}.json'.format(
            slug.replace('-', '_'))
        return response
        return super(ExportIconCollection, self).dispatch(request, *args, **kwargs)


class AjaxImportTileSource(View):
    """
    Import tile layer sources from json file to database.
    Импортировать источники тайловых слоев из файла json в базу данных.
    """

    def post(self, request, *args, **kwargs):
        with request.FILES.get('sources').file as json_file:
            source_list = json_file.read()

        source_list = json.loads(source_list)

        for source in source_list:
            if TileSource.objects.filter(slug=slugify(source['title'])).count() == 0:
                image_type = 'png' if re.search(
                    r'png', source['screenshot']) is not None else 'jpg'
                screenshot = re.sub(
                    r'^data:image/(png|jpeg);base64,', "", source['screenshot'])
                TileSource.objects.create(
                    title=source['title'],
                    maxzoom=source['maxzoom'],
                    minzoom=source['minzoom'],
                    source=source['source'],
                    screenshot=ContentFile(
                        base64.b64decode(screenshot), 'pic.' + image_type),
                    copyrights=source['copyrights'],
                    site=source['site'],
                    apikey=source['apikey'],
                    note=source['note']
                )

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxImportTileSource, self).dispatch(request, *args, **kwargs)


class ExportTileSource(StaffRequiredMixin, View):
    """
    Export tile layer sources from a database to a json file.
    Экспортировать источники тайловых слоев из базы данных в файл json.
    """

    def dispatch(self, request, *args, **kwargs):
        sources = TileSource.objects.all()
        sources_list = []
        raw_include_json = {
            "title": "",
            "maxzoom": 0,
            "minzoom": 0,
            "source": "",
            "screenshot": None,
            "copyrights": "",
            "note": ""
        }

        for source in sources:
            with open(source.screenshot.path, "rb") as image_file:
                include_json = copy.deepcopy(raw_include_json)
                include_json['title'] = source.title
                include_json['maxzoom'] = source.maxzoom
                include_json['minzoom'] = source.minzoom
                include_json['source'] = source.source
                include_json['screenshot'] = base64.b64encode(
                    image_file.read()).decode("utf-8")
                include_json['copyrights'] = source.copyrights
                include_json['site'] = source.site
                include_json['apikey'] = source.apikey
                include_json['note'] = source.note
                sources_list.append(include_json)

        sources_json = json.dumps(
            sources_list, ensure_ascii=False).encode('utf-8')
        stream = io.BytesIO(sources_json)
        response = FileResponse(stream, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=Tile_Sources.json'
        return response
        return super(ExportTileSource, self).dispatch(request, *args, **kwargs)
