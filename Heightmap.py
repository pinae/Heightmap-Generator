#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys
import numpy as np
from random import randint, shuffle

from Config import mapdimensions, slope, slopediag, directions


def update_min_max_map(height_map, water_map, pix, min_height, max_height):
    print("Doing: "+str(pix))
    jobs = [(height_map, water_map, (pix[0],pix[1]), min_height, max_height)]
    while len(jobs) > 0:
        height_map, water_map, pix, job_min_height, job_max_height = jobs.pop(0)
        a = directions.keys()
        shuffle(a)
        for i in a:
            v = directions[i]
            min_height = job_min_height
            max_height = job_max_height
            if 0 <= pix[0] + v[0] < mapdimensions[0] and 0 <= pix[1] + v[1] < mapdimensions[1]:
                #print(str((pix[0] + v[0],pix[1] + v[1]))+"   "+str(i))
                if i != randint(0,7):#water_map[pix[0], pix[1], 0]:
                    if v[2]:
                        max_height += slope
                        min_height -= slope
                    else:
                        max_height += slopediag
                        min_height -= slopediag
                if height_map[pix[0] + v[0], pix[1] + v[1], 1] > max_height or\
                   height_map[pix[0] + v[0], pix[1] + v[1], 0] < min_height:
                    height_map[pix[0] + v[0], pix[1] + v[1], 1] = min(max_height,
                        height_map[pix[0] + v[0], pix[1] + v[1], 1])
                    height_map[pix[0] + v[0], pix[1] + v[1], 0] = max(min_height,
                        height_map[pix[0] + v[0], pix[1] + v[1], 0])
                    jobs.append((height_map, water_map, (pix[0] + v[0], pix[1] + v[1]), min_height, max_height))
        #print(str(len(jobs))+" Calls to be calculated")


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
            #print("New Pixel ____________________________________________")
            #raw_input("Press Enter to continue...")
            #print("Fails auf 0 gesetzt")
            height = randint(height_map[pix[0], pix[1], 0], height_map[pix[0], pix[1], 1])
            height_map[pix[0], pix[1], 2] = height
            #min- und maxmap updaten
            height_map[pix[0], pix[1], 0] = height
            height_map[pix[0], pix[1], 1] = height
            update_min_max_map(height_map, water_map, pix, height, height)
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
            update_min_max_map(height_map, water_map, (x, y), height, height)
        pygame.surfarray.blit_array(screen, height_map)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    return height_map