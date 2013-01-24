#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys
import numpy as np

from Config import mapdimensions
from Watermap import create_water_map
from Heightmap import create_height_map

def main():
    # initialize PyGame environment
    pygame.init()
    # create a window
    screen = pygame.display.set_mode(mapdimensions)
    pygame.display.set_caption("Height Map Generator")
    # create the water_map and display it
    #water_map = create_water_map(screen)
    water_map = np.array([np.array([np.array([255,0,0]) for y in range(mapdimensions[1])]) for x in range(mapdimensions[0])])
    pygame.surfarray.blit_array(screen, water_map)
    pygame.display.flip()
    print("water map created.")
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    # create the height_map and display it
    height_map = create_height_map(water_map, screen)
    pygame.surfarray.blit_array(screen, height_map)
    pygame.display.flip()
    # shutdown if requested
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

if __name__ == "__main__":
    main()