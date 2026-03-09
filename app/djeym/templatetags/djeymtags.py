"""DjEYM Tags."""

from __future__ import annotations

from django import template
from django.conf import settings

from ..models import Map

register = template.Library()

YANDEX_MAPS_API_VERSION = "2.1"

BOOTSTRAP_VERSION = "5.3.8"


# Load data of model Map to site page
# ------------------------------------------------------------------------------
@register.inclusion_tag("djeym/includes/ymaps_site.html")
def djeym_yandex_map(slug, lang="en"):
    """Load data of model Map to site page."""
    ymap = Map.objects.filter(slug=slug, active=True).first()
    ctx = {"ymap": ymap}

    if ymap is not None:
        general_settings = ymap.general_settings
        ctx["lang"] = (lang or "en",)
        ctx["is_heatmap"] = ymap.heatmap_settings.active
        ctx["width_map"] = general_settings.width_map_site
        ctx["height_map"] = general_settings.height_map_site

    return ctx


# Load URL for API Yandex Maps
# ------------------------------------------------------------------------------
@register.inclusion_tag("djeym/includes/api_ymaps.html")
def djeym_load_api_ymaps(lang="en", ns="djeymYMaps"):
    """Load URL for API Yandex Maps."""
    api_version = YANDEX_MAPS_API_VERSION
    api_key = getattr(settings, "DJEYM_YMAPS_API_KEY", "")
    is_enterprise = getattr(settings, "DJEYM_YMAPS_API_KEY_FOR_ENTERPRISE", False)
    mode = getattr(settings, "DJEYM_YMAPS_DOWNLOAD_MODE", "release")
    lang = lang[:2].lower() if bool(lang) else "en"

    if lang == "ru":
        lang += "_RU"
    elif lang == "en":
        lang += "_US"
    elif lang == "uk":
        lang += "_UA"
    elif lang == "tr":
        lang += "_TR"
    else:
        lang = "en_US"

    return {
        "api_key": api_key,
        "is_enterprise": is_enterprise,
        "api_version": api_version,
        "lang": lang,
        "mode": mode,
        "ns": ns,
    }


# Vendors - Icons, CSS and JS
# ------------------------------------------------------------------------------
@register.inclusion_tag("djeym/includes/vendor_md_icons.html")
def djeym_load_vendor_md_icons():
    """Load URL vendor of Material Design Icons."""
    return {"mdi_version": settings.MD_ICONS_VERSION}


@register.inclusion_tag("djeym/includes/vendor_bootstrap_css.html")
def djeym_load_vendor_bootstrap_css():
    """CSS vendor of Bootstrap."""
    return {"version": BOOTSTRAP_VERSION}


@register.inclusion_tag("djeym/includes/vendor_bootstrap_js.html")
def djeym_load_vendor_bootstrap_js():
    """JavaSscript vendor of Bootstrap."""
    return {"version": BOOTSTRAP_VERSION}
