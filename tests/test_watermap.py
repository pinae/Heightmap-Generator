#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from Watermap import initialize_water_map, get_dir, get_min_flow_point, get_near_sink, create_river, create_water_map
from Watermap import calculate_amount_for_pix, calculate_water_amounts


def return1():
    return 1.0


def return0():
    return 0.0


def return_half():
    return 0.5


def return_the_same(x):
    return x


class WaterMapUtilityTest(TestCase):
    @patch('Watermap.mapdimensions', (2, 2))
    def test_initialize_water_map(self):
        water_map = initialize_water_map()
        self.assertEqual(len(water_map), 2)
        self.assertEqual(len(water_map[0]), 2)
        for line in water_map:
            for cell in line:
                self.assertEqual(cell[0], 255)
                self.assertEqual(cell[2], 0)

    def test_get_dir(self):
        self.assertEqual(get_dir((2, 2), (1, 2)), 0)
        self.assertEqual(get_dir((2, 2), (1, 1)), 1)
        self.assertEqual(get_dir((2, 2), (2, 1)), 2)
        self.assertEqual(get_dir((2, 2), (3, 1)), 3)
        self.assertEqual(get_dir((2, 2), (3, 2)), 4)
        self.assertEqual(get_dir((2, 2), (3, 3)), 5)
        self.assertEqual(get_dir((2, 2), (2, 3)), 6)
        self.assertEqual(get_dir((2, 2), (1, 3)), 7)

    def test_get_min_flow_point(self):
        flow_points = [(0, 0), (2, 0), (3, 5)]
        self.assertEqual(get_min_flow_point((2, 2), flow_points), ((2, 0), 2))
        self.assertEqual(get_min_flow_point((3, 3), flow_points), ((3, 5), 2))
        self.assertEqual(get_min_flow_point((0, 1), flow_points), ((0, 0), 1))
        self.assertEqual(get_min_flow_point((2, 0), flow_points), ((2, 0), 0))

    @patch('Watermap.mapdimensions', (6, 6))
    def test_get_near_sink(self):
        water_map = initialize_water_map()
        for cell in water_map[0]:
            cell[0] = 0
        for cell in water_map[5]:
            cell[0] = 0
        self.assertEqual(get_near_sink((3, 2), [(0, 0), (6, 0)], water_map), (5, 2))

    @patch('Watermap.mapdimensions', (2, 2))
    def test_create_river_neighbouring_points(self):
        water_map = initialize_water_map()
        self.assertTrue(create_river(water_map, (0, 0), (1, 1)))
        self.assertEqual(water_map[0, 0, 0], 5 * 30)
        self.assertEqual(water_map[0, 1, 0], 255)
        self.assertEqual(water_map[1, 0, 0], 255)
        self.assertEqual(water_map[1, 1, 0], 255)
        self.assertFalse(create_river(water_map, (0, 0), (1, 1)))

    @patch('Watermap.mapdimensions', (3, 3))
    @patch('Watermap.random', return1)
    def test_create_river(self):
        water_map = initialize_water_map()
        self.assertTrue(create_river(water_map, (0, 0), (2, 2)))
        self.assertEqual(water_map[0, 0, 0], 4 * 30)
        self.assertEqual(water_map[1, 0, 0], 5 * 30)
        self.assertEqual(water_map[2, 1, 0], 6 * 30)
        self.assertEqual(water_map[2, 0, 0], 255)
        self.assertEqual(water_map[2, 2, 0], 255)
        self.assertEqual(water_map[1, 1, 0], 255)
        self.assertEqual(water_map[1, 2, 0], 255)
        self.assertEqual(water_map[0, 1, 0], 255)
        self.assertEqual(water_map[0, 2, 0], 255)

    @patch('Watermap.mapdimensions', (3, 3))
    @patch('Watermap.random', return0)
    def test_create_river(self):
        water_map = initialize_water_map()
        self.assertTrue(create_river(water_map, (0, 0), (2, 2)))
        self.assertEqual(water_map[0, 0, 0], 6 * 30)
        self.assertEqual(water_map[0, 1, 0], 5 * 30)
        self.assertEqual(water_map[1, 2, 0], 4 * 30)
        self.assertEqual(water_map[2, 0, 0], 255)
        self.assertEqual(water_map[2, 2, 0], 255)
        self.assertEqual(water_map[1, 1, 0], 255)
        self.assertEqual(water_map[2, 1, 0], 255)
        self.assertEqual(water_map[1, 0, 0], 255)
        self.assertEqual(water_map[0, 2, 0], 255)

    @patch('Watermap.mapdimensions', (3, 3))
    @patch('Watermap.random', return_half)
    def test_create_river(self):
        water_map = initialize_water_map()
        self.assertTrue(create_river(water_map, (0, 0), (2, 2)))
        self.assertEqual(water_map[0, 0, 0], 5 * 30)
        self.assertEqual(water_map[1, 1, 0], 5 * 30)
        self.assertEqual(water_map[2, 1, 0], 255)
        self.assertEqual(water_map[2, 0, 0], 255)
        self.assertEqual(water_map[2, 2, 0], 255)
        self.assertEqual(water_map[1, 0, 0], 255)
        self.assertEqual(water_map[1, 2, 0], 255)
        self.assertEqual(water_map[0, 1, 0], 255)
        self.assertEqual(water_map[0, 2, 0], 255)

    @patch('Watermap.mapdimensions', (3, 3))
    @patch('Watermap.random', return_half)
    @patch('Watermap.shuffle', return_the_same)
    def test_create_water_map(self):
        water_map = create_water_map(None, [((0, 1), 0)])
        expected = [[[180, 0, 0],
                     [0, 0, 0],
                     [60, 0, 0]],
                    [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]],
                    [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]]
        for x in range(len(water_map)):
            for y in range(len(water_map[0])):
                for v in range(len(water_map[0][0])):
                    self.assertEqual(water_map[x][y][v], expected[x][y][v])

    @patch('Watermap.mapdimensions', (3, 3))
    def test_calculate_amount_for_pix(self):
        water_map = initialize_water_map()
        water_map[0, 0, 0] = 5 * 30
        water_map[1, 0, 0] = 6 * 30
        water_map[2, 0, 0] = 7 * 30
        water_map[0, 1, 0] = 6 * 30
        water_map[1, 1, 0] = 0 * 30
        water_map[2, 1, 0] = 6 * 30
        water_map[0, 2, 0] = 0 * 30
        water_map[1, 2, 0] = 6 * 30
        water_map[2, 2, 0] = 5 * 30
        calculate_amount_for_pix(water_map, (1, 1))
        self.assertEqual(water_map[0, 0, 2], 1)
        self.assertEqual(water_map[1, 0, 2], 1)
        self.assertEqual(water_map[2, 0, 2], 1)
        self.assertEqual(water_map[1, 1, 2], 4)
        self.assertEqual(water_map[2, 2, 2], 0)

    @patch('Watermap.mapdimensions', (3, 3))
    def test_calculate_water_amounts(self):
        water_map = initialize_water_map()
        water_map[0, 0, 0] = 5 * 30
        water_map[1, 0, 0] = 6 * 30
        water_map[2, 0, 0] = 7 * 30
        water_map[0, 1, 0] = 6 * 30
        water_map[1, 1, 0] = 0 * 30
        water_map[2, 1, 0] = 6 * 30
        water_map[0, 2, 0] = 0 * 30
        water_map[1, 2, 0] = 6 * 30
        water_map[2, 2, 0] = 5 * 30
        calculate_water_amounts(water_map)
        self.assertEqual(water_map[0, 0, 2], 1)
        self.assertEqual(water_map[1, 0, 2], 1)
        self.assertEqual(water_map[2, 0, 2], 1)
        self.assertEqual(water_map[0, 1, 2], 5)
        self.assertEqual(water_map[1, 1, 2], 4)
        self.assertEqual(water_map[2, 1, 2], 1)
        self.assertEqual(water_map[0, 2, 2], 6)
        self.assertEqual(water_map[1, 2, 2], 1)
        self.assertEqual(water_map[2, 2, 2], 2)