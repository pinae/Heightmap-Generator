#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys

from Config import mapdimensions
from Watermap import create_water_map, calculate_water_amounts, direct_flow_pass, initialize_amount_map, clear_amounts
from Heightmap import create_height_map


def main():
    # initialize PyGame environment
    pygame.init()
    # create a window
    screen = pygame.display.set_mode(mapdimensions)
    pygame.display.set_caption("Height Map Generator")
    # create the water_map and display it
    flow_points = [((0, 50), 0)]
    water_map = create_water_map(screen, flow_points)
    amount_map = initialize_amount_map()
    calculate_water_amounts(water_map, amount_map)
    pygame.surfarray.blit_array(screen, water_map)
    pygame.display.flip()
    direct_flow_pass(water_map, amount_map)
    clear_amounts(water_map, amount_map)
    calculate_water_amounts(water_map, amount_map)
    pygame.surfarray.blit_array(screen, water_map)
    pygame.display.flip()
    direct_flow_pass(water_map, amount_map)
    clear_amounts(water_map, amount_map)
    calculate_water_amounts(water_map, amount_map)
    pygame.surfarray.blit_array(screen, water_map)
    pygame.display.flip()
    print("water map created.")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # create the height_map and display it
    height_map = create_height_map(water_map, screen)
    pygame.surfarray.blit_array(screen, height_map)
    pygame.display.flip()
    # shutdown if requested
    print("Finished.")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == "__main__":
    main()