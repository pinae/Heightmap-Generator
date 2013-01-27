#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame
import numpy as np
from random import randint, random

from Config import mapdimensions


def get_dir(start, end):
    if start[0] < end[0]:
        if start[1] < end[1]:
            return 5
        else:
            if start[1] > end[1]:
                return 7
            else:
                return 6
    else:
        if start[0] > end[0]:
            if start[1] < end[1]:
                return 3
            else:
                if start[1] > end[1]:
                    return 1
                else:
                    return 2
        else:
            if start[1] < end[1]:
                return 0
            else:
                if start[1] > end[1]:
                    return 4
                else:
                    print("Keine Richtung definierbar! Start und End sind gleich!")
                    return 0


def create_river(water_map, start, end):
    if abs(start[0] - end[0]) > 1 or abs(start[1] - end[1]) > 1:
        dist = np.sqrt((start[0] - end[0]) * (start[0] - end[0]) + (start[1] - end[1]) * (start[1] - end[1]))
        #print("Dist ist " + str(dist))
        middle = [start[0] / 2.0 + end[0] / 2.0, start[1] / 2.0 + end[1] / 2.0]
        rand_num = (random() - 0.5) / 2
        middle = (max(0,min(mapdimensions[0]-1,int(round(middle[0] + (end[1] - start[1]) * rand_num)))),
                  max(0,min(mapdimensions[1]-1,int(round(middle[1] - (end[0] - start[0]) * rand_num)))))
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
            return False


def get_min_flow_point(point, flow_points):
    min_dist = np.sqrt(
        (flow_points[0][0] - point[0]) * (flow_points[0][0] - point[0]) + (flow_points[0][1] - point[1]) * (
            flow_points[0][1] - point[1]))
    min_point = flow_points[0]
    for flow_point in flow_points:
        dist = np.sqrt((flow_point[0] - point[0]) * (flow_point[0] - point[0]) + (flow_point[1] - point[1]) * (
            flow_point[1] - point[1]))
        if dist < min_dist:
            min_dist = dist
            min_point = flow_point
    return min_point


def get_near_flow_point(point, flow_points, water_map):
    min_point = get_min_flow_point(point, flow_points)
    dist = np.sqrt(
        (min_point[0] - point[0]) * (min_point[0] - point[0]) + (min_point[1] - point[1]) * (min_point[1] - point[1]))
    # search for flowpoints in the middle of rivers which are nearer
    step = 1
    while step < min(dist,50):
        if randint(0,1):
            if randint(0,1):
                if randint(0,1):
                    if point[0] + step < mapdimensions[0] and water_map[point[0] + step, point[1], 0] < 255: return point[0] + step, point[1]
                    if point[1] + step < mapdimensions[1] and water_map[point[0], point[1] + step, 0] < 255: return point[0], point[1] + step
                else:
                    if point[1] + step < mapdimensions[1] and water_map[point[0], point[1] + step, 0] < 255: return point[0], point[1] + step
                    if point[0] + step < mapdimensions[0] and water_map[point[0] + step, point[1], 0] < 255: return point[0] + step, point[1]
                if randint(0,1):
                    if point[0] - step >= 0 and water_map[point[0] - step, point[1], 0] < 255: return point[0] - step, point[1]
                    if point[1] - step >= 0 and water_map[point[0], point[1] - step, 0] < 255: return point[0], point[1] - step
                else:
                    if point[1] - step >= 0 and water_map[point[0], point[1] - step, 0] < 255: return point[0], point[1] - step
                    if point[0] - step >= 0 and water_map[point[0] - step, point[1], 0] < 255: return point[0] - step, point[1]
            else:
                if randint(0,1):
                    if point[0] - step >= 0 and water_map[point[0] - step, point[1], 0] < 255: return point[0] - step, point[1]
                    if point[1] - step >= 0 and water_map[point[0], point[1] - step, 0] < 255: return point[0], point[1] - step
                else:
                    if point[1] - step >= 0 and water_map[point[0], point[1] - step, 0] < 255: return point[0], point[1] - step
                    if point[0] - step >= 0 and water_map[point[0] - step, point[1], 0] < 255: return point[0] - step, point[1]
                if randint(0,1):
                    if point[0] + step < mapdimensions[0] and water_map[point[0] + step, point[1], 0] < 255: return point[0] + step, point[1]
                    if point[1] + step < mapdimensions[1] and water_map[point[0], point[1] + step, 0] < 255: return point[0], point[1] + step
                else:
                    if point[1] + step < mapdimensions[1] and water_map[point[0], point[1] + step, 0] < 255: return point[0], point[1] + step
                    if point[0] + step < mapdimensions[0] and water_map[point[0] + step, point[1], 0] < 255: return point[0] + step, point[1]
            if randint(0,1):
                if randint(0,1):
                    if point[0] - step >= 0 and point[1] - step >= 0 and water_map[point[0] - step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] - step * 180 / 255
                    if point[0] + step < mapdimensions[0] and point[1] + step < mapdimensions[1] and water_map[point[0] + step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] + step * 180 / 255
                else:
                    if point[0] + step < mapdimensions[0] and point[1] + step < mapdimensions[1] and water_map[point[0] + step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] + step * 180 / 255
                    if point[0] - step >= 0 and point[1] - step >= 0 and water_map[point[0] - step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] - step * 180 / 255
                if randint(0,1):
                    if point[0] + step < mapdimensions[0] and point[1] - step >= 0 and water_map[point[0] + step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] - step * 180 / 255
                    if point[0] - step >= 0 and point[1] + step < mapdimensions[1] and water_map[point[0] - step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] + step * 180 / 255
                else:
                    if point[0] - step >= 0 and point[1] + step < mapdimensions[1] and water_map[point[0] - step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] + step * 180 / 255
                    if point[0] + step < mapdimensions[0] and point[1] - step >= 0 and water_map[point[0] + step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] - step * 180 / 255
            else:
                if randint(0,1):
                    if point[0] + step < mapdimensions[0] and point[1] - step >= 0 and water_map[point[0] + step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] - step * 180 / 255
                    if point[0] - step >= 0 and point[1] + step < mapdimensions[1] and water_map[point[0] - step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] + step * 180 / 255
                else:
                    if point[0] - step >= 0 and point[1] + step < mapdimensions[1] and water_map[point[0] - step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] + step * 180 / 255
                    if point[0] + step < mapdimensions[0] and point[1] - step >= 0 and water_map[point[0] + step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] - step * 180 / 255
                if randint(0,1):
                    if point[0] - step >= 0 and point[1] - step >= 0 and water_map[point[0] - step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] - step * 180 / 255
                    if point[0] + step < mapdimensions[0] and point[1] + step < mapdimensions[1] and water_map[point[0] + step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] + step * 180 / 255
                else:
                    if point[0] + step < mapdimensions[0] and point[1] + step < mapdimensions[1] and water_map[point[0] + step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] + step * 180 / 255
                    if point[0] - step >= 0 and point[1] - step >= 0 and water_map[point[0] - step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] - step * 180 / 255
        else:
            if randint(0,1):
                if randint(0,1):
                    if point[0] - step >= 0 and point[1] - step >= 0 and water_map[point[0] - step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] - step * 180 / 255
                    if point[0] + step < mapdimensions[0] and point[1] + step < mapdimensions[1] and water_map[point[0] + step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] + step * 180 / 255
                else:
                    if point[0] + step < mapdimensions[0] and point[1] + step < mapdimensions[1] and water_map[point[0] + step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] + step * 180 / 255
                    if point[0] - step >= 0 and point[1] - step >= 0 and water_map[point[0] - step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] - step * 180 / 255
                if randint(0,1):
                    if point[0] + step < mapdimensions[0] and point[1] - step >= 0 and water_map[point[0] + step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] - step * 180 / 255
                    if point[0] - step >= 0 and point[1] + step < mapdimensions[1] and water_map[point[0] - step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] + step * 180 / 255
                else:
                    if point[0] - step >= 0 and point[1] + step < mapdimensions[1] and water_map[point[0] - step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] + step * 180 / 255
                    if point[0] + step < mapdimensions[0] and point[1] - step >= 0 and water_map[point[0] + step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] - step * 180 / 255
            else:
                if randint(0,1):
                    if point[0] + step < mapdimensions[0] and point[1] - step >= 0 and water_map[point[0] + step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] - step * 180 / 255
                    if point[0] - step >= 0 and point[1] + step < mapdimensions[1] and water_map[point[0] - step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] + step * 180 / 255
                else:
                    if point[0] - step >= 0 and point[1] + step < mapdimensions[1] and water_map[point[0] - step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] + step * 180 / 255
                    if point[0] + step < mapdimensions[0] and point[1] - step >= 0 and water_map[point[0] + step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] - step * 180 / 255
                if randint(0,1):
                    if point[0] - step >= 0 and point[1] - step >= 0 and water_map[point[0] - step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] - step * 180 / 255
                    if point[0] + step < mapdimensions[0] and point[1] + step < mapdimensions[1] and water_map[point[0] + step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] + step * 180 / 255
                else:
                    if point[0] + step < mapdimensions[0] and point[1] + step < mapdimensions[1] and water_map[point[0] + step * 180 / 255, point[1] + step * 180 / 255, 0] < 255: return point[0] + step * 180 / 255, point[1] + step * 180 / 255
                    if point[0] - step >= 0 and point[1] - step >= 0 and water_map[point[0] - step * 180 / 255, point[1] - step * 180 / 255, 0] < 255: return point[0] - step * 180 / 255, point[1] - step * 180 / 255
            if randint(0,1):
                if randint(0,1):
                    if point[0] + step < mapdimensions[0] and water_map[point[0] + step, point[1], 0] < 255: return point[0] + step, point[1]
                    if point[1] + step < mapdimensions[1] and water_map[point[0], point[1] + step, 0] < 255: return point[0], point[1] + step
                else:
                    if point[1] + step < mapdimensions[1] and water_map[point[0], point[1] + step, 0] < 255: return point[0], point[1] + step
                    if point[0] + step < mapdimensions[0] and water_map[point[0] + step, point[1], 0] < 255: return point[0] + step, point[1]
                if randint(0,1):
                    if point[0] - step >= 0 and water_map[point[0] - step, point[1], 0] < 255: return point[0] - step, point[1]
                    if point[1] - step >= 0 and water_map[point[0], point[1] - step, 0] < 255: return point[0], point[1] - step
                else:
                    if point[1] - step >= 0 and water_map[point[0], point[1] - step, 0] < 255: return point[0], point[1] - step
                    if point[0] - step >= 0 and water_map[point[0] - step, point[1], 0] < 255: return point[0] - step, point[1]
            else:
                if randint(0,1):
                    if point[0] - step >= 0 and water_map[point[0] - step, point[1], 0] < 255: return point[0] - step, point[1]
                    if point[1] - step >= 0 and water_map[point[0], point[1] - step, 0] < 255: return point[0], point[1] - step
                else:
                    if point[1] - step >= 0 and water_map[point[0], point[1] - step, 0] < 255: return point[0], point[1] - step
                    if point[0] - step >= 0 and water_map[point[0] - step, point[1], 0] < 255: return point[0] - step, point[1]
                if randint(0,1):
                    if point[0] + step < mapdimensions[0] and water_map[point[0] + step, point[1], 0] < 255: return point[0] + step, point[1]
                    if point[1] + step < mapdimensions[1] and water_map[point[0], point[1] + step, 0] < 255: return point[0], point[1] + step
                else:
                    if point[1] + step < mapdimensions[1] and water_map[point[0], point[1] + step, 0] < 255: return point[0], point[1] + step
                    if point[0] + step < mapdimensions[0] and water_map[point[0] + step, point[1], 0] < 255: return point[0] + step, point[1]
        step += 1
    return min_point


def create_water_map(screen):
    water_map = np.zeros(mapdimensions+(3,),dtype=np.uint8)
    for x in water_map:
        for y in x:
            y[0] = 255
            y[2] = 0#randint(0, 7) * 30
    flow_points = [[0, 50]]
    fail_counter = 0
    show_counter = 1
    while fail_counter < 13:
        #koordinaten wählen
        point = (randint(0, mapdimensions[0] - 1), randint(0, mapdimensions[1] - 1))
        #test
        if water_map[point[0],point[1],0] < 255:
            fail_counter += 1
        else:
            end_point = get_near_flow_point(point, flow_points, water_map)
            if len(flow_points) < 1000: flow_points.append(end_point)
            create_river(water_map, point, end_point)
            fail_counter = 0
        if fail_counter == show_counter:
            pygame.surfarray.blit_array(screen, water_map)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            show_counter += 1
    for x in water_map:
        for y in x:
            if y[0] == 255: y[0] = randint(0,7)*30#180
    return water_map