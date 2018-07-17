import numpy as np
import scipy
import plotly
# import plotly.plotly as py
import plotly.graph_objs as go
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score
from enum import Enum

class GraphMode(Enum):
    LINEAR = 1
    QUADRATIC = 2
    CUBIC = 3
    QUATRIC = 4


# TODO: Replace method content with modular 'fitting_master' component
def regression(x, y, graph_mode=None):
    if graph_mode is None:
        z, res, _, _, _ = np.polyfit(x, y, GraphMode.LINEAR.value, full=True)
    else:
        z, res, _, _, _ = np.polyfit(x, y, graph_mode, full=True)
    f = np.poly1d(z)
    r2value = r2_score(y, f(x)) # To return this value as well

    x_new = np.linspace(min(x), max(x), max(x))
    y_new = f(x_new)

    return {'x': x_new, 'y': y_new}, r2value, res, f


# TODO: Check if function works as intended
def k_means(x, y, clusters=None):
    # Default cluster
    if clusters is None:
        clusters = len(x) / 3

    beforeCoords = np.c_[np.array(x), np.array(y)]
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(beforeCoords)
    x = [xN for xN, yN in kmeans.cluster_centers_]
    y = [yN for xN, yN in kmeans.cluster_centers_]

    return {'x': x, 'y': y}

def test_3d(x,y,z, xAxis, yAxis, zAxis):
    dataset = np.c_[np.array(x), np.array(y), np.array(z)]
    data = np.array(dataset)

    # plot points and fitted surface using Plotly
    trace1 = go.Scatter3d(
        x=data[:,0],
        y=data[:,1],
        z=data[:,2],
        mode='markers',
        marker=dict(size=4, color='red', line=dict(color='black', width=0.5), opacity=0.8)
    )

    # regular grid covering the domain of the data
    mn = np.min(data, axis=0)
    mx = np.max(data, axis=0)
    X,Y = np.meshgrid(np.linspace(mn[0], mx[0], 20), np.linspace(mn[1], mx[1], 20))
    XX = X.flatten()
    YY = Y.flatten()
    # best-fit quadratic curve (2nd-order)
    A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])

    # evaluate it on a grid
    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)

    # plot points and fitted surface using Plotly
    trace3 = go.Surface(
        z=Z,
        x=X,
        y=Y,
        colorscale='RdBu',
        opacity=0.999
    )

    layout = go.Layout(
        title=xAxis + " vs " + yAxis + " vs " + zAxis,
        width=500,
        height=500,
        scene=dict(
        xaxis=dict(title=xAxis),
        yaxis=dict(title=yAxis),
        zaxis=dict(title=zAxis),),
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
        )
    )
    return trace3, layout
