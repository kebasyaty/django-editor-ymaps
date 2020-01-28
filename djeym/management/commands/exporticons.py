# -*- coding: utf-8 -*-
import os

from django.core.files import File
from django.core.management import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.utils.translation import ugettext as _
from slugify import slugify

from djeym.models import IconCollection, MarkerIcon

# --name - 'Icon Collection Name
# --path - '/home/user_name/The path to the directory with icons'
# python manage.py exporticons --name '' --path ''


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, default="")
        parser.add_argument('--path', type=str, default="")

    def handle(self, *args, **options):
        collection_name = options['name']
        dir_path = options['path']

        if len(collection_name) == 0:
            msg = _('Error - Collection name not specified. Parameter: --name')
            raise CommandError(msg)

        if not os.path.isdir(dir_path):
            msg = _('Error - Specify a directory with icons. Parameter: --path')
            raise CommandError(msg)

        if IconCollection.objects.filter(slug=slugify(collection_name)).count() != 0:
            msg = _('The {} collection already exists.')
            raise CommandError(msg.format(collection_name))

        collection = IconCollection.objects.create(title=collection_name)
        icon_list = os.listdir(path=dir_path)

        try:
            with transaction.atomic():
                for icon in icon_list:
                    icon_path = "{0}/{1}".format(dir_path, icon)
                    with open(icon_path, mode='rb') as svg_file:
                        MarkerIcon.objects.create(
                            icon_collection=collection,
                            title=os.path.splitext(icon)[0],
                            svg=File(svg_file))
        except IntegrityError as err:
            raise CommandError(err)
