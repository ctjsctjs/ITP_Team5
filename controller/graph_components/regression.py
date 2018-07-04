import numpy as np


# TODO: Replace method content with modular 'fitting_master' component
def linear_regression(x, y):
    polyfit = np.polyfit(x, y, 2)
    polyval = np.polyval(polyfit, x)

    return polyval


# TODO: Rename method
# TODO: Replace method content with modular 'fitting_master' component
def k_means(x, y):
    pass
