# -*- coding: utf-8 -*-
from datetime import datetime

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# Example: {{ '2014'|year_copyright }}
@register.filter
def year_copyright(start_year):
    start_year = int(start_year)
    curr_year = int(datetime.today().year)
    if start_year < curr_year:
        return '{0}-{1}'.format(start_year, curr_year)
    return start_year


@register.filter
def escape_double_brackets(value):
    return mark_safe(value.replace('"', '\\"'))
