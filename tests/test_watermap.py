#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase
from Watermap import get_dir

class WatermapUtilityTest(TestCase):
    def test_get_dir(self):
        self.assertEqual(get_dir((2,2),(1,2)),0)
        self.assertEqual(get_dir((2,2),(1,1)),1)
        self.assertEqual(get_dir((2,2),(2,1)),2)
        self.assertEqual(get_dir((2,2),(3,1)),3)
        self.assertEqual(get_dir((2,2),(3,2)),4)
        self.assertEqual(get_dir((2,2),(3,3)),5)
        self.assertEqual(get_dir((2,2),(2,3)),6)
        self.assertEqual(get_dir((2,2),(1,3)),7)
