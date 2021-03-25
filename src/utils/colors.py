#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import math
from base64 import b16encode
from enum import IntEnum, auto

from matplotlib.colors import Colormap
from matplotlib.pyplot import get_cmap

import src.configuration.personal_configuration as config

_COLORMAP_A = get_cmap(config.COLORMAP_A)
_COLORMAP_B = get_cmap(config.COLORMAP_B)


#
# PUBLIC interface
#

class ColorPalette(IntEnum):
    GREYS = auto()
    DISCRETE_THREE = auto()
    DISCRETE_FIVE = auto()
    MULTI_COLOR_A = auto()
    MULTI_COLOR_B = auto()


def get_color_for_data(data: float, palette: ColorPalette) -> str:
    data = float(data)
    assert 0.0 <= data <= 1.0

    if palette == ColorPalette.GREYS:
        mono_data = round(255 * data)
        return _rgb_color((mono_data, mono_data, mono_data))
    if palette == ColorPalette.DISCRETE_THREE:
        return _discrete_color(3, config.DISCRETE_THREE_COLOURS, data)
    if palette == ColorPalette.DISCRETE_FIVE:
        return _discrete_color(5, config.DISCRETE_FIVE_COLOURS, data)
    if palette == ColorPalette.MULTI_COLOR_A:
        return _matplotlib_color(_COLORMAP_A, data)
    if palette == ColorPalette.MULTI_COLOR_B:
        return _matplotlib_color(_COLORMAP_B, data)


#
# PRIVATE implementation
#

def _rgb_color(rgb: (int, int, int)) -> str:
    return '#' + str(b16encode(bytes(rgb)))[2:8]


def _discrete_color(number_of_colors: int, colors: list, data: float) -> str:
    assert(number_of_colors == len(colors))
    return colors[min(math.floor(data * number_of_colors), number_of_colors - 1)]


def _matplotlib_color(colormap: Colormap, data: float) -> str:
    (r, g, b, a) = colormap.__call__(data)
    r = round(255 * r)
    g = round(255 * g)
    b = round(255 * b)
    return _rgb_color((r, g, b))
