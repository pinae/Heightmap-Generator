#!/usr/bin/python
# -*- coding: utf-8 -*-

mapdimensions = (128,128)

slope = 20
slopediag = 35

directions = {0: (-1, 0, True),
              1: (-1, -1, False),
              2: (0, -1, True),
              3: (+1, -1, False),
              4: (+1, 0, True),
              5: (+1, +1, False),
              6: (0, +1, True),
              7: (-1, +1, False)}