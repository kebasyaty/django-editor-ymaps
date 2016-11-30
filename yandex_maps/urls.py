# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'yandex_maps.views',
    url(r'load_geoobjects/$', 'load_geoobjects', name='load_geoobjects'),
    url(r'save_geoobject/$', 'save_geoobject', name='save_geoobject'),
    url(r'editor/(?P<slug>[-_\w]+)/$', 'editor_load_ymap', name='ymap'),
)
