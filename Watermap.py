#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame
import numpy as np
from random import randint, random, shuffle

from Config import mapdimensions


def get_dir(start, end):
    if start[0] < end[0]:
        if start[1] < end[1]:
            return 5
        else:
            if start[1] > end[1]:
                return 3
            else:
                return 4
    else:
        if start[0] > end[0]:
            if start[1] < end[1]:
                return 7
            else:
                if start[1] > end[1]:
                    return 1
                else:
                    return 0
        else:
            if start[1] < end[1]:
                return 6
            else:
                if start[1] > end[1]:
                    return 2
                else:
                    print("Keine Richtung definierbar! Start und End sind gleich!")
                    return 0


def create_river(water_map, start, end):
    if abs(start[0] - end[0]) > 1 or abs(start[1] - end[1]) > 1:
        dist = np.sqrt((start[0] - end[0]) * (start[0] - end[0]) + (start[1] - end[1]) * (start[1] - end[1]))
        #print("Dist ist " + str(dist))
        middle = (start[0] / 2.0 + end[0] / 2.0, start[1] / 2.0 + end[1] / 2.0)
        rand_num = (random() - 0.5) / 2
        middle = (max(0, min(mapdimensions[0]-1, int(round(middle[0] + (end[1] - start[1]) * rand_num)))),
                  max(0, min(mapdimensions[1]-1, int(round(middle[1] - (end[0] - start[0]) * rand_num)))))
        if create_river(water_map, start, middle):
            return create_river(water_map, middle, end)
        else:
            return False
    else:
        #print("Benachbart!")
        if water_map[start[0], start[1], 0] == 255:
            water_map[start[0], start[1], 0] = get_dir(start, end) * 30
            return True
        else:
            #print("Direction already decided!")
            return False


def get_min_flow_point(point, flow_points):
    min_dist = np.sqrt(
        (flow_points[0][0] - point[0]) * (flow_points[0][0] - point[0]) +
        (flow_points[0][1] - point[1]) * (flow_points[0][1] - point[1])
    )
    min_point = flow_points[0]
    for flow_point in flow_points[1:]:
        dist = np.sqrt(
            (flow_point[0] - point[0]) * (flow_point[0] - point[0]) +
            (flow_point[1] - point[1]) * (flow_point[1] - point[1])
        )
        if dist < min_dist:
            min_dist = dist
            min_point = flow_point
    return min_point, min_dist


def get_near_sink(point, flow_points, water_map):
    min_point, dist = get_min_flow_point(point, flow_points)
    # search for flowpoints in the middle of rivers which are nearer
    step = 1
    while step < min(dist, 50):
        possible_positions = [
            (point[0] + step, point[1]),
            (point[0], point[1] + step),
            (point[0] - step, point[1]),
            (point[0], point[1] - step),
            (point[0] + step * 180 / 255, point[1] + step * 180 / 255),
            (point[0] + step * 180 / 255, point[1] - step * 180 / 255),
            (point[0] - step * 180 / 255, point[1] + step * 180 / 255),
            (point[0] - step * 180 / 255, point[1] - step * 180 / 255)
        ]
        shuffle(possible_positions)
        for sink_candidate in possible_positions:
            if 0 <= sink_candidate[0] < mapdimensions[0] and 0 <= sink_candidate[1] < mapdimensions[1] and \
               water_map[sink_candidate[0], sink_candidate[1], 0] < 255:
                return sink_candidate
        step += 1
    return min_point


def initialize_water_map():
    water_map = np.zeros(mapdimensions+(3,), dtype=np.uint8)
    for x in water_map:
        for y in x:
            y[0] = 255
            y[2] = 0  # randint(0, 7) * 30
    return water_map


def create_water_map(screen):
    water_map = initialize_water_map()
    flow_points = [(0, 50)]
    fail_counter = 0
    show_counter = 1
    while fail_counter < 13:
        #select a random point
        point = (randint(0, mapdimensions[0] - 1), randint(0, mapdimensions[1] - 1))
        #test
        if water_map[point[0], point[1], 0] < 255:
            fail_counter += 1
        else:
            end_point = get_near_sink(point, flow_points, water_map)
            if len(flow_points) < 1000:
                flow_points.append(end_point)
            create_river(water_map, point, end_point)
            fail_counter = 0
        if fail_counter == show_counter:
            pygame.surfarray.blit_array(screen, water_map)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            show_counter += 1
    for x in water_map:
        for y in x:
            if y[0] == 255:
                y[0] = randint(0, 7)*30#180
    return water_map