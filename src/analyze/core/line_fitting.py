import numpy as np
from scipy import stats

# TODO: NaNs are essential in *plot_y* for plotting graphs with gaps, so really I do need to filter out the Nans in here after all!!!
# Sandbox2 has efficient code to strip leading Nans - but then need a slower algorithm for ones in the middle?
# Or perhaps just always simply rebuild an array of just the finite Y values for linear fitting calculation


def get_linear_regression(plot_x: np.ndarray, plot_y: np.ndarray, r_min: float = 0.0):
    assert 0.0 <= r_min < 1
    assert not np.isnan(plot_x).any()     # NaNs screw up line fitting
    assert not np.isnan(plot_y).any()

    (slope_y, r) = (None, None)

    if len(plot_x) >= 3:
        slope, intercept, r, p, std_err = stats.linregress(plot_x, plot_y)

        def linear_line(x):
            return slope * x + intercept
        if abs(r) >= r_min:
            slope_y = list(map(linear_line, plot_x))

    return slope_y, r
