#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys
import numpy as np
from random import randint, shuffle, random
from math import exp
from Config import mapdimensions, slope, slopediag, directions


def get_min_height(job):
    return job[3]


def update_min_map(height_map, water_map, pix, min_height):
    jobs = [(height_map, water_map, (pix[0], pix[1]), min_height)]
    while len(jobs) > 0:
        height_map, water_map, pix, job_min_height = jobs.pop(0)
        a = directions.keys()
        for i in a:
            v = directions[i]
            min_height = job_min_height
            if 0 <= pix[0] + v[0] < mapdimensions[0] and 0 <= pix[1] + v[1] < mapdimensions[1]:
                v_source = directions[water_map[pix[0]+v[0], pix[1]+v[1], 0]]
                if 0 != v[0]+v_source[0] or 0 != v[1]+v_source[1]:
                    if v[2]:
                        min_height -= slope
                    else:
                        min_height -= slopediag
                if height_map[pix[0] + v[0], pix[1] + v[1], 0] < min_height:
                    height_map[pix[0] + v[0], pix[1] + v[1], 0] = max(
                        min_height,
                        height_map[pix[0] + v[0], pix[1] + v[1], 0]
                    )
                    jobs.append((height_map, water_map, (pix[0] + v[0], pix[1] + v[1]), min_height))
        jobs.sort(key=get_min_height)


def update_max_map(height_map, water_map, pix, max_height):
    jobs = [(height_map, water_map, (pix[0], pix[1]), max_height)]
    while len(jobs) > 0:
        height_map, water_map, pix, job_max_height = jobs.pop(0)
        a = directions.keys()
        for i in a:
            v = directions[i]
            max_height = job_max_height
            if 0 <= pix[0] + v[0] < mapdimensions[0] and 0 <= pix[1] + v[1] < mapdimensions[1]:
                if i != water_map[pix[0], pix[1], 0]:
                    if v[2]:
                        max_height += slope
                    else:
                        max_height += slopediag
                if height_map[pix[0] + v[0], pix[1] + v[1], 1] > max_height:
                    height_map[pix[0] + v[0], pix[1] + v[1], 1] = min(
                        max_height,
                        height_map[pix[0] + v[0], pix[1] + v[1], 1])
                    jobs.append((height_map, water_map, (pix[0] + v[0], pix[1] + v[1]), max_height))
        jobs.sort(key=get_min_height, reverse=True)


def create_height_map(water_map, screen):
    height_map = np.zeros(mapdimensions+(3,), dtype=np.uint8)
    for x in height_map:
        for y in x:
            y[1] = 255
    for x in water_map:
        for y in x:
            y[0] /= 30
    all_points = []
    for x in range(mapdimensions[0]):
        for y in range(mapdimensions[1]):
            all_points.append((x, y))
    shuffle(all_points)
    for pix_no, pix in enumerate(all_points):
        min_value = height_map[pix[0], pix[1], 0]
        max_value = height_map[pix[0], pix[1], 1]
        #height = randint(min_value, max_value)
        #height = min_value + int(round((max_value-min_value)/2.0))
        height = min_value + int(round((max_value-min_value)/2.0+(max_value-min_value)*0.2*(random()-0.5)))
        #x = water_map[pix[0], pix[1], 2] * 3000.0 / slope / (mapdimensions[0] + mapdimensions[1])
        #height = min_value + int(round(exp(-0.5 * x * x) * (max_value - min_value) * 0.99 + 0.01 * random()))
        height_map[pix[0], pix[1], 2] = height
        # update min- and maxmap
        height_map[pix[0], pix[1], 0] = height
        height_map[pix[0], pix[1], 1] = height
        update_min_map(height_map, water_map, pix, height)
        update_max_map(height_map, water_map, pix, height)
        # view update
        if pix_no < mapdimensions[0] + mapdimensions[1] or pix[0] == 0:
            pygame.surfarray.blit_array(screen, height_map)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
    return height_map