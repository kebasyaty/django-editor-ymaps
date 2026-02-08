"""Middleware."""

from __future__ import annotations


class AjaxMiddleware:  # noqa: D101
    def __init__(self, get_response):  # noqa: D107
        self.get_response = get_response

    def __call__(self, request):  # noqa: D102
        def is_ajax(self):  # noqa: ARG001
            return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"

        request.is_ajax = is_ajax.__get__(request)
        return self.get_response(request)
