# -*- coding: utf-8 -*-
import random

from django.core.management import BaseCommand, CommandError
from django.utils.lorem_ipsum import paragraphs

from djeym.models import (CategoryPlacemark, CustomMarkerIcon, Map, Placemark,
                          SubCategoryPlacemark)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100)

    def handle(self, *args, **options):
        count = options['count']

        if count == 0:
            msg = 'Error - The number of markers can not be zero. Parameter: --count'
            raise CommandError(msg)
        elif count < 0:
            msg = 'Error - The number of markers cannot be a negative number. Parameter: --count'
            raise CommandError(msg)

        slug = 'test'
        ymap = Map.objects.filter(slug=slug).first()

        if ymap is None:
            msg = 'Create a map with the name - Test'
            raise CommandError(msg)

        categories = CategoryPlacemark.objects.all()
        count_categories = categories.count()
        subcategories = SubCategoryPlacemark.objects.all()
        count_subcategories = subcategories.count()
        next_number_marker = Placemark.objects.count() + 1
        text = paragraphs(30, common=False)[0]
        icon_name_list = [icon.slug for icon in CustomMarkerIcon.objects.filter(icon_collection=ymap.icon_collection)]
        images = [
            '<p><img alt="" src="/media/uploads/2019/02/13/e51b6d5e-18df-4bb0-988a-b10b7a3bebb5.jpg" style="height:214px; width:322px" /></p>',
            '<p><img alt="" src="/media/uploads/2019/02/13/80c1d6e5-0a8e-48e5-9fda-980666ba2525.jpg" style="height:214px; width:322px" /></p>',
            '<p><img alt="" src="/media/uploads/2019/02/13/f05915cb-5683-4507-a186-c7f6466408ac.jpg" style="height:214px; width:322px" /></p>',
            '<p><img alt="" src="/media/uploads/2019/02/13/6be19160-164d-456d-aa3e-d407d40edae5.jpg" style="height:214px; width:322px" /></p>',
            '<p><img alt="" src="/media/uploads/2019/02/13/e988f41a-92cd-4f6c-b8db-8655188c1f2a.jpg" style="height:214px; width:322px" /></p>',
            '<p><img alt="" src="/media/uploads/2019/02/13/556e0572-e8f6-4b23-96ae-b53f73587ac9.jpg" style="height:214px; width:322px" /></p>',
            '<p><img alt="" src="/media/uploads/2019/02/13/da2fb316-9fd9-4d96-b4dd-7e44c0610eb2.jpg" style="height:181px; width:322px" /></p>',
            '<p><img alt="" src="/media/uploads/2019/02/13/36fa0a2f-6784-4314-a40b-903a1a734a35.png" style="height:120px; width:120px" /></p>'
        ]
        count_images = len(images)

        if count_categories == 0:
            msg = 'Create a category for markers!'
            raise CommandError(msg)

        for num in range(count):
            placemark = Placemark.objects.create(
                ymap=ymap,
                category=categories[random.randrange(count_categories)],
                header='<p>Marker heading - {}</p>'.format(next_number_marker),
                body='{0}<p>{1}</p>'.format(images[random.randrange(count_images)], text[:1000]),
                footer='<p>Footer text information - {}</p>'.format(next_number_marker),
                icon_name=random.choice(icon_name_list),
                coordinates='[{0},{1}]'.format(
                    random.randrange(-84, 76), random.randrange(-170, 170))
            )
            if count_subcategories > 0:
                placemark.subcategories.add(*[subcategories[idx] for idx in random.sample(
                    range(count_subcategories), random.randrange(count_subcategories) + 1)])
            next_number_marker += 1
