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


def get_target_point(start: Point, finish: Point, direction_offset: int, distance: float):
    assert (direction_offset in [90, -90])

    (start_x, start_y) = start
    (finish_x, finish_y) = finish

    direction_in_radians = math.atan2(finish_y - start_y, finish_x - start_x)

    direction_to_target = math.degrees(direction_in_radians) + direction_offset
    radians_to_target = math.radians(direction_to_target)

    x = finish_x + math.cos(radians_to_target) * distance
    y = finish_y + math.sin(radians_to_target) * distance

    return x, y