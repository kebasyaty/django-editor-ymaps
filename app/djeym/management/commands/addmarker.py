"""Add Marker.

Hint:
- Map name: Test Map
- --count - default=100
- python manage.py addmarker
- python manage.py addmarker --count 1000
"""

from __future__ import annotations

import random

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.utils.lorem_ipsum import paragraphs

from djeym.models import CategoryPlacemark, Map, MarkerIcon, Placemark, SubCategoryPlacemark


class Command(BaseCommand):  # noqa: D101
    def add_arguments(self, parser):  # noqa: D102
        parser.add_argument("--count", type=int, default=100)

    def handle(self, *args, **options):  # noqa: D102
        count = options["count"]

        if count == 0:
            msg = "Error - The number of markers can not be zero. Parameter: --count"
            raise CommandError(msg)
        elif count < 0:  # noqa: RET506
            msg = "Error - The number of markers cannot be a negative number. Parameter: --count"
            raise CommandError(msg)

        slug = "test-map"
        media_url = getattr(settings, "MEDIA_URL", None)
        ymap = Map.objects.filter(slug=slug).first()

        if ymap is None:
            msg = "Create a map with the name - Test Map"
            raise CommandError(msg)
        elif media_url is None:  # noqa: RET506
            msg = "Add MEDIA_URL in settings.py"
            raise CommandError(msg)

        categories = CategoryPlacemark.objects.all()
        count_categories = categories.count()
        subcategories = SubCategoryPlacemark.objects.all()
        count_subcategories = subcategories.count()
        next_number_marker = Placemark.objects.count() + 1
        text = paragraphs(30, common=False)[0]
        icon_name_list = [icon.slug for icon in MarkerIcon.objects.filter(icon_collection=ymap.icon_collection)]
        images = [
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/1.jpg" style="width:322px;" /></p>',
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/2.jpg" style="width:322px;" /></p>',
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/3.jpg" style="width:322px;" /></p>',
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/4.jpg" style="width:322px;" /></p>',
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/5.jpg" style="width:322px;" /></p>',
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/6.jpg" style="width:322px;" /></p>',
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/7.jpg" style="width:322px;" /></p>',
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/8.jpg" style="width:322px;" /></p>',
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/9.jpg" style="width:322px;" /></p>',
            f'<p><img alt="" src="{media_url}uploads/2019/12/29/10.jpg" style="width:322px;" /></p>',
        ]
        count_images = len(images)

        if count_categories == 0:
            msg = "Create a category for markers!"
            raise CommandError(msg)

        for _ in range(count):
            placemark = Placemark.objects.create(
                ymap=ymap,
                category=categories[random.randrange(count_categories)],  # noqa: S311
                header=f"<p>Marker Header - {next_number_marker}</p>",
                body=f"{images[random.randrange(count_images)]}<p>{text[:1000]}</p>",  # noqa: S311
                footer=f"<p>Footer of Marker - {next_number_marker}</p>",
                icon_slug=random.choice(icon_name_list),  # noqa: S311
                coordinates="[{random.randrange(-84, 76)},{random.randrange(-170, 170)}]",
            )
            if count_subcategories > 0:
                placemark.subcategories.add(
                    *[
                        subcategories[idx]
                        for idx in random.sample(range(count_subcategories), random.randrange(count_subcategories) + 1)  # noqa: S311
                    ],
                )
            next_number_marker += 1
