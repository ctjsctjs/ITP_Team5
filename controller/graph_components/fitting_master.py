'''
References:
================ GENERAL ================
https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly
https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit
================ EXPONENTIAL ================
https://plot.ly/python/exponential-fits/
https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly
https://stackoverflow.com/questions/9559346/deal-with-overflow-in-exp-using-numpy
================ R - SQUARED ================
http://blog.minitab.com/blog/adventures-in-statistics-2/why-is-there-no-r-squared-for-nonlinear-regression
https://stackoverflow.com/questions/38816154/obtaining-polynomial-regression-stats-in-numpy
http://statisticsbyjim.com/regression/r-squared-invalid-nonlinear-regression/
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2892436/
https://stackoverflow.com/questions/14530770/calculating-r2-for-a-nonlinear-least-squares-fit
https://stackoverflow.com/questions/893657/how-do-i-calculate-r-squared-using-python-and-numpy
================ FORCE COORDINATES ================
https://stackoverflow.com/questions/33539287/how-to-force-specific-points-in-curve-fitting
https://stackoverflow.com/questions/15191088/how-to-do-a-polynomial-fit-with-fixed-points
'''
import plotly.plotly as py
import plotly.graph_objs as go

# Line Fitting
import numpy as np
from scipy import stats  # For linregress

# Data Reading
from openpyxl import load_workbook

# R generation
import math
from operator import mul

# K Means
from sklearn.cluster import KMeans

def generateGraphTest():
    # Test Comparison
    wb = load_workbook(filename='C:\\Users\\Sean\\Downloads\\DSME 10700_2018_Combined_A.xlsx', data_only=True)
    ws = wb['Before DD']
    ws2 = wb['After DD']

    beforeSpeed = []
    beforeME = []
    count = 0
    for row in ws.rows:
        count += 1
        ##    if count == 12:
        ##        break
        if count <= 1:
            continue
        ##    if row[0].value == 'APL BARCELONA':
        if (row[9].value is not None) and (row[20].value is not None):
            beforeSpeed.append(float(row[9].value))
            beforeME.append(float(row[20].value))
        else:
            pass

    x = beforeSpeed
    y = beforeME

    afterSpeed = []
    afterME = []
    count = 0
    for row in ws2.rows:
        count += 1
        ##    if count == 12:
        ##        break
        if count <= 1:
            continue
        ##    if row[0].value == 'APL BARCELONA':
        if (row[9].value is not None) and (row[20].value is not None):
            afterSpeed.append(float(row[9].value))
            afterME.append(float(row[20].value))
        else:
            pass

    x2 = afterSpeed
    y2 = afterME

    print 'K-Means applied to data\n'
    numClusters = len(x) / 3
    numClusters2 = len(x2) / 3
    beforeCoords = np.c_[np.array(x), np.array(y)]
    kmeans = KMeans(n_clusters=numClusters, random_state=0).fit(beforeCoords)
    x = [xN for xN, yN in kmeans.cluster_centers_]
    y = [yN for xN, yN in kmeans.cluster_centers_]

    afterCoords = np.c_[np.array(x2), np.array(y2)]
    kmeans2 = KMeans(n_clusters=numClusters2, random_state=0).fit(afterCoords)
    x2 = [xN for xN, yN in kmeans2.cluster_centers_]
    y2 = [yN for xN, yN in kmeans2.cluster_centers_]

    # Polyfit method master race 1=linear, 2=quadratic, 3=cubic, 4=idk
    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)
    print 'Before DD Formula'
    print f
    print 'After DD Formula'
    z2 = np.polyfit(x2, y2, 2)
    f2 = np.poly1d(z2)
    print f2
    print 'Individual Values of After DD formula (debug purposes)'
    for item in f2:
        print item  # individual value

    # calculate new x's and y's
    x_new = np.linspace(min(x), max(x), max(x))
    y_new = f(x_new)

    x_new2 = np.linspace(min(x2), max(x2), max(x2))
    y_new2 = f2(x_new2)

    # Creating the dataset, and generating the plot
    trace1 = go.Scatter(
        x=x_new2,
        y=y_new2,
        mode='lines',
        marker=go.Marker(color='rgb(255, 127, 14)'),
        name='After DD'
    )

    trace2 = go.Scatter(
        x=x_new,
        y=y_new,
        mode='lines',
        marker=go.Marker(color='rgb(31, 119, 180)'),
        name='Before DD'
    )

    trace3 = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=go.Marker(color='rgb(255, 127, 14)'),
        name='Before DD'
    )

    trace4 = go.Scatter(
        x=x2,
        y=y2,
        mode='markers',
        marker=go.Marker(color='rgb(31, 119, 180)'),
        name='After DD '
    )

    layout = go.Layout(
        title='FO Consumption & Speed Graph',
        plot_bgcolor='rgb(229, 229, 229)',
        xaxis=go.XAxis(title='Avg speed (knts)', zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
        yaxis=go.YAxis(title='FO cons. / 24 hrs (tons)', zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
        ##                  annotations=[annotation]
    )

    ##data = [trace1, trace2]
    data = [trace1, trace2, trace3, trace4]
    fig = go.Figure(data=data, layout=layout)
    return fig

def calculate_r(xList, yList):
    ##    Defective Cubic R**2
    ##    yMean = sum(yList)/len(yList)
    ##    sstot = sum([(y - yMean)**2 for y in yList])
    ##    ssres = []
    ##    count = 0
    ##    for x in xList:
    ##        yVal = 0.1738*(x**3) - 10.53*(x**2) - 212.8*x - 1275
    ##        ssres.append((yList[count] - yVal)**2)
    ##        count += 1
    ##    ssres2 = sum(ssres)
    ##    r3 = 1 - (ssres2/sstot)
    ##    print "R2 cube = " + str(r3)

    # Linear
    sumXY = sum(map(mul, xList, yList))
    sumX = sum(xList)
    sumY = sum(yList)
    n = len(xList)
    sumX2 = sum([i ** 2 for i in xList])
    sumY2 = sum([i ** 2 for i in yList])

    rValue = (sumXY - (sumX * sumY) / n) / math.sqrt((sumX2 - sumX ** 2 / n) * (sumY2 - sumY ** 2 / n))

    print "R=" + str(rValue)
    print "R-Squared=" + str(rValue ** 2)
    return rValue


# linregress method with R value
##slope, intercept, r_value, p_value, std_err = stats.linregress(x2,y2)
##print slope
##print intercept
##print r_value
##calculate_r(x2, y2)

# K Means (Comment this block to view original graph)


##py.plot(fig, filename='FO Consumption & Speed Polynomial Graph')
