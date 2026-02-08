"""Apps."""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjeymConfig(AppConfig):  # noqa: D101
    name = "djeym"
    verbose_name = _("Yandex maps")
