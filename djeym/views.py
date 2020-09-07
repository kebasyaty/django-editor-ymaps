# -*- coding: utf-8 -*-
import base64
import copy
import io
import json
import re

from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import (FileResponse, HttpResponse, HttpResponseForbidden,
                         JsonResponse)
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, View
from ipware import get_client_ip
from slugify import slugify

from .__init__ import (__django_version__, __djeym_version__,
                       __python_version__, __vue_version__,
                       __vuetify_version__)
from .decorators import ajax_login_required_and_staff
from .forms import (BlockedIPForm, CKEditorTextareaForm, CustomPlacemarkForm,
                    GeneralSettingsForm, HeatmapSettingsForm, HeatPointForm,
                    MapControlsForm, PlacemarkForm, PolygonForm, PolylineForm,
                    PresetForm)
from .mixins import StaffRequiredMixin
from .models import (BlockedIP, ClusterIcon, HeatPoint, IconCollection,
                     JsonSettings, LoadIndicator, Map, MarkerIcon, Placemark,
                     Polygon, Polyline, Preset, Statistics, TileSource)
from .signals_func import save_json_settings
from .utils import get_errors_form

IS_DEVELOPMANT = False


def vue_vendors_css_js(target):
    """Vendors CSS and JS for a framework Vue.js"""

    ctx = {}

    if not IS_DEVELOPMANT:
        if target == 'front':
            ctx['vue_css_app'] = 'app.73a7fd93.css'
            ctx['vue_css_chunk_vendors'] = 'chunk-vendors.e7a238a9.css'
            ctx['vue_js_app'] = 'app.55e65604.js'
            ctx['vue_js_chunk_vendors'] = 'chunk-vendors.11111a86.js'
            ctx['vue_js_app_legacy'] = 'app-legacy.9769f2c8.js'
            ctx['vue_js_chunk_vendors_legacy'] = 'chunk-vendors-legacy.36c3a3d3.js'
        else:
            ctx['vue_css_app'] = 'app.304727ca.css'
            ctx['vue_css_chunk_vendors'] = 'chunk-vendors.c47a893d.css'
            ctx['vue_js_app'] = 'app.c80f73bf.js'
            ctx['vue_js_chunk_vendors'] = 'chunk-vendors.61c8bbd1.js'
            ctx['vue_js_app_legacy'] = 'app-legacy.fb75bea4.js'
            ctx['vue_js_chunk_vendors_legacy'] = 'chunk-vendors-legacy.736c5d5a.js'
    else:
        # Automatically get CSS and JS for Vue.js (for development only).
        import os
        from django.conf import settings
        css_path_dir = '{0}/djeym/nodymaps/{1}/css'.format(
            settings.STATIC_ROOT, target)
        js_path_dir = '{0}/djeym/nodymaps/{1}/js'.format(
            settings.STATIC_ROOT, target)
        css_name_list = os.listdir(path=css_path_dir)
        js_name_list = os.listdir(path=js_path_dir)
        vue_css_app = list(filter(lambda name: re.match(
            r'^app.[0-9a-z]+.css$', name) is not None, css_name_list))[0]
        vue_css_chunk_vendors = list(filter(lambda name: re.match(
            r'^chunk-vendors.[0-9a-z]+.css$', name) is not None, css_name_list))[0]
        vue_js_app = list(filter(lambda name: re.match(
            r'^app.[0-9a-z]+.js$', name) is not None, js_name_list))[0]
        vue_js_chunk_vendors = list(filter(lambda name: re.match(
            r'^chunk-vendors.[0-9a-z]+.js$', name) is not None, js_name_list))[0]
        vue_js_app_legacy = list(filter(lambda name: re.match(
            r'^app-legacy.[0-9a-z]+.js$', name) is not None, js_name_list))[0]
        vue_js_chunk_vendors_legacy = list(filter(lambda name: re.match(
            r'^chunk-vendors-legacy.[0-9a-z]+.js$', name) is not None, js_name_list))[0]
        ctx['vue_css_app'] = vue_css_app
        ctx['vue_css_chunk_vendors'] = vue_css_chunk_vendors
        ctx['vue_js_app'] = vue_js_app
        ctx['vue_js_chunk_vendors'] = vue_js_chunk_vendors
        ctx['vue_js_app_legacy'] = vue_js_app_legacy
        ctx['vue_js_chunk_vendors_legacy'] = vue_js_chunk_vendors_legacy

    return ctx


# UPLOADING BALLOON CONTENT ------------------------------------------------------------------------
class AjaxBalloonContent(View):
    """Ajax - Upload Balloon Content."""

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
        is_presets = eval(request.GET.get('isPresets'))
        presets = []
        sign_loading = '<div id="djeymSignLoaded"></div>'

        if is_presets:
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

            geoobject.footer += sign_loading if is_presets else ''
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
                placemark.footer += sign_loading if is_presets else ''
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


# UPLOADING GEO OBJECTS ----------------------------------------------------------------------------
class AjaxUploadPlacemarks(View):
    """Ajax - Upload placemarks to map."""

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('mapID'))
        offset = int(request.GET.get('offset'))
        limit = offset + 1000

        geoobjects = Placemark.objects.filter(ymap__pk=map_id, active=True).values_list(
            'json_code', flat=True)[offset:limit]

        response_data = '[' + ','.join(geoobjects) + ']'

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxUploadPlacemarks, self).dispatch(request, *args, **kwargs)


class AjaxUploadHeatPoints(View):
    """Ajax - Upload heat points to map."""

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('mapID'))
        offset = int(request.GET.get('offset'))
        limit = offset + 1000

        geoobjects = HeatPoint.objects.filter(ymap__pk=map_id, active=True).values_list(
            'json_code', flat=True)[offset:limit]

        response_data = '[' + ','.join(geoobjects) + ']'

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxUploadHeatPoints, self).dispatch(request, *args, **kwargs)


class AjaxUploadPolylines(View):
    """Ajax - Upload polylines to map."""

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('mapID'))
        offset = int(request.GET.get('offset'))
        limit = offset + 500

        geoobjects = Polyline.objects.filter(ymap__pk=map_id, active=True).values_list(
            'json_code', flat=True)[offset:limit]

        response_data = '[' + ','.join(geoobjects) + ']'

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxUploadPolylines, self).dispatch(request, *args, **kwargs)


class AjaxUploadPolygons(View):
    """Ajax - Upload polygons to map."""

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('mapID'))
        offset = int(request.GET.get('offset'))
        limit = offset + 500

        geoobjects = Polygon.objects.filter(ymap__pk=map_id, active=True).values_list(
            'json_code', flat=True)[offset:limit]

        response_data = '[' + ','.join(geoobjects) + ']'

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxUploadPolygons, self).dispatch(request, *args, **kwargs)


# UPLOADING MAP AND SETTINGS TO THE EDITOR PAGE AND FRONT PAGE -------------------------------------
class YMapEditor(StaffRequiredMixin, TemplateView):
    """Load the map to the editor page."""

    template_name = "djeym/ymaps_editor.html"

    def get_context_data(self, **kwargs):
        slug = force_text(kwargs.get('slug'))
        ymap = Map.objects.filter(slug=slug, active=True).first()
        context = super(YMapEditor, self).get_context_data(**kwargs)

        if ymap is not None:
            context['load_indicator'] = ymap.load_indicator
            context['load_indicator_size'] = ymap.load_indicator_size
            context['form_cke'] = CKEditorTextareaForm()
            context['djeym_version'] = __djeym_version__
            context['python_version'] = '>= ' + __python_version__
            context['django_version'] = '>= ' + __django_version__
            context['vue_version'] = '== ' + __vue_version__
            context['vuetify_version'] = '== ' + __vuetify_version__
            context['is_heatmap'] = ymap.heatmap_settings.active
            context['is_round_theme'] = ymap.general_settings.roundtheme
            context['presets'] = ymap.presets.values_list('js', flat=True)
            vue_vendors = vue_vendors_css_js('editor')
            context.update(vue_vendors)

        context['ymap'] = ymap
        return context


class AjaxUploadSettingsEditor(View):
    """Ajax - Upload the settings for the editor page."""

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('mapID'))
        response_data = Map.objects.get(pk=map_id).json_settings.editor

        return HttpResponse(response_data, content_type="application/json")

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxUploadSettingsEditor, self).dispatch(request, *args, **kwargs)


class AjaxUploadSettingsFront(View):
    """Ajax - Upload the settings for the front page."""

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('mapID'))
        response_data = Map.objects.get(pk=map_id).json_settings.front

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxUploadSettingsFront, self).dispatch(request, *args, **kwargs)


# GEO OBJECTS - SAVING | UPDATING | DELETING -------------------------------------------------------
class AjaxSaveGeoObjects(View):
    """Geo objects - saving, updating and deleting"""

    def post(self, request, *args, **kwargs):
        pk = int(request.POST.get('pk'))
        geo_type = request.POST.get('geoType')
        action = request.POST.get('action')

        # Heatpoint
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

        # Placemark
        elif geo_type == 'placemark':

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

        # Polyline
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

        # Polygon
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


class AjaxSaveCusotmMarker(View):
    """Ajax - Save cusotm marker"""

    def post(self, request, *args, **kwargs):
        client_ip, is_routable = get_client_ip(request)

        if BlockedIP.objects.filter(ip=client_ip).count() == 0:
            form = CustomPlacemarkForm(request.POST)

            if form.is_valid():
                marker = form.save(commit=False)
                marker.user_ip = client_ip
                marker.user_image = request.FILES.get('user_image', None)
                marker.save()
                form.save_m2m()
            else:
                response_data = {'detail': get_errors_form(form)['detail']}
                return JsonResponse(response_data, status=400)

        response_data = {'Success': True}
        return JsonResponse(response_data)


# BLOCK IP ADDRESSES -------------------------------------------------------------------------------
class AjaxBlockIPAddress(View):
    """Ajax - Block ip address"""

    def post(self, request, *args, **kwargs):
        form = BlockedIPForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            response_data = {'detail': get_errors_form(form)['detail']}
            return JsonResponse(response_data, status=400)

        response_data = {'Success': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxBlockIPAddress, self).dispatch(request, *args, **kwargs)


# UPLOADING - SCREENSHOTS,EXAMPLE ICON, ICON COLLECTION --------------------------------------------
# (For admin panel.)
class AjaxClusterIcon(View):
    """Ajax - Upload a example of cluster icon to admin panel."""

    def get(self, request, *args, **kwargs):
        icon_id = request.GET.get("obj_id")
        icon = ClusterIcon.objects.filter(pk=icon_id).first()

        if icon is not None:
            return JsonResponse({"url": icon.svg.url})
        else:
            return JsonResponse({"detail": "Icon not found."}, status=404)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxClusterIcon, self).dispatch(request, *args, **kwargs)


class AjaxLoadIndicatorIcon(View):
    """Ajax - Upload a example of icon for Upload Indicator to admin panel."""

    def get(self, request, *args, **kwargs):
        icon_id = request.GET.get("obj_id")
        icon = LoadIndicator.objects.filter(pk=icon_id).first()

        if icon is not None:
            return JsonResponse({"url": icon.svg.url})
        else:
            return JsonResponse({"detail": "Icon not found."}, status=404)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxLoadIndicatorIcon, self).dispatch(request, *args, **kwargs)


class AjaxCollectionExampleIcon(View):
    """Ajax - Upload a example of cluster icon to admin panel."""

    def get(self, request, *args, **kwargs):
        collection_id = request.GET.get("obj_id")
        icon = MarkerIcon.objects.filter(
            icon_collection__pk=collection_id).first()

        if icon is not None:
            return JsonResponse({"url": icon.svg.url})
        else:
            return JsonResponse({"detail": "Icon not found."}, status=404)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxCollectionExampleIcon, self).dispatch(request, *args, **kwargs)


class AjaxTileScreenshot(View):
    """Ajax - Upload a example of screenshot of the tile to admin panel."""

    def get(self, request, *args, **kwargs):
        source_id = request.GET.get("obj_id")
        tile_source = TileSource.objects.filter(pk=source_id).first()

        if tile_source is not None:
            return JsonResponse({"url": tile_source.screenshot.url})
        else:
            return JsonResponse({"detail": "Screenshot not found."}, status=404)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxTileScreenshot, self).dispatch(request, *args, **kwargs)


class AjaxIconCollection(View):
    """Ajax - Upload icon collection for custom marker."""

    def get(self, request, *args, **kwargs):
        map_id = int(request.GET.get('mapID'))
        icon_collection = Map.objects.get(
            pk=map_id).icon_collection.icons.filter(active=True)

        if icon_collection:
            icon_collection = [{"url": item.svg.url, "slug": item.slug}
                               for item in icon_collection]
            return JsonResponse({"iconCollection": icon_collection})
        else:
            return JsonResponse({"detail": "Icon Collection not found."}, status=404)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxIconCollection, self).dispatch(request, *args, **kwargs)


# SAVING CHANGES -----------------------------------------------------------------------------------
class AjaxUpdateTileSource(View):
    """Ajax - Tile source replacement."""

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('mapID')
        tile_id = int(request.POST.get('tileID'))

        ymap = Map.objects.get(pk=map_id)
        ymap.tile = TileSource.objects.get(pk=tile_id) if tile_id > 0 else None
        ymap.save()

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxUpdateTileSource, self).dispatch(request, *args, **kwargs)


class AjaxUpdateLoadIndicator(View):
    """Ajax - Change the Load Indicator."""

    def post(self, request, *args, **kwargs):
        map_id = int(request.POST.get('mapID'))
        slug = force_text(request.POST.get('slug'))
        size = int(request.POST.get('size'))
        speed = request.POST.get('speed')
        animation = request.POST.get('animation')

        ymap = Map.objects.get(pk=map_id)
        ymap.load_indicator = LoadIndicator.objects.filter(slug=slug).first()
        ymap.load_indicator_size = size
        ymap.animation_speed = speed
        ymap.disable_indicator_animation = eval(animation)
        ymap.save()

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxUpdateLoadIndicator, self).dispatch(request, *args, **kwargs)


class AjaxUpdateGeneralSettings(View):
    """Ajax - Update general settings."""

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('ymap')
        ymap = Map.objects.get(pk=map_id)
        img_bg_panel_front_b64 = request.POST.get('img_bg_panel_front_b64', "")
        form = GeneralSettingsForm(
            request.POST, instance=ymap.general_settings)

        if form.is_valid():
            instance = form.save(commit=False)
            if len(img_bg_panel_front_b64) > 0:
                img_bg_panel_front_b64 = img_bg_panel_front_b64.split(',')[1]
                instance.img_bg_panel_front = ContentFile(
                    base64.b64decode(img_bg_panel_front_b64), 'pic.jpg')
            instance.save()
        else:
            response_data = {'detail': get_errors_form(form)['detail']}
            return JsonResponse(response_data, status=400)

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxUpdateGeneralSettings, self).dispatch(request, *args, **kwargs)


class AjaxDeleteImgBgPanelFront(View):
    """Ajax - Delete the background image for the panel."""

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('mapID')
        ymap = Map.objects.get(pk=map_id)
        general_settings = ymap.general_settings
        general_settings.img_bg_panel_front = None
        general_settings.save()

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxDeleteImgBgPanelFront, self).dispatch(request, *args, **kwargs)


class AjaxUpdateMapControls(View):
    """Ajax - Update Map controls."""

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('ymap')
        map_controls = Map.objects.get(pk=map_id).map_controls
        form = MapControlsForm(request.POST, instance=map_controls)

        if form.is_valid():
            form.save()
        else:
            response_data = {'detail': get_errors_form(form)['detail']}
            return JsonResponse(response_data, status=400)

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxUpdateMapControls, self).dispatch(request, *args, **kwargs)


class AjaxUpdateHeatmapSettings(View):
    """Ajax - Update Heatmap settings."""

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
        return super(AjaxUpdateHeatmapSettings, self).dispatch(request, *args, **kwargs)


class AjaxUpdatePresetSettings(View):
    """Ajax - Update Preset settings."""

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('ymap')
        preset_id = request.POST.get('presetID')
        ymap = Map.objects.get(pk=map_id)
        preset = Preset.objects.get(pk=preset_id, ymap=ymap)
        form = PresetForm(request.POST, instance=preset)

        if form.is_valid():
            form.save()
        else:
            response_data = {'detail': get_errors_form(form)['detail']}
            return JsonResponse(response_data, status=400)

        presets = ymap.presets.all()
        presets = [{
            'id': item.pk,
            'title': item.title,
            'icon': item.icon,
            'description': item. description,
            'autoheader': item.autoheader,
            'autobody': item.autobody,
            'autofooter': item.autofooter,
            'placemark': item.placemark,
            'polyline': item.polyline,
            'polygon': item.polygon,
            'position': item.position
        } for item in presets]

        response_data = {'presets': presets}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxUpdatePresetSettings, self).dispatch(request, *args, **kwargs)


class AjaxUpdateFiltersCategories(View):
    """Ajax - Update filters of categories"""

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('mapID')
        json_categories = request.POST.get('jsonCategories')

        json_settings = JsonSettings.objects.get(ymap__pk=map_id)
        editor = json.loads(json_settings.editor)
        editor['categories'] = json.loads(json_categories)
        save_json_settings(json_settings, editor)

        response_data = {'successfully': True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxUpdateFiltersCategories, self).dispatch(request, *args, **kwargs)


# GETTING AND UPDATING - LIKES | DISLIKES ----------------------------------------------------------
class AjaxUpdateLikes(View):
    """Ajax - Getting and updating likes;dislikes."""

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
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(AjaxUpdateLikes, self).dispatch(request, *args, **kwargs)


# HEATMAP - ACTIVATE | RESET -----------------------------------------------------------------------
class AjaxActivateHeatmap(View):
    """Ajax - Activate Heatmap."""

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
    """Ajax - Heatmap, reset to default settings."""

    def post(self, request, *args, **kwargs):
        map_id = request.POST.get('map_id')
        heatmap_settings = Map.objects.get(pk=map_id).heatmap_settings

        heatmap_settings.radius = 10
        heatmap_settings.dissipating = False
        heatmap_settings.opacity = '0.8'
        heatmap_settings.intensity = '0.2'
        heatmap_settings.gradient_color1 = '#66BB6A'
        heatmap_settings.gradient_color2 = '#FDD835'
        heatmap_settings.gradient_color3 = '#EF5350'
        heatmap_settings.gradient_color4 = '#B71C1C'
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


# IMPORT | EXPORT ----------------------------------------------------------------------------------
# (Icon Collections and Tile Sources)
class AjaxImportIconCollection(View):
    """Ajax - Import icon collection from the json file to the database."""

    def post(self, request, *args, **kwargs):
        with request.FILES.get('collection').file as json_file:
            collection_json = json_file.read()

        collection_json = json.loads(collection_json.decode('utf-8'))
        title = collection_json['title']

        if IconCollection.objects.filter(slug=slugify(title)).count() != 0:
            msg = _('The {} collection already exists.')
            response_data = {'detail': msg.format(title)}
            return JsonResponse(response_data, status=400)

        collection = IconCollection.objects.create(title=title)
        icons = collection_json['icons']

        for icon in icons:
            with io.BytesIO(icon['svg'].encode('utf-8')) as svg:
                marker_icon = MarkerIcon.objects.create(
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
    """Export a icon collection from a database to a json file."""

    def dispatch(self, request, *args, **kwargs):
        slug = force_text(kwargs.get("slug"))
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
    """Import tile sources from json file to database."""

    def post(self, request, *args, **kwargs):
        with request.FILES.get('sources').file as json_file:
            source_list = json_file.read()

        source_list = json.loads(source_list.decode('utf-8'))

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
    """Export tile sources from a database to a json file."""

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
