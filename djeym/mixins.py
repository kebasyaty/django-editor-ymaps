# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _


class StaffRequiredMixin:
    """
    Mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True).
    """
    # login_required(redirect_field_name='next', login_url=None)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request,
                _('You do not have the permission required to perform the requested operation.'))
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
