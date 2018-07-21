import numpy as np
import scipy
import plotly
import plotly.graph_objs as go
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score
from enum import Enum
import pandas as pd

class GraphMode(Enum):
    LINEAR = 1
    QUADRATIC = 2
    CUBIC = 3
    QUATRIC = 4


# Calculate the best fit line, sum of least squares, equation, r-squared value
def regression(x, y, graph_mode=None):
    if graph_mode is None:
        z, res, _, _, _ = np.polyfit(x, y, GraphMode.QUADRATIC.value, full=True)
    else:
        z, res, _, _, _ = np.polyfit(x, y, graph_mode, full=True)
    f = np.poly1d(z)
    r2value = r2_score(y, f(x)) # To return this value as well

    x_new = np.linspace(0, max(x) + max(x)*0.25, max(x))
    # x_new = np.linspace(0, max(x), max(x))
    y_new = f(x_new)

    return {'x': x_new, 'y': y_new}, r2value, res, f


# Generate the clustered dataset
def k_means(graphSettings, df, clusters=None):
    # Default cluster
    if clusters is None:
        clusters = len(df.index) / 3

    if int(clusters) > df.shape[0]:
        clusters = df.shape[0]

    if graphSettings[0] == "2D":
        beforeCoords = np.c_[df[graphSettings[1]], df[graphSettings[2]]]
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(beforeCoords)
        newDf = pd.DataFrame({graphSettings[1]: [xN for xN, yN in kmeans.cluster_centers_], graphSettings[2]: [yN for xN, yN in kmeans.cluster_centers_]})
    else:
        beforeCoords = np.c_[df[graphSettings[1]], df[graphSettings[2]], df[graphSettings[3]]]
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(beforeCoords)
        newDf = pd.DataFrame({graphSettings[1]: [xN for xN, yN, zN in kmeans.cluster_centers_], graphSettings[2]: [yN for xN, yN, zN in kmeans.cluster_centers_], graphSettings[3]: [zN for xN, yN, zN in kmeans.cluster_centers_]})

    return newDf

# 3D Graph function
def plot_3d(x,y,z, xAxis, yAxis, zAxis):
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
