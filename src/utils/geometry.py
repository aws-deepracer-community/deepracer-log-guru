#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import math

from src.utils.types import Point


def get_distance_between_points(first, second):
    (x1, y1) = first
    (x2, y2) = second

    x_diff = x2 - x1
    y_diff = y2 - y1

    return math.sqrt(x_diff * x_diff + y_diff * y_diff)


def get_bearing_between_points(start, finish):
    (start_x, start_y) = start
    (finish_x, finish_y) = finish

    direction_in_radians = math.atan2(finish_y - start_y, finish_x - start_x)
    return math.degrees(direction_in_radians)


def get_angle_in_proper_range(angle):
    if angle >= 180:
        return angle - 360
    elif angle <= -180:
        return 360 + angle
    else:
        return angle


def get_turn_between_directions(current, required):
    difference = required - current
    return get_angle_in_proper_range(difference)


def get_edge_point(previous: Point, mid: Point, future: Point, direction_offset: int, distance: float):
    assert direction_offset in [90, -90]
    assert previous != mid

    (previous_x, previous_y) = previous
    (mid_x, mid_y) = mid
    (next_x, next_y) = future

    degrees_to_mid_point = math.degrees(math.atan2(mid_y - previous_y, mid_x - previous_x))
    if mid == future:
        track_heading_degrees = degrees_to_mid_point
    else:
        degrees_from_mid_point = math.degrees(math.atan2(next_y - mid_y, next_x - mid_x))
        degrees_difference = get_turn_between_directions(degrees_to_mid_point, degrees_from_mid_point)
        track_heading_degrees = degrees_to_mid_point + degrees_difference / 2

    radians_to_edge_point = math.radians(track_heading_degrees + direction_offset)

    x = mid_x + math.cos(radians_to_edge_point) * distance
    y = mid_y + math.sin(radians_to_edge_point) * distance

    return x, y


# Distance of point from line comes from Wikipedia
# https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line

def get_distance_of_point_from_line(point: Point, line_point_a: Point, line_point_b: Point):
    (x0, y0) = point
    (x1, y1) = line_point_a
    (x2, y2) = line_point_b

    # print(point, line_point_a, line_point_b)

    upper_expression = abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1))
    lower_expression = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    return upper_expression / lower_expression


# Intersection of two lines comes from Wikipedia
# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line

def get_intersection_of_two_lines(line_a_point_1: Point, line_a_point_2: Point,
                                  line_b_point_1: Point, line_b_point_2: Point) -> Point:
    (x1, y1) = line_a_point_1
    (x2, y2) = line_a_point_2
    (x3, y3) = line_b_point_1
    (x4, y4) = line_b_point_2

    denominator = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))

    if denominator == 0.0:
        return None

    z1 = (x1 * y2) - (y1 * x2)
    z2 = (x3 * y4) - (y3 * x4)

    x = ((z1 * (x3 - x4)) - ((x1 - x2) * z2)) / denominator
    y = ((z1 * (y3 - y4)) - ((y1 - y2) * z2)) / denominator

    return x, y


def is_point_between(point: Point, start: Point, finish: Point):
    bearing_from_start = get_bearing_between_points(start, point)
    bearing_to_finish = get_bearing_between_points(point, finish)
    return abs(get_turn_between_directions(bearing_from_start, bearing_to_finish)) < 1


def is_left_bearing(bearing: float) -> bool:
    return bearing > 0.0001


def is_right_bearing(bearing: float) -> bool:
    return bearing < -0.0001


def get_point_at_bearing(start_point, bearing: float, distance: float):
    (x, y) = start_point

    radians_to_target = math.radians(bearing)

    x2 = x + math.cos(radians_to_target) * distance
    y2 = y + math.sin(radians_to_target) * distance

    return x2, y2
