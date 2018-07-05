import numpy as np
from sklearn.cluster import KMeans
from enum import Enum


class GraphMode(Enum):
    LINEAR = 1
    QUADRATIC = 2
    CUBIC = 3
    QUATRIC = 4


# TODO: Replace method content with modular 'fitting_master' component
def regression(x, y, graph_mode=GraphMode.LINEAR):
    z = np.polyfit(x, y, graph_mode.value)
    f = np.poly1d(z)

    x_new = np.linspace(min(x), max(x), max(x))
    y_new = f(x_new)

    return {'x': x_new, 'y': y_new}


# TODO: Check if function works as intended
def k_means(x, y):
    numClusters = len(x) / 3

    beforeCoords = np.c_[np.array(x), np.array(y)]
    kmeans = KMeans(n_clusters=numClusters, random_state=0).fit(beforeCoords)
    x = [xN for xN, yN in kmeans.cluster_centers_]
    y = [yN for xN, yN in kmeans.cluster_centers_]

    return {'x': x, 'y': y}
