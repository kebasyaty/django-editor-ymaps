from django.test import TestCase
from djeym.utils import get_distance_from_coords
from django.template import Context, Template
from django.contrib.auth import get_user_model


class UtilsTest(TestCase):
    def setUp(self):
        pass

    def test_get_distance_from_coords(self):
        """
            Тестируем функцию рассчёта расстояния по координатам для больших, маленьких и средних расстояний.
        """
        # arrange
        moscow_center = [55.753215, 37.622504]
        newyork = [40.853544, -73.099544]
        voronezh = [51.660781, 39.200269]
        moscow_kurskiy = [55.756989, 37.661230]
        # act
        long = get_distance_from_coords(moscow_center[0], moscow_center[1], newyork[0], newyork[1])
        middle = get_distance_from_coords(moscow_center[0], moscow_center[1], voronezh[0], voronezh[1])
        short = get_distance_from_coords(moscow_center[0], moscow_center[1], moscow_kurskiy[0], moscow_kurskiy[1])
        # assert
        self.assertEqual(int(long), 7454423)
        self.assertEqual(int(middle), 466724)
        self.assertEqual(int(short), 2459)


class TagsTest(TestCase):
    pass
