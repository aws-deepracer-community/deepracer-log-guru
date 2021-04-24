#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

_WORST_STRAIGHT_STEERING = 8
_IDEAL_PROJECTED_TRAVEL_DISTANCE = 3
_MAX_POSSIBLE_STEERING = 30


def get_brightness_for_steering_straight(event):
    return max(0.1, 1 - 0.9 * abs(event.steering_angle) / _WORST_STRAIGHT_STEERING)


def get_brightness_for_steering_left(event):
    if event.steering_angle > 0:
        return min(1, 0.1 + 0.9 * event.steering_angle / _MAX_POSSIBLE_STEERING)
    else:
        return 0.1


def get_brightness_for_steering_right(event):
    if event.steering_angle < 0:
        return min(1, 0.1 - 0.9 * event.steering_angle / _MAX_POSSIBLE_STEERING)
    else:
        return 0.1


def get_brightness_for_projected_travel_distance(event):
    return min(1, 0.1 + 0.9 * event.projected_travel_distance / _IDEAL_PROJECTED_TRAVEL_DISTANCE)


