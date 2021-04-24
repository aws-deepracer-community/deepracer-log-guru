#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import numpy as np


def get_lap_times(episodes: list):
    lap_times = []

    for e in episodes:
        if e.lap_complete:
            lap_times.append(e.time_taken)

    return np.array(lap_times)


def get_lap_times_per_quarter(episodes: list):
    lap_times = [[], [], [], []]

    for e in episodes:
        if e.lap_complete:
            lap_times[e.quarter - 1].append(e.time_taken)

    return [np.array(lap_times[0]), np.array(lap_times[1]), np.array(lap_times[2]), np.array(lap_times[3])]
