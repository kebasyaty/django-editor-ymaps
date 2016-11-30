# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse

from .utils import get_errors_form

from .models import Map, Placemark, Polyline, Polygon, CustomIcon
from .forms import PlacemarkForm, PolylineForm, PolygonForm


def editor_load_ymap(request, slug=None):

    user = request.user

    if user.is_authenticated() and user.is_staff:

        if slug is not None:

            try:
                ymap = Map.objects.get(slug=slug, active=True)
                custom_icons = CustomIcon.objects.filter(active=True)
            except Map.DoesNotExist:
                ymap = custom_icons = None

            return render(request, 'yandex_maps/ymap_editor.html', {
                'ymap': ymap,
                'custom_icons': custom_icons
            })

    return redirect('home')


def load_geoobjects(request):

    if request.is_ajax():

        data = {'success': True}

        try:
            current_map = Map.objects.get(pk=request.GET['id_map'])

            collections = {
                'placemark': serializers.serialize('json', current_map.category_placemark.filter(active=True)
                                                   .only('id', 'title'), fields=('id', 'title')),
                'submark': serializers.serialize('json', current_map.subcategory.filter(active=True)
                                                 .only('id', 'title'), fields=('id', 'title')),
                'polyline': serializers.serialize('json', current_map.category_polyline.filter(active=True)
                                                  .only('id', 'title'), fields=('id', 'title')),
                'polygon': serializers.serialize('json', current_map.category_polygon.filter(active=True)
                                                 .only('id', 'title'), fields=('id', 'title'))
            }

            geoobjects = {
                'placemarks': serializers.serialize('json', current_map.placemark_map.filter(active=True)
                                                    .only('id', 'category', 'subcategory', 'icon_content',
                                                          'hint_content', 'balloon_content', 'icon_name',
                                                          'color', 'coordinates'),
                                                    fields=('id', 'category', 'subcategory', 'icon_content',
                                                            'hint_content', 'balloon_content', 'icon_name',
                                                            'color', 'coordinates')),
                'polylines': serializers.serialize('json', current_map.polyline_map.filter(active=True)
                                                   .only('id', 'category', 'hint_content', 'balloon_content',
                                                         'stroke_width', 'stroke_color', 'stroke_opacity',
                                                         'coordinates'),
                                                   fields=('id', 'category', 'hint_content', 'balloon_content',
                                                           'stroke_width', 'stroke_color', 'stroke_opacity',
                                                           'coordinates')),
                'polygons': serializers.serialize('json', current_map.polygon_map.filter(active=True)
                                                  .only('id', 'category', 'hint_content', 'balloon_content',
                                                        'stroke_width', 'stroke_color', 'stroke_opacity',
                                                        'fill_color', 'fill_opacity', 'coordinates'),
                                                  fields=('id', 'category', 'hint_content', 'balloon_content',
                                                          'stroke_width', 'stroke_color', 'stroke_opacity',
                                                          'fill_color', 'fill_opacity', 'coordinates'))
            }

        except Map.DoesNotExist:
            collections = geoobjects = None
            data['success'] = False

        data['collections'] = collections
        data['geoobjects'] = geoobjects

        return JsonResponse(data)

    return redirect('home')


def save_geoobject(request):

    if request.is_ajax():
        data = {'success': False}

        pk = int(request.GET.get('pk', None))
        geo_type = request.GET.get('geo_type', None)
        action = request.GET.get('action', None)

        if geo_type == 'placemark':

            if action == 'save':

                if pk:
                    form = PlacemarkForm(request.GET,  instance=Placemark.objects.get(id=pk))
                else:
                    form = PlacemarkForm(request.GET)

                if form.is_valid():
                    placemark = form.save()
                    data['placemark'] = serializers.serialize('json', [placemark])
                    data['success'] = True
                else:
                    data['err_txt'] = get_errors_form(form)['err_txt']

            elif action == 'reload':
                if pk:
                    data['placemark'] = serializers.serialize('json', [Placemark.objects.get(id=pk)])

                data['success'] = True

            elif action == 'delete':
                Placemark.objects.get(id=pk).delete()
                data['success'] = True

        elif geo_type == 'polyline':

            if action == 'save':

                if pk:
                    form = PolylineForm(request.GET,  instance=Polyline.objects.get(id=pk))
                else:
                    form = PolylineForm(request.GET)

                if form.is_valid():
                    polyline = form.save()
                    data['polyline'] = serializers.serialize('json', [polyline])
                    data['success'] = True
                else:
                    data['err_txt'] = get_errors_form(form)['err_txt']

            elif action == 'reload':
                if pk:
                    data['polyline'] = serializers.serialize('json', [Polyline.objects.get(id=pk)])

                data['success'] = True

            elif action == 'delete':
                Polyline.objects.get(id=pk).delete()
                data['success'] = True

        elif geo_type == 'polygon':

            if action == 'save':

                if pk:
                    form = PolygonForm(request.GET,  instance=Polygon.objects.get(id=pk))
                else:
                    form = PolygonForm(request.GET)

                if form.is_valid():
                    polygon = form.save()
                    data['polygon'] = serializers.serialize('json', [polygon])
                    data['success'] = True
                else:
                    data['err_txt'] = get_errors_form(form)['err_txt']

            elif action == 'reload':
                if pk:
                    data['polygon'] = serializers.serialize('json', [Polygon.objects.get(id=pk)])

                data['success'] = True

            elif action == 'delete':
                Polygon.objects.get(id=pk).delete()
                data['success'] = True

        return JsonResponse(data)

    return redirect('home')
