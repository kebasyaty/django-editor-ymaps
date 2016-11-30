# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ValidationError
import os
import uuid


def get_errors_form(*args):
    err_dict = {}
    err_txt = ''

    for form in args:
        for item in list(form):
            if item.errors:
                err_dict[item.name] = True
                err_txt += u'{0}: {1}<br>'.format(item.label, item.errors)
            else:
                err_dict[item.name] = False

    return {'err_dict': err_dict, 'err_txt': err_txt}


def validate_image(image):
    extension_list = ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']
    size = int(image.size)
    extension = image.name.split('.')[-1]

    if not [ext for ext in extension_list if extension == ext]:
        raise ValidationError(_('Only JPG, PNG or GIF format files.'))
    elif not size:
        raise ValidationError(_('image cannot be 0.0 mb'))
    elif not size or size > 1024000:
        raise ValidationError(_('Image size exceeds the limit 1.0 mb.'))


def make_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    return os.path.join(instance.upload_dir, u'{0}.{1}'.format(uuid.uuid4(), extension))
