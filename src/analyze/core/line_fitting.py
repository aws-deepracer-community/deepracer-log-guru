#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import numpy as np
from scipy import stats, optimize

#  TODO - fix duplications, initial check-in just gets it working with different flavours of equation ...


def get_linear_regression(plot_x: np.ndarray, plot_y: np.ndarray):
    assert len(plot_x) == len(plot_y)
    assert not np.isnan(plot_x).any()     # X axis must be complete, no gaps indicated by NaN

    # Remove non-numbers/gaps indicated by the y axis values
    nan_filter = np.isfinite(plot_y)
    analyse_x = plot_x[nan_filter]
    analyse_y = plot_y[nan_filter]

    if len(analyse_x) <= 2:
        return analyse_x, analyse_y, 1
    else:
        slope, intercept, r, p, std_err = stats.linregress(analyse_x, analyse_y)

        min_x = np.min(analyse_x)
        max_x = np.max(analyse_x)
        step_x = (max_x - min_x) / 100
        fitted_x = np.arange(min_x, max_x + step_x, step_x)

        def fitted_line(x):
            return slope * x + intercept

        fitted_y = list(map(fitted_line, fitted_x))
        return fitted_x, fitted_y, r


def f_quadratic(x, a, b, c):
    return a * x + b * x ** 2 + c


def get_quadratic_regression(plot_x: np.ndarray, plot_y: np.ndarray):
    assert len(plot_x) == len(plot_y)
    assert not np.isnan(plot_x).any()     # X axis must be complete, no gaps indicated by NaN

    # Remove non-numbers/gaps indicated by the y axis values
    nan_filter = np.isfinite(plot_y)
    analyse_x = plot_x[nan_filter]
    analyse_y = plot_y[nan_filter]

    if len(analyse_x) <= 2:
        return analyse_x, analyse_y
    else:
        params, _ = optimize.curve_fit(f_quadratic, analyse_x, analyse_y)
        (a, b, c) = params

        min_x = np.min(analyse_x)
        max_x = np.max(analyse_x)
        step_x = (max_x - min_x) / 100
        fitted_x = np.arange(min_x, max_x + step_x, step_x)

        def fitted_line(x):
            return f_quadratic(x, a, b, c)

        fitted_y = list(map(fitted_line, fitted_x))
        return fitted_x, fitted_y


def f_cubic(x, a, b, c, d):
    return a * x + b * x ** 2 + c * x ** 3 + d


def get_cubic_regression(plot_x: np.ndarray, plot_y: np.ndarray):
    assert len(plot_x) == len(plot_y)
    assert not np.isnan(plot_x).any()     # X axis must be complete, no gaps indicated by NaN

    # Remove non-numbers/gaps indicated by the y axis values
    nan_filter = np.isfinite(plot_y)
    analyse_x = plot_x[nan_filter]
    analyse_y = plot_y[nan_filter]

    if len(analyse_x) <= 2:
        return analyse_x, analyse_y
    else:
        params, _ = optimize.curve_fit(f_cubic, analyse_x, analyse_y)
        (a, b, c, d) = params

        min_x = np.min(analyse_x)
        max_x = np.max(analyse_x)
        step_x = (max_x - min_x) / 100
        fitted_x = np.arange(min_x, max_x + step_x, step_x)

        def fitted_line(x):
            return f_cubic(x, a, b, c, d)

        fitted_y = list(map(fitted_line, fitted_x))
        return fitted_x, fitted_y
