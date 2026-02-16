"""Mixins."""

from __future__ import annotations

import uuid
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from PIL import Image


class StaffRequiredMixin:
    """Mixin which requires that the authenticated user is a staff member (i.e. `is_staff` is True)."""

    # login_required(redirect_field_name='next', login_url=None)  # noqa: ERA001
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if not request.user.is_staff:
            messages.error(request, _("You do not have the permission required to perform the requested operation."))
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)


class ResizeImageMixin:
    def resize(self, image_field: models.ImageField, max_size: tuple[int, int]):  # noqa: D102
        extension = Path(image_field.name).suffix.lower()  # pyrefly: ignore[bad-argument-type]
        img = Image.open(image_field)  # Catch original # pyrefly: ignore[bad-argument-type]
        source_image = img.convert("RGB")
        source_image.thumbnail(max_size)  # Resize to size
        output = BytesIO()
        format = "PNG" if extension == ".png" else "JPEG"
        source_image.save(output, format=format)  # Save resize image to bytes
        output.seek(0)

        content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
        file = File(content_file)

        random_name = f"{uuid.uuid4()}{extension}"
        image_field.save(random_name, file, save=False)
