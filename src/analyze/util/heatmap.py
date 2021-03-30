#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
import math
import typing
import numpy as np

from src.graphics.track_graphics import TrackGraphics
from src.utils.colors import get_color_for_data, ColorPalette


class HeatMap:
    #
    # PUBLIC interface
    #

    def __init__(self, min_x, min_y, max_x, max_y, granularity, allow_repeats: bool):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self._allow_repeats = allow_repeats

        self._granularity = granularity

        x_size = self._get_x_index(max_x) + 1
        y_size = self._get_y_index(max_y) + 1

        self._stats = [[[] for _ in range(x_size)] for _ in range(y_size)]
        self._last_visitor = [[None] * x_size for _ in range(y_size)]

    def visit(self, x, y, visitor, stat: typing.Union[float, int]):
        x_index = self._get_x_index(x)
        y_index = self._get_y_index(y)

        if self._allow_repeats or visitor != self._last_visitor[y_index][x_index]:
            self._last_visitor[y_index][x_index] = visitor
            self._stats[y_index][x_index].append(float(stat))

    def draw_visits(self, track_graphics: TrackGraphics, brightness: int, color_palette: ColorPalette):
        assert brightness in [-1, 0, 1, 2]

        (visits, _, max_visits) = self._get_stats_array(np.count_nonzero)
        if max_visits == 0:
            return

        colour_multiplier = 255 / max_visits / max_visits * 2
        min_visits = max_visits / 10

        if brightness == 1:
            colour_multiplier *= 2
            min_visits /= 2
        elif brightness == 2:
            colour_multiplier *= 3.5
            min_visits /= 3.5
        elif brightness == -1:
            colour_multiplier /= 2
            min_visits *= 1.5

        for yy, visits in enumerate(visits):
            for xx, visit in enumerate(visits):
                if visit >= min_visits:
                    x = self.min_x + self._granularity * xx
                    y = self.min_y + self._granularity * yy

                    data = min(1.0, 30/255 + colour_multiplier / 255 * visit * visit)
                    colour = get_color_for_data(data, color_palette)
                    track_graphics.plot_box(x, y, x + self._granularity, y + self._granularity, colour)

    def draw_statistic(self, track_graphics: TrackGraphics, brightness: int, color_palette: ColorPalette,
                       forced_max_stat=-1, forced_min_stat=-1):
        assert brightness in [-1, 0, 1, 2]

        threshold = round(self._get_stats_count() / 10)

        if brightness == 1:
            threshold /= 2
        elif brightness == 2:
            threshold /= 3.5
        elif brightness == -1:
            threshold *= 1.5

        (stats, min_stat, max_stat) = self._get_stats_array(np.median, threshold)
        if max_stat == 0:
            return

        if forced_max_stat > 0:
            max_stat = forced_max_stat
        if forced_min_stat > 0:
            min_stat = forced_min_stat

        if brightness == 1:
            max_stat *= 0.93
        elif brightness == 2:
            max_stat *= 0.85
            min_stat *= 0.95
        elif brightness == -1:
            min_stat *= 1.1

        if min_stat >= max_stat:
            min_stat = 0.99 * max_stat

        stat_range = max_stat - min_stat

        for yy, stats in enumerate(stats):
            for xx, stat in enumerate(stats):
                if not math.isnan(stat):
                    x = self.min_x + self._granularity * xx
                    y = self.min_y + self._granularity * yy

                    gap_from_best = max_stat - stat
                    data = max(0.1, min(1, 1 - 0.9 * gap_from_best / stat_range))
                    colour = get_color_for_data(data, color_palette)
                    track_graphics.plot_box(x, y, x + self._granularity, y + self._granularity, colour)

    #
    # PRIVATE implementation
    #

    def _get_x_index(self, value):
        value = max(min(value, self.max_x), self.min_x)
        return round((value - self.min_x - self._granularity / 2) / self._granularity)

    def _get_y_index(self, value):
        value = max(min(value, self.max_y), self.min_y)
        return round((value - self.min_y - self._granularity / 2) / self._granularity)

    def _get_stats_count(self):
        count = 0
        for y_stats in self._stats:
            for x_stats in y_stats:
                if x_stats:
                    count = max(count, len(x_stats))
        return count

    def _get_stats_array(self, stat_method: callable, threshold: int = 0):
        min_value = math.nan
        max_value = 0.0
        new_stats = []
        for y_stats in self._stats:
            new_y_stats = []
            for x_stats in y_stats:
                if x_stats and len(x_stats) >= threshold:
                    stat = stat_method(np.array(x_stats))
                    min_value = min(stat, min_value)
                    max_value = max(stat, max_value)
                else:
                    stat = math.nan
                new_y_stats.append(stat)
            new_stats.append(new_y_stats)
        return new_stats, min_value, max_value

    def print_debug(self):
        for v in reversed(self._get_stats_array(np.sum)):
            s = ""
            for w in v:
                if w == 0:
                    s += "  "
                else:
                    s += str(round(w)) + " "
            print(s)




def test_it():
    map = HeatMap(1, 1, 5.99, 7.99, 0.5, True)

    print(map._get_x_index(1))
    print(map._get_x_index(1.24))
    print(map._get_x_index(1.25))
    print(map._get_x_index(1.49))
    print(map._get_x_index(1.51))

    print("-------------------------")

    map.visit(1, 1, "aaa", 1)
    map.visit(6, 7, "bbb", 1)
    map.visit(6, 7, "ccc", 1)

    # map.print_debug()

    map.visit(5.9, 6.9, "zzz", 1)

    map.visit(1.26, 1.26, "a", 1)
    map.visit(1.4, 1.4, "b", 1)
    map.visit(1.6, 1.6, "c", 1)
    map.visit(1.8, 1.8, "d", 1)

    map.visit(3, 3, "d", 1)
    map.visit(4, 4, "d", 1)
    map.visit(5, 5, "d", 1)

    map.print_debug()

    print("=============")
    print(map._stats[0])

    print(map._get_stats_array(np.sum))



# RUN TEST
# test_it()






