"""Export Icons.

Hint:
- --name - 'Icon Collection Name
- --path - '/home/user_name/The path to the directory with icons'
- python manage.py exporticons --name '' --path ''
"""

from __future__ import annotations

from pathlib import Path

from django.core.files import File
from django.core.management import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.utils.translation import ugettext as _  # pyrefly: ignore[missing-module-attribute]
from slugify import slugify

from djeym.models import IconCollection, MarkerIcon


class Command(BaseCommand):  # noqa: D101
    def add_arguments(self, parser):  # noqa: D102
        parser.add_argument("--name", type=str, default="")
        parser.add_argument("--path", type=str, default="")

    def handle(self, *args, **options):  # noqa: D102
        collection_name = options["name"]
        dir_path = options["path"]

        if len(collection_name) == 0:
            msg = _("Error - Collection name not specified. Parameter: --name")
            raise CommandError(msg)

        if not Path(dir_path).is_dir():
            msg = _("Error - Specify a directory with icons. Parameter: --path")
            raise CommandError(msg)

        if IconCollection.objects.filter(slug=slugify(collection_name)).count() != 0:
            msg = _("The {} collection already exists.")
            raise CommandError(msg.format(collection_name))

        collection = IconCollection.objects.create(title=collection_name)
        icon_list = Path(dir_path).iterdir()

        try:
            with transaction.atomic():
                for icon in icon_list:
                    icon_path = f"{dir_path}/{icon}"
                    with Path(icon_path).open(mode="rb") as svg_file:
                        MarkerIcon.objects.create(
                            icon_collection=collection,
                            title=icon.suffix()[0],  # pyrefly: ignore[not-callable]
                            svg=File(svg_file),
                        )
        except IntegrityError as err:
            raise CommandError from err
