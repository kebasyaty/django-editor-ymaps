# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

# Maximum size of icons for markers and clusters.
DJEYM_YMAPS_ICONS_MAX_SIZE = 60

ZOOM_CHOICES = [(num, num) for num in range(24)]

# Load indicator animation speed
ANIMATION_SPEED = (
    ('0.3', '0.3'),
    ('0.4', '0.4'),
    ('0.5', '0.5'),
    ('0.6', '0.6'),
    ('0.7', '0.7'),
    ('0.8', '0.8'),
    ('0.9', '0.9'),
    ('1', '1'),
    ('1.1', '1.1'),
    ('1.2', '1.2'),
    ('1.3', '1.3'),
    ('1.4', '1.4'),
    ('1.5', '1.5'),
    ('1.6', '1.6'),
    ('1.7', '1.7'),
    ('1.8', '1.8'),
)

TRANSPARENCY_CHOICES = (
    ('0', '0'),
    ('0.1', '0.1'),
    ('0.2', '0.2'),
    ('0.3', '0.3'),
    ('0.4', '0.4'),
    ('0.5', '0.5'),
    ('0.6', '0.6'),
    ('0.7', '0.7'),
    ('0.8', '0.8'),
    ('0.9', '0.9'),
    ('1', '1')
)

COLORS = (
    '#F44336', '#C62828', '#E91E63', '#AD1457', '#9C27B0',
    '#6A1B9A', '#673AB7', '#4527A0', '#3F51B5', '#283593',
    '#2196F3', '#1565C0', '#0091EA', '#03A9F4', '#0277BD',
    '#00BCD4', '#00838F', '#009688', '#00695C', '#4CAF50',
    '#2E7D32', '#00C853', '#8BC34A', '#558B2F', '#CDDC39',
    '#9E9D24', '#FFEB3B', '#F9A825', '#FFC107', '#FF8F00',
    '#FF9800', '#EF6C00', '#FF5722', '#D84315', '#795548',
    '#4E342E', '#607D8B', '#37474F', '#FAFAFA', '#F5F5F5',
    '#EEEEEE', '#E0E0E0', '#BDBDBD', '#9E9E9E', '#757575',
    '#616161', '#424242', '#212121', '#000000', '#FFFFFF'
)

STROKE_STYLE_CHOICES = (
    ('solid', _('Solid line')),
    ('dash', _('Dash')),
    ('dashdot', _('Long dash-short dash')),
    ('dot', _('Dots')),
    ('longdash', _('Long dashes')),
    ('longdashdot', _('Extra long dash-dot')),
    ('longdashdotdot', _('Long dash-dot-dot')),
    ('shortdash', _('Short dashes')),
    ('shortdashdot', _('Dash-dot')),
    ('shortdashdotdot', _('Dash-dot-dot')),
    ('shortdot', _('Dots with double spacing')),
)

CLUSTER_BALLOON_CONTENT_LAYOUT_CHOICES = (
    ('cluster#balloonTwoColumns', _('Two Columns')),
    ('cluster#balloonCarousel', _('Carousel'))
)

THEME_TYPE_CHOICES = (
    ('light', _('Light')),
    ('dark', _('Dark'))
)

LOAD_INDICATOR_SIZE_CHOICES = (
    (64, "64"),
    (96, "96"),
    (128, "128")
)

FEATURE_POINT = {
    "type": "Feature",
    "id": 0,
    "geometry": {
        "type": "Point",
        "coordinates": []
    },
    "properties": {
        "id": 0,
        "categoryID": 0,
        "subCategoryIDs": [],
        "iconSlug": ""
    },
    "options": {
        "iconLayout": "default#image",
        "iconImageHref": "",
        "iconImageSize": [],
        "iconImageOffset": []
    }
}

FEATURE_LINE = {
    "type": "Feature",
    "id": 0,
    "geometry": {
        "type": "LineString",
        "coordinates": []
    },
    "properties": {
        "id": 0,
        "categoryID": 0,
        "subCategoryIDs": []
    },
    "options": {
        "strokeWidth": 5,
        "strokeColor": "#00c853",
        "strokeStyle": "solid",
        "strokeOpacity": 0.9
    }
}

FEATURE_POLYGON = {
    "type": "Feature",
    "id": 0,
    "geometry": {
        "type": "Polygon",
        "coordinates": []
    },
    "properties": {
        "id": 0,
        "categoryID": 0,
        "subCategoryIDs": []
    },
    "options": {
        "strokeWidth": 2,
        "strokeColor": "#00c853",
        "strokeStyle": "solid",
        "strokeOpacity": 0.9,
        "fillColor": "#00E676",
        "fillOpacity": 0.9
    }
}

FEATURE_HEAT_POINT = {
    "type": "Feature",
    "id": 0,
    "geometry": {
        "type": "Point",
        "coordinates": []
    },
    "properties": {
        "weight": 0
    }
}
