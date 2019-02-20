# -*- coding: utf-8 -*-
from functools import wraps

from django.http import HttpResponseForbidden, JsonResponse


def ajax_login_required(view_func):
    """
    Ajax.
    Class-based views - dispatch.
    Verify that the current user is authenticated.
    """
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        if request.user.is_authenticated:
            return view_func(self, request, *args, **kwargs)
        msg = {'detail': 'HTTP 403 Forbidden'}
        return JsonResponse(msg, status=403)
    return wrapper


def ajax_login_required_and_staff(view_func):
    """
    Ajax.
    Class-based views - dispatch.
    Verify that the current user is authenticated.
    """
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user
        if not request.is_ajax():
            return HttpResponseForbidden()
        if user.is_authenticated and user.is_staff:
            return view_func(self, request, *args, **kwargs)
        msg = {'detail': 'HTTP 403 Forbidden'}
        return JsonResponse(msg, status=403)
    return wrapper
