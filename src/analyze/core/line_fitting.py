import numpy as np
from scipy import stats


def get_linear_regression(plot_x: np.ndarray, plot_y: np.ndarray, r_min: float = 0.0):
    assert 0.0 <= r_min < 1
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

        def linear_line(x):
            return slope * x + intercept
        if abs(r) >= r_min:
            slope_y = list(map(linear_line, analyse_x))
            return analyse_x, slope_y, r
        else:
            return None, None, r
