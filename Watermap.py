#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame
import numpy as np
from random import random, shuffle

from Config import mapdimensions, directions, slope


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
            y[1] = 0
            y[2] = 0  # randint(0, 7) * 30
    return water_map


def initialize_amount_map():
    return np.zeros(mapdimensions, dtype=np.float)


def clear_amounts(water_map, amount_map):
    for y in range(len(water_map)):
        for x in range(len(water_map[0])):
            water_map[x, y, 1] = 0
            water_map[x, y, 2] = 0
            amount_map[x][y] = 0.0


def create_water_map(screen, flow_point_tuples):
    water_map = initialize_water_map()
    flow_points = []
    for flow_point_tuple in flow_point_tuples:
        flow_points.append(flow_point_tuple[0])
        water_map[flow_point_tuple[0][0], flow_point_tuple[0][1], 0] = flow_point_tuple[1]
    all_points = []
    for x in range(mapdimensions[0]):
        for y in range(mapdimensions[1]):
            all_points.append((x, y))
    shuffle(all_points)
    for point in all_points:
        end_point = get_near_sink(point, flow_points, water_map)
        create_river(water_map, point, end_point)
        if point[0] == 0 and screen:
            pygame.surfarray.blit_array(screen, water_map)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
    return water_map


def calculate_amount_for_pix(water_map, amount_map, pix):
    if water_map[pix[0], pix[1], 2] > 0:
        return amount_map[pix[0]][pix[1]]
    water_amount = 1
    water_map[pix[0], pix[1], 1] = 1
    for dir_no in directions.keys():
        if 0 <= pix[0] + directions[(dir_no + 4) % 8][0] < mapdimensions[0] and \
           0 <= pix[1] + directions[(dir_no + 4) % 8][1] < mapdimensions[1] and \
           water_map[
               pix[0] + directions[(dir_no + 4) % 8][0],
               pix[1] + directions[(dir_no + 4) % 8][1],
               0
           ] / 30 == dir_no:
            if water_map[
                pix[0] + directions[(dir_no + 4) % 8][0],
                pix[1] + directions[(dir_no + 4) % 8][1],
                2
            ] <= 0 and water_map[
                pix[0] + directions[(dir_no + 4) % 8][0],
                pix[1] + directions[(dir_no + 4) % 8][1],
                1
            ] == 1:
                print("Circle detected!")
                #water_amount = int(round(pow(water_amount + 30, 0.6) * slope / 3.0 - 51.3))
                amount_map[pix[0]][pix[1]] = water_amount
                if water_amount > 255:
                    water_map[pix[0], pix[1], 2] = 255
                else:
                    water_map[pix[0], pix[1], 2] = water_amount
                return water_amount
            water_amount += calculate_amount_for_pix(
                water_map,
                amount_map,
                (pix[0] + directions[(dir_no + 4) % 8][0], pix[1] + directions[(dir_no + 4) % 8][1])
            )
    #water_amount = int(round(pow(water_amount + 30, 0.6) * slope / 3.0 - 51.3))
    amount_map[pix[0]][pix[1]] = water_amount
    if water_amount > 255:
        water_map[pix[0], pix[1], 2] = 255
    else:
        water_map[pix[0], pix[1], 2] = water_amount
    return water_amount


def calculate_water_amounts(water_map, amount_map):
    for y in range(len(water_map)):
        for x in range(len(water_map[0])):
            if water_map[x, y, 2] <= 0:
                calculate_amount_for_pix(water_map, amount_map, (x, y))


def direct_flow_pass(water_map, amount_map):
    for y in range(len(water_map)):
        for x in range(len(water_map[0])):
            max_flow_dir = 0
            max_flow_amount = 0
            for direction in directions:
                if 0 <= x + directions[direction][0] < mapdimensions[0] and \
                   0 <= y + directions[direction][1] < mapdimensions[1] and \
                   amount_map[x + directions[direction][0]][y + directions[direction][1]] >= max_flow_amount:
                    max_flow_amount = amount_map[x + directions[direction][0]][y + directions[direction][1]]
                    max_flow_dir = direction
            water_map[x, y, 0] = max_flow_dir * 30
