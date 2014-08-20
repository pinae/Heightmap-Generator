#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase
from Watermap import get_dir, get_min_flow_point


class WaterMapUtilityTest(TestCase):
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

    def test_get_near_sink(self):
        pass
