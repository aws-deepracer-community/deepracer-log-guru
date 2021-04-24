#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import math


def get_pretty_small_float(number, max_value, decimal_places):
    assert 0 <= decimal_places <= 1

    if max_value >= 10 and abs(round(number, decimal_places)) < 10:
        prepend = " "
    else:
        prepend = ""

    full_str = prepend + str(round(number, decimal_places))

    if full_str.count(".") == 1 and decimal_places == 0:
        return full_str[0:-2]
    elif full_str.endswith(".0") and decimal_places == 1:
        return full_str[0:-2] + "  "
    elif full_str.count(".") == 0 and decimal_places == 1:
        return full_str + "  "
    else:
        return full_str


def get_pretty_large_integer(number):
    return "{:,}".format(round(number))


def get_pretty_hours_and_minutes(minutes: int):
    show_hours = math.floor(minutes / 60)
    show_mins = minutes - show_hours * 60

    if show_hours < 10:
        formatted_hours = "0" + str(show_hours)
    else:
        formatted_hours = str(show_hours)

    if show_mins < 10:
        formatted_mins = "0" + str(show_mins)
    else:
        formatted_mins = str(show_mins)

    return formatted_hours + " : " + formatted_mins




def get_pretty_large_float(number):
    return "{:,}".format(number)


def get_pretty_whole_percentage(number):
    return str(round(number)) + " %"
