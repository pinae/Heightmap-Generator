#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys
import numpy as np
from random import randint

from Config import mapdimensions, slope, slopediag, directions


def update_min_max_map(height_map, water_map, pix, height):
    print("Doing: "+str(pix))
    jobs = []
    direction = water_map[pix[0], pix[1], 0]
    for i in directions.keys():
        v = directions[i]
        if 0 <= pix[0] + v[0] < mapdimensions[0] and 0 <= pix[1] + v[1] < mapdimensions[1]:
            if i == direction:
                max_height = height
                min_height = height
            else:
                if v[2]:
                    max_height = height + slope
                    min_height = height - slope
                else:
                    max_height = height + slopediag
                    min_height = height - slopediag
            if height_map[pix[0] + v[0], pix[1] + v[1], 1] > max_height:
                height_map[pix[0] + v[0], pix[1] + v[1], 1] = max_height
                jobs.append((height_map, water_map, (pix[0]+v[0],pix[1]+v[1]), max_height))
            if height_map[pix[0] + v[0], pix[1] + v[1], 0] < min_height:
                height_map[pix[0] + v[0], pix[1] + v[1], 0] = min_height
                jobs.append((height_map, water_map, (pix[0]+v[0],pix[1]+v[1]), min_height))
    for height_map, water_map, pix, height in jobs:
        update_min_max_map(height_map, water_map, pix, height)


def create_height_map(water_map, screen):
    height_map = np.zeros(mapdimensions+(3,),dtype=np.uint8)
    for x in height_map:
        for y in x:
            y[1] = 255
    for x in water_map:
        for y in x:
            y[0] /= 30
    fails = 0
    update = 0
    start_phase = 400
    while fails < 10:
        pix = (randint(0, mapdimensions[0] - 1), randint(0, mapdimensions[1] - 1))
        if height_map[pix[0], pix[1], 0] == height_map[pix[0], pix[1], 1]:
            fails += 1
            #print("Fails erhöht auf "+str(fails))
        else:
            fails = 0
            #print("Fails auf 0 gesetzt")
            height = randint(height_map[pix[0], pix[1], 0], height_map[pix[0], pix[1], 1])
            height_map[pix[0], pix[1], 2] = height
            #min- und maxmap updaten
            height_map[pix[0], pix[1], 0] = height
            height_map[pix[0], pix[1], 1] = height
            update_min_max_map(height_map, water_map, pix, height)
            #Anzeige
            if update == 0:
                if start_phase > 0:
                    update = 1
                else:
                    update = 75 + 10 * (fails + 1) * (fails + 1)
                pygame.surfarray.blit_array(screen, height_map)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()
            update -= 1
            start_phase -= 1
    print("Zufälliges setzen der Pixel beendet. Jetzt systematisch.")
    for x in range(len(height_map)):
        for y in range(len(height_map[x])):
            height = randint(height_map[x, y, 0], height_map[x, y, 1])
            height_map[x, y, 2] = height
            #min- und maxmap updaten
            height_map[x, y, 0] = height
            height_map[x, y, 1] = height
            update_min_max_map(height_map, water_map, (x, y), height)
        pygame.surfarray.blit_array(screen, height_map)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    return height_map