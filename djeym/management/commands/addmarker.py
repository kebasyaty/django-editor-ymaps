# -*- coding: utf-8 -*-
import random

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.utils.lorem_ipsum import paragraphs

from djeym.models import (CategoryPlacemark, Map, MarkerIcon, Placemark,
                          SubCategoryPlacemark)

# Map name: Test Map
# --count - default=100
# python manage.py addmarker
# python manage.py addmarker --count 1000


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

        slug = 'test-map'
        media_url = getattr(settings, 'MEDIA_URL', None)
        ymap = Map.objects.filter(slug=slug).first()

        if ymap is None:
            msg = 'Create a map with the name - Test Map'
            raise CommandError(msg)
        elif media_url is None:
            msg = 'Add MEDIA_URL in settings.py'
            raise CommandError(msg)

        categories = CategoryPlacemark.objects.all()
        count_categories = categories.count()
        subcategories = SubCategoryPlacemark.objects.all()
        count_subcategories = subcategories.count()
        next_number_marker = Placemark.objects.count() + 1
        text = paragraphs(30, common=False)[0]
        icon_name_list = [icon.slug for icon in MarkerIcon.objects.filter(
            icon_collection=ymap.icon_collection)]
        images = [
            '<p><img alt="" src="{}uploads/2019/12/29/1.jpg" style="width:322px;" /></p>'.format(
                media_url),
            '<p><img alt="" src="{}uploads/2019/12/29/2.jpg" style="width:322px;" /></p>'.format(
                media_url),
            '<p><img alt="" src="{}uploads/2019/12/29/3.jpg" style="width:322px;" /></p>'.format(
                media_url),
            '<p><img alt="" src="{}uploads/2019/12/29/4.jpg" style="width:322px;" /></p>'.format(
                media_url),
            '<p><img alt="" src="{}uploads/2019/12/29/5.jpg" style="width:322px;" /></p>'.format(
                media_url),
            '<p><img alt="" src="{}uploads/2019/12/29/6.jpg" style="width:322px;" /></p>'.format(
                media_url),
            '<p><img alt="" src="{}uploads/2019/12/29/7.jpg" style="width:322px;" /></p>'.format(
                media_url),
            '<p><img alt="" src="{}uploads/2019/12/29/8.jpg" style="width:322px;" /></p>'.format(
                media_url),
            '<p><img alt="" src="{}uploads/2019/12/29/9.jpg" style="width:322px;" /></p>'.format(
                media_url),
            '<p><img alt="" src="{}uploads/2019/12/29/10.jpg" style="width:322px;" /></p>'.format(
                media_url),
        ]
        count_images = len(images)

        if count_categories == 0:
            msg = 'Create a category for markers!'
            raise CommandError(msg)

        for num in range(count):
            placemark = Placemark.objects.create(
                ymap=ymap,
                category=categories[random.randrange(count_categories)],
                header='<p>Marker Header - {}</p>'.format(next_number_marker),
                body='{0}<p>{1}</p>'.format(
                    images[random.randrange(count_images)], text[:1000]),
                footer='<p>Footer of Marker - {}</p>'.format(
                    next_number_marker),
                icon_slug=random.choice(icon_name_list),
                coordinates='[{0},{1}]'.format(
                    random.randrange(-84, 76), random.randrange(-170, 170))
            )
            if count_subcategories > 0:
                placemark.subcategories.add(*[subcategories[idx] for idx in random.sample(
                    range(count_subcategories), random.randrange(count_subcategories) + 1)])
            next_number_marker += 1
