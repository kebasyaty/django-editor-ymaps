"""Views."""

from __future__ import annotations

import base64
import copy
import io
import json
from pathlib import Path

from django.core.files import File
from django.core.files.base import ContentFile
from django.http import FileResponse, HttpResponse, HttpResponseForbidden, JsonResponse
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, View
from ipware import get_client_ip
from slugify import slugify

from .decorators import ajax_login_required_and_staff
from .forms import (
    BanIPForm,
    CustomPlacemarkForm,
    GeneralSettingsForm,
    HeatmapSettingsForm,
    HeatPointForm,
    MapControlsForm,
    PlacemarkForm,
    PolygonForm,
    PolylineForm,
)
from .mixins import StaffRequiredMixin
from .models import (
    BannedIP,
    ClusterIcon,
    HeatPoint,
    IconCollection,
    Map,
    MarkerIcon,
    Placemark,
    Polygon,
    Polyline,
)
from .utils import get_errors_form


# UPLOADING BALLOON CONTENT
# ------------------------------------------------------------------------------
class AjaxBalloonContent(View):
    """Ajax - Upload Balloon Content."""

    def get(self, request, *args, **kwargs):  # noqa: D102
        response_data = {}
        pk = request.GET.get("objID")
        obj_type = request.GET.get("objType")
        ids = request.GET.get("ids")

        if ids is None:
            if obj_type == "Point":
                geoobject = Placemark.objects.filter(id=pk).only("header", "image", "footer").first()
            elif obj_type == "LineString":
                geoobject = Polyline.objects.filter(id=pk).only("header", "image", "footer").first()
            elif obj_type == "Polygon":
                geoobject = Polygon.objects.filter(id=pk).only("header", "image", "footer").first()

            response_data = {
                "header": mark_safe(geoobject.header),  # noqa: S308 # pyrefly: ignore[unbound-name]
                "body": geoobject.image.url,  # pyrefly: ignore[unbound-name]
                "footer": mark_safe(geoobject.footer),  # noqa: S308 # pyrefly: ignore[unbound-name]
            }
        else:
            ids = json.loads(ids)
            placemarks = Placemark.objects.filter(id__in=ids)

            for placemark in placemarks:
                response_data[placemark.pk] = {
                    "header": mark_safe(placemark.header),  # noqa: S308
                    "body": placemark.image.url,
                    "footer": mark_safe(placemark.footer),  # noqa: S308
                }

        return JsonResponse(response_data)

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


# UPLOADING GEO OBJECTS
# ------------------------------------------------------------------------------
class AjaxUploadPlacemarks(View):
    """Ajax - Upload placemarks to map."""

    def get(self, request, *args, **kwargs):  # noqa: D102
        map_id = int(request.GET.get("mapID"))
        offset = int(request.GET.get("offset"))
        limit = offset + 1000

        geoobjects = Placemark.objects.filter(ymap__pk=map_id, active=True).values_list("json_code", flat=True)[
            offset:limit
        ]

        response_data = "[" + ",".join(geoobjects) + "]"

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class AjaxUploadHeatPoints(View):
    """Ajax - Upload heat points to map."""

    def get(self, request, *args, **kwargs):  # noqa: D102
        map_id = int(request.GET.get("mapID"))
        offset = int(request.GET.get("offset"))
        limit = offset + 1000

        geoobjects = HeatPoint.objects.filter(ymap__pk=map_id, active=True).values_list("json_code", flat=True)[
            offset:limit
        ]

        response_data = "[" + ",".join(geoobjects) + "]"

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class AjaxUploadPolylines(View):
    """Ajax - Upload polylines to map."""

    def get(self, request, *args, **kwargs):  # noqa: D102
        map_id = int(request.GET.get("mapID"))
        offset = int(request.GET.get("offset"))
        limit = offset + 500

        geoobjects = Polyline.objects.filter(ymap__pk=map_id, active=True).values_list("json_code", flat=True)[
            offset:limit
        ]

        response_data = "[" + ",".join(geoobjects) + "]"

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class AjaxUploadPolygons(View):
    """Ajax - Upload polygons to map."""

    def get(self, request, *args, **kwargs):  # noqa: D102
        map_id = int(request.GET.get("mapID"))
        offset = int(request.GET.get("offset"))
        limit = offset + 500

        geoobjects = Polygon.objects.filter(ymap__pk=map_id, active=True).values_list("json_code", flat=True)[
            offset:limit
        ]

        response_data = "[" + ",".join(geoobjects) + "]"

        return HttpResponse(response_data, content_type="application/json")

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


# LOADING MAP TO EDITOR PAGE
# ------------------------------------------------------------------------------
class YMapEditor(StaffRequiredMixin, TemplateView):
    """Load map to editor page."""

    template_name = "djeym/ymaps_editor.html"

    def get_context_data(self, **kwargs):  # noqa: D102
        slug = force_str(kwargs.get("slug"))
        ymap = Map.objects.filter(slug=slug, active=True).first()
        context = super().get_context_data(**kwargs)

        if ymap is not None:
            settings = ymap.general_settings
            heatmap_settings = ymap.heatmap_settings

            context["settings"] = settings
            context["is_dark_theme"] = settings.theme_type == "dark"
            context["map_controls"] = ymap.map_controls
            context["heatmap_settings"] = heatmap_settings
            context["is_heatmap"] = heatmap_settings.active

        context["ymap"] = ymap
        return context


# GEO-OBJECTS - SAVING | UPDATING | DELETING
# ------------------------------------------------------------------------------
class AjaxSaveGeoObjects(View):
    """Geo-objects - saving, updating and deleting."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        pk = int(request.POST.get("pk"))
        geo_type = request.POST.get("geoType")
        action = request.POST.get("action")

        # Heatpoint
        if geo_type == "heatpoint":
            if action == "save":
                if pk:
                    form = HeatPointForm(request.POST, instance=HeatPoint.objects.get(id=pk))
                else:
                    form = HeatPointForm(request.POST)

                if form.is_valid():
                    heatpoint = form.save()
                    response_data = "[" + heatpoint.json_code + "]"
                else:
                    response_data = {"detail": get_errors_form(form)["detail"]}
                    return JsonResponse(response_data, status=400)

            elif action == "reload":
                json_code = HeatPoint.objects.get(pk=pk).json_code
                response_data = "[" + json_code + "]"

            elif action == "delete":
                HeatPoint.objects.get(id=pk).delete()
                response_data = "[]"

        # Placemark
        elif geo_type == "placemark":
            if action == "save":
                if pk:
                    form = PlacemarkForm(request.POST, instance=Placemark.objects.get(id=pk))
                else:
                    form = PlacemarkForm(request.POST)

                if form.is_valid():
                    placemark = form.save()
                    response_data = "[" + placemark.json_code + "]"
                else:
                    response_data = {"detail": get_errors_form(form)["detail"]}
                    return JsonResponse(response_data, status=400)

            elif action == "reload":
                json_code = Placemark.objects.get(pk=pk).json_code
                response_data = "[" + json_code + "]"

            elif action == "delete":
                Placemark.objects.get(id=pk).delete()
                response_data = "[]"

        # Polyline
        elif geo_type == "polyline":
            if action == "save":
                if pk:
                    form = PolylineForm(request.POST, instance=Polyline.objects.get(id=pk))
                else:
                    form = PolylineForm(request.POST)

                if form.is_valid():
                    polyline = form.save()
                    response_data = "[" + polyline.json_code + "]"
                else:
                    response_data = {"detail": get_errors_form(form)["detail"]}
                    return JsonResponse(response_data, status=400)

            elif action == "reload":
                json_code = Polyline.objects.get(pk=pk).json_code
                response_data = "[" + json_code + "]"

            elif action == "delete":
                Polyline.objects.get(id=pk).delete()
                response_data = "[]"

        # Polygon
        elif geo_type == "polygon":
            if action == "save":
                if pk:
                    form = PolygonForm(request.POST, instance=Polygon.objects.get(id=pk))
                else:
                    form = PolygonForm(request.POST)

                if form.is_valid():
                    polygon = form.save()
                    response_data = "[" + polygon.json_code + "]"
                else:
                    response_data = {"detail": get_errors_form(form)["detail"]}
                    return JsonResponse(response_data, status=400)

            elif action == "reload":
                json_code = Polygon.objects.get(pk=pk).json_code
                response_data = "[" + json_code + "]"

            elif action == "delete":
                Polygon.objects.get(id=pk).delete()
                response_data = "[]"

        return HttpResponse(response_data, content_type="application/json")  # pyrefly: ignore[unbound-name]

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


class AjaxSaveCusotmMarker(View):
    """Ajax - Save cusotm marker."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        client_ip, is_routable = get_client_ip(request)  # noqa: RUF059

        if BannedIP.objects.filter(ip=client_ip).count() == 0:
            form = CustomPlacemarkForm(request.POST)

            if form.is_valid():
                marker = form.save(commit=False)
                marker.user_ip = client_ip
                marker.user_image = request.FILES.get("user_image", None)
                marker.save()
                form.save_m2m()
            else:
                response_data = {"detail": get_errors_form(form)["detail"]}
                return JsonResponse(response_data, status=400)

        response_data = {"Success": True}
        return JsonResponse(response_data)


# BAN IP ADDRESSES
# ------------------------------------------------------------------------------
class AjaxBanIPAddress(View):
    """Ajax - Ban ip address."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        form = BanIPForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            response_data = {"detail": get_errors_form(form)["detail"]}
            return JsonResponse(response_data, status=400)

        response_data = {"Success": True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


# UPLOADING - SCREENSHOTS, EXAMPLE ICON, ICON COLLECTION
# ------------------------------------------------------------------------------
# (For admin panel.)
class AjaxClusterIcon(View):
    """Ajax - Upload a example of cluster icon to admin panel."""

    def get(self, request, *args, **kwargs):  # noqa: D102
        icon_id = request.GET.get("obj_id")
        icon = ClusterIcon.objects.filter(pk=icon_id).first()

        if icon is not None:
            return JsonResponse({"url": icon.svg.url})
        else:  # noqa: RET505
            return JsonResponse({"detail": "Icon not found."}, status=404)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


class AjaxCollectionExampleIcon(View):
    """Ajax - Upload a example of cluster icon to admin panel."""

    def get(self, request, *args, **kwargs):  # noqa: D102
        collection_id = request.GET.get("obj_id")
        icon = MarkerIcon.objects.filter(icon_collection__pk=collection_id).first()

        if icon is not None:
            return JsonResponse({"url": icon.svg.url})
        else:  # noqa: RET505
            return JsonResponse({"detail": "Icon not found."}, status=404)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


class AjaxIconCollection(View):
    """Ajax - Upload icon collection for custom marker."""

    def get(self, request, *args, **kwargs):  # noqa: D102
        map_id = int(request.GET.get("mapID"))
        icon_collection = Map.objects.get(pk=map_id).icon_collection.icons.filter(active=True)

        if icon_collection:
            icon_collection = [{"url": item.svg.url, "slug": item.slug} for item in icon_collection]
            return JsonResponse({"iconCollection": icon_collection})
        else:  # noqa: RET505
            return JsonResponse({"detail": "Icon Collection not found."}, status=404)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


# SAVING CHANGES
# ------------------------------------------------------------------------------
class AjaxUpdateGeneralSettings(View):
    """Ajax - Update general settings."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        map_id = request.POST.get("ymap")
        ymap = Map.objects.get(pk=map_id)
        img_bg_panel_site_b64 = request.POST.get("img_bg_panel_site_b64", "")
        form = GeneralSettingsForm(request.POST, instance=ymap.general_settings)

        if form.is_valid():
            instance = form.save(commit=False)
            if len(img_bg_panel_site_b64) > 0:
                img_bg_panel_site_b64 = img_bg_panel_site_b64.split(",")[1]
                instance.img_bg_panel_site = ContentFile(base64.b64decode(img_bg_panel_site_b64), "pic.jpg")
            instance.save()
        else:
            response_data = {"detail": get_errors_form(form)["detail"]}
            return JsonResponse(response_data, status=400)

        response_data = {"successfully": True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


class AjaxDeleteImgBgPanelSite(View):
    """Ajax - Delete the background image for the panel."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        map_id = request.POST.get("mapID")
        ymap = Map.objects.get(pk=map_id)
        general_settings = ymap.general_settings
        general_settings.img_bg_panel_site = None
        general_settings.save()

        response_data = {"successfully": True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


class AjaxUpdateMapControls(View):
    """Ajax - Update Map controls."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        map_id = request.POST.get("ymap")
        map_controls = Map.objects.get(pk=map_id).map_controls
        form = MapControlsForm(request.POST, instance=map_controls)

        if form.is_valid():
            form.save()
        else:
            response_data = {"detail": get_errors_form(form)["detail"]}
            return JsonResponse(response_data, status=400)

        response_data = {"successfully": True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


class AjaxUpdateHeatmapSettings(View):
    """Ajax - Update Heatmap settings."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        map_id = request.POST.get("ymap")
        ymap = Map.objects.get(pk=map_id)
        form = HeatmapSettingsForm(request.POST, instance=ymap.heatmap_settings)

        if form.is_valid():
            form.save()
        else:
            response_data = {"detail": get_errors_form(form)["detail"]}
            return JsonResponse(response_data, status=400)

        response_data = {"successfully": True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


# HEATMAP - ACTIVATE | RESET
# ------------------------------------------------------------------------------
class AjaxActivateHeatmap(View):
    """Ajax - Activate Heatmap."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        map_id = request.POST.get("mapID")
        heatmap_bool = request.POST.get("heatmap")
        external_modules = Map.objects.get(pk=map_id).external_modules

        external_modules.heatmap = heatmap_bool
        external_modules.save()

        response_data = {"successfully": True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


class AjaxHeatmapUndoSettings(View):
    """Ajax - Heatmap, reset to default settings."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        map_id = request.POST.get("map_id")
        heatmap_settings = Map.objects.get(pk=map_id).heatmap_settings

        heatmap_settings.radius = 10
        heatmap_settings.dissipating = False
        heatmap_settings.opacity = "0.8"
        heatmap_settings.intensity = "0.2"
        heatmap_settings.gradient_color1 = "#66BB6A"
        heatmap_settings.gradient_color2 = "#FDD835"
        heatmap_settings.gradient_color3 = "#EF5350"
        heatmap_settings.gradient_color4 = "#B71C1C"
        heatmap_settings.save()

        response_data = {
            "radius": int(heatmap_settings.radius),
            "dissipating": heatmap_settings.dissipating,
            "opacity": float(heatmap_settings.opacity),
            "intensityOfMidpoint": float(heatmap_settings.intensity),
            "gradient_color1": heatmap_settings.gradient_color1,
            "gradient_color2": heatmap_settings.gradient_color2,
            "gradient_color3": heatmap_settings.gradient_color3,
            "gradient_color4": heatmap_settings.gradient_color4,
        }
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


# IMPORT | EXPORT - Icon Collections
# ------------------------------------------------------------------------------
class AjaxImportIconCollection(View):
    """Ajax - Import icon collection from the json file to the database."""

    def post(self, request, *args, **kwargs):  # noqa: D102
        with request.FILES.get("collection").file as json_file:
            collection_json = json_file.read()

        collection_json = json.loads(collection_json.decode("utf-8"))
        title = collection_json["title"]

        if IconCollection.objects.filter(slug=slugify(title)).count() != 0:
            msg = _("The {} collection already exists.")
            response_data = {"detail": msg.format(title)}
            return JsonResponse(response_data, status=400)

        collection = IconCollection.objects.create(title=title)
        icons = collection_json["icons"]

        for icon in icons:
            with io.BytesIO(icon["svg"].encode("utf-8")) as svg:
                marker_icon = MarkerIcon.objects.create(
                    icon_collection=collection,
                    title=icon["title"],
                    size_width=icon["size_width"],
                    size_height=icon["size_height"],
                    offset_x=icon["offset_x"],
                    offset_y=icon["offset_y"],
                )
                marker_icon.svg.save("icon.svg", File(svg))

        response_data = {"successfully": True}
        return JsonResponse(response_data)

    @ajax_login_required_and_staff
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


class ExportIconCollection(StaffRequiredMixin, View):
    """Export a icon collection from a database to a json file."""

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        slug = force_str(kwargs.get("slug"))
        collection = IconCollection.objects.get(slug=slug)
        icons = collection.icons.all()
        collection_json = {"title": collection.title, "icons": []}
        raw_icon_json = {"title": "", "svg": "", "size_width": 0, "size_height": 0, "offset_x": ".0", "offset_y": ".0"}

        for icon in icons:
            svg = Path(icon.svg.path).read_text(encoding="utf-8")
            icon_json = copy.deepcopy(raw_icon_json)
            icon_json["title"] = icon.title
            icon_json["svg"] = svg
            icon_json["size_width"] = icon.size_width
            icon_json["size_height"] = icon.size_height
            icon_json["offset_x"] = str(icon.offset_x)
            icon_json["offset_y"] = str(icon.offset_y)
            collection_json["icons"].append(icon_json)

        collection_json = json.dumps(collection_json, ensure_ascii=False).encode("utf-8")
        stream = io.BytesIO(collection_json)
        response = FileResponse(stream, content_type="application/json")
        response["Content-Disposition"] = "attachment; filename={}.json".format(slug.replace("-", "_"))
        return response
