from dash.dependencies import Input, Output, State

import static.colors as color
import plotly.graph_objs as go
import pandas as pd
import json
import os
import datetime
import numpy as np
from pandas.api.types import is_numeric_dtype
from view.pages.generateGraph import layout, generate_filter_input, add_filters, generate_axis_parameters, \
    generate_graph, add_hidden_filters, generate_dropdown_filter
from controller.graph_components.regression import GraphMode, regression, k_means, plot_3d
from model.database import SQL
from app import app
from config.important_attributes import full_attributes
import collections

# import sympy as sp
# from sympy.abc import x

# Init
# options = [{'label': i, 'value': i} for i in SQL().get_column_names()]
n_filters = 10
dfs = {}
temp_store = {}
# PATH of your Proj:TODO CHANGE PATH TO YOUR PROJ PATH
path = 'C:/Users/YC/Documents/GitHub/ITP_Team5(UI)/'
arr_txt = [x for x in os.listdir('archive') if x.endswith(".txt")]
# TEMPORARY Variables. TO replace if there is a better way
gr_squared = 0.0
gsols = 0.0
gformula = ""
global gr_squared
global gsols
global gformula
global xName
global yName
global zName
global gName
xName = ""
yName = ""
zName = ""
gName = ""
default_figure = {
    'data': [],
    'layout': go.Layout(
        xaxis={
            'title': "Select X Axis",
            'type': 'linear'
        },
        yaxis={
            'title': "Select Y Axis",
            'type': 'linear'
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest'
    )}
#threshold value
threshold = ['None', 1, 1.5, 2, 2.5, 3]

# Populate Database field options
@app.callback(
    Output('gen-database-input-1', 'options'),
    [Input('gen-database-input-dump', 'children')])
def load_series_field(dump):
    return [{'label': table, 'value': table} for table in SQL().get_table_names()]
#
# # Populate Line field options
# @app.callback(
#     Output('gen-loadline-input-1', 'options'),
#     [Input('gen-loadline-dump', 'children')])
# def load_series_field(dump):
#     fileNames = []
#     if arr_txt != []:
#         for item in arr_txt:
#             file = open('archive/' + item, 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             if dictionaryFile.get('graphName') == "":
#                 fileNames.append('(Empty File Name)')
#             else:
#                 fileNames.append(dictionaryFile.get('graphName'))
#         return [{'label': files, 'value': files} for files in fileNames]
#     # else:
#         return None
#
# # Generates callbacks for filter options
# def filter_input1_callback(filter_number):
#     @app.callback(
#         Output('gen-filter-input-{}'.format(filter_number + 1), 'value'),
#         [Input('load-settings-btn','n_clicks'),
#          Input('save-setting-filter','children')])
#     def loadFilters(loadClick,filterData):
#         if loadClick > 0:
#             #print (filter_number*3+1)
#             return '{}'.format(filterData[filter_number*3+1])
#
# # Generates callbacks for filter options
# def filter_value1_callback(filter_number):
#     @app.callback(
#         Output('gen-filter-value1-{}'.format(filter_number + 1), 'value'),
#         [Input('load-settings-btn','n_clicks'),
#          Input('save-setting-filter','children')])
#     def loadFilters(loadClick,filterData):
#         if loadClick > 0:
#             #print (filter_number*3+1)
#             return '{}'.format(filterData[filter_number*3+2])
#
# # Generates callbacks for filter options
# def filter_value2_callback(filter_number):
#     @app.callback(
#         Output('gen-filter-value2-{}'.format(filter_number + 1), 'value'),
#         [Input('load-settings-btn', 'n_clicks'),
#          Input('save-setting-filter', 'children')])
#     def loadFilters(loadClick, filterData):
#         if loadClick > 0:
#             # print (filter_number*3+1)
#             return '{}'.format(filterData[filter_number * 3 + 3])
#
# for k in range(n_filters):
#     filter_input1_callback(k + 1)
#     filter_value1_callback(k + 1)
#     filter_value2_callback(k + 1)
# #

# # load saved mode input
# @app.callback(
#     Output('gen-mode-input-1','value'),
#     [Input('gen-loadline-input-1','value')])
# def load_settings(load):
#     if load is not None:
#         file = open('archive/' + load + ".txt", 'r')
#         dictionaryFile = json.loads(file.read())[0]
#         return '{}'.format(dictionaryFile.get('param')[0])
#
#
# #load saved database input
# @app.callback(
#     Output('gen-database-input-1','value'),
#     [Input('gen-loadline-input-1', 'value')])
# def load_settings(load):
#     if arr_txt != []:
#         if load is not None:
#             file = open('archive/' + load + ".txt", 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             return '{}'.format(dictionaryFile.get('database'))
#
# #load saved series input
# @app.callback(
#     Output('gen-series-input-1','value'),
#     [Input('gen-loadline-input-1', 'value')])
# def load_settings(load):
#     if arr_txt != []:
#         if load is not None:
#             file = open('archive/' + load + ".txt", 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             return '{}'.format(dictionaryFile.get('series'))
#
#   #
# #load saved vessel input
# @app.callback(
#     Output('gen-vessel-input-1','value'),
#     [Input('gen-loadline-input-1', 'value')])
# def load_settings(load):
#     if arr_txt != []:
#         if load is not None:
#             file = open('archive/' + load + ".txt", 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             print(dictionaryFile.get('vessel')[0])
#             return '{}'.format(dictionaryFile.get('vessel')[0])
# #load saved paramX input
# @app.callback(
#     Output('gen-paramX-input-1','value'),
#     [Input('gen-loadline-input-1', 'value')])
# def load_settings(load):
#     if arr_txt != []:
#         if load is not None:
#             file = open('archive/' + load + ".txt", 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             print(dictionaryFile.get('param')[1])
#             return '{}'.format(dictionaryFile.get('param')[1])
#
# #load saved kmeans-cluster input
# @app.callback(
#     Output('gen-kmeans-cluster','value'),
#     [Input('gen-loadline-input-1', 'value')])
# def load_settings(load):
#     if arr_txt != []:
#         if load is not None:
#             file = open('archive/' + load + ".txt", 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             return '{}'.format(dictionaryFile.get('cluster'))
#
# #load saved regression-degree input
# @app.callback(
#     Output('gen-regression-input-1','value'),
#     [Input('gen-loadline-input-1', 'value')])
# def load_settings(load):
#     if arr_txt != []:
#         if load is not None:
#             file = open('archive/' + load + ".txt", 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             return '{}'.format(dictionaryFile.get('regression'))
#
# #load saved settings input
# @app.callback(
#     Output('gen-settings-input-1','values'),
#     [Input('gen-loadline-input-1', 'value')])
# def load_settings(load):
#     if arr_txt != []:
#         if load is not None:
#             file = open('archive/' + load + ".txt", 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             return '{}'.format(dictionaryFile.get('setting'))
#
#
#
# #load saved paramY input
# @app.callback(
#     Output('gen-paramY-input-1','value'),
#     [Input('gen-loadline-input-1', 'value')])
# def load_settings(load):
#     if arr_txt != []:
#         if load is not None:
#             file = open('archive/' + load + ".txt", 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             return '{}'.format(dictionaryFile.get('param')[2])
#
# #load saved paramZ input
# @app.callback(
#     Output('gen-paramZ-input-1','value'),
#     [Input('gen-loadline-input-1', 'value')])
# def load_settings(load):
#     if arr_txt != []:
#         if load is not None:
#             file = open('archive/' + load + ".txt", 'r')
#             dictionaryFile = json.loads(file.read())[0]
#             return '{}'.format(dictionaryFile.get('param')[3])

@app.callback(
    Output('gen-series-input-1', 'options'),
    [Input('gen-series-dump', 'children')])
def load_series_field(dump):
    return [{'label': series, 'value': series} for series in SQL().get_all_series()]


# Populate Vessel field options
@app.callback(
    Output('gen-vessel-input-1', 'options'),
    [Input('gen-series-input-1', 'value'),
     Input('gen-database-input-1', 'value')])
def load_vessel_field(series, db_table):
    if series is not None or series != u'None' or db_table is not None or db_table != u'None':
        vessels_in_series = SQL().get_vessel_from_series(series=series, db_table=db_table)
        if vessels_in_series is not None:
            return [{'label': i, 'value': i} for i in vessels_in_series]
    return


# Load Vessel Data
@app.callback(
    Output('gen-vessel-store', 'children'),
    [Input('gen-vessel-input-1', 'value')],
    [State('gen-database-input-1', 'value')])
def load_vessel_df(vessels, table):
    if vessels is not None:
        for vessel in vessels:
            if vessel not in dfs:
                dfs[vessel] = SQL().get_vessel(table=table, vessel=vessel)


# Load Axis Parameters selection
# @app.callback(
#     Output('gen-params-wrapper', 'children'),
#     [Input('gen-params-dump', 'children'),
#      Input('gen-mode-input-1', 'value')])
# def load_axis_parameteers(dump, mode):
#     return generate_axis_parameters(mode, options)


# Populate 'gen-filter's
for n in range(n_filters):
    @app.callback(
        Output('gen-filter-input-{}'.format(n + 1), 'options'),
        [Input('gen-filter-dump-{}'.format(n + 1), 'children')])
    def load_filter(dump):
        return [{'label': i, 'value': i} for i in SQL().get_column_names()]


# Generates callbacks for filter options
def create_callback(filter_number):
    @app.callback(
        Output('gen-filter-wrapper-{}'.format(filter_number), 'children'),
        [Input('gen-filter-input-{}'.format(filter_number), 'value')])
    def update_filer(filter):
        return generate_filter_input(get_option_type(filter), filter_number)


for n in range(n_filters):
    create_callback(n + 1)

filter_inputs = [Input('gen-vessel-input-1', 'value')]
for n in range(n_filters):
    filter_inputs.append(Input('gen-filter-input-{}'.format(n + 1), 'value'))
    filter_inputs.append(Input('gen-filter-value1-{}'.format(n + 1), 'value'))
    filter_inputs.append(Input('gen-filter-value2-{}'.format(n + 1), 'value'))

filter_state_inputs = [State('gen-vessel-input-1', 'value')]
for n in range(n_filters):
    filter_state_inputs.append(State('gen-filter-input-{}'.format(n + 1), 'value'))
    filter_state_inputs.append(State('gen-filter-value1-{}'.format(n + 1), 'value'))
    filter_state_inputs.append(State('gen-filter-value2-{}'.format(n + 1), 'value'))


# Generate parameter fields depending on mode selected
@app.callback(
    Output('gen-params-wrapper', 'children'),
    [Input('gen-mode-input-1', 'value'),
     Input('gen-database-input-1', 'value')])
def update_filter(value, db_table):
    options = [{'label': label2, 'value': value2} for label2, value2 in
               SQL().get_attributes('{}'.format(db_table)).items()]
    return generate_axis_parameters(value, options)


# Populate Graph Mode Selection Dropdown
@app.callback(
    Output('gen-regression-input-1', 'options'),
    [Input('gen-regression-input-dump', 'children')])
def load_graphmode_selection(dump):
    return [{'label': item.name, 'value': item.value} for item in GraphMode]


# Populate Graph Mode Selection Dropdown
@app.callback(
    Output('gen-threshold-input-1', 'options'),
    [Input('gen-threshold-input-dump', 'children')])
def load_threshold_selection(dump):
    return [{'label': item, 'value': item} for item in threshold]


# Obtain Axis Parameters Input
@app.callback(
    Output('gen-params-store', 'children'),
    [Input('gen-mode-input-1', 'value'),
     Input('gen-paramX-input-1', 'value'),
     Input('gen-paramY-input-1', 'value'),
     Input('gen-paramZ-input-1', 'value')])
def get_params_input(mode, input_x, input_y, input_z):
    return [mode, input_x, input_y, input_z]


# Testing update for Graph Values
@app.callback(
    Output('gen-settings-rsquared-1', 'children'),
    [Input('g2', 'figure')])
def update_rsquared(temp):
    return "R-Squared: " + str(round(gr_squared, 4))


@app.callback(
    Output('gen-settings-sols-1', 'children'),
    [Input('g2', 'figure')])
def update_sols(temp):
    return "Sum of Least Squares: " + str(round(gsols, 4))


@app.callback(
    Output('gen-settings-formula-1', 'children'),
    [Input('g2', 'figure')])
def update_formula(temp):
    eqString, supScript = generateEquationString(gformula)
    return "Formula: " + eqString.format(*supScript)

# Generate the template string and the list of subscript values
def generateEquationString(baseFormula):
    fVariableList = list(baseFormula)
    variableCount = len(fVariableList)
    displayString = u""
    tmpList = []

    for variable in fVariableList:
        displayString += str(round(variable, 3))
        if variableCount > 1:
            supVal = variableCount - 1
            displayString += "x"
            if supVal == 2:
                displayString += "{"+str(len(tmpList))+"}"
                tmpList.append(u'\u00b2')
            elif supVal == 3:
                displayString += "{"+str(len(tmpList))+"}"
                tmpList.append(u'\u00b3')
            elif supVal == 4:
                displayString += "{"+str(len(tmpList))+"}"
                tmpList.append(u'\u2074')
        variableCount -= 1
        displayString += " "
    return displayString, tmpList

@app.callback(
    Output('gen-filter-store', 'children'),
    filter_inputs)
def get_filtered_df(*values):
    return None
    # # Get specifications
    # specifications = []
    # for i in range(1, len(values), 3):
    #     specifications.append(get_condition(values[i], values[i + 1], values[i + 2]))
    # # Cleanup and prepare conditions
    # conditions = []
    # for specification in specifications:
    #     for value in specification:
    #         conditions.append(value)
    #
    # # Obtain filtered df
    # df = []
    # for vessel in values[0]:
    #     df.append(dfs[vessel].get_filtered(conditions=conditions))
    #
    # df = pd.concat(df)
    # return df.to_json()


@app.callback(
    Output('g2', 'figure'),
    [Input('gen-filter-store', 'children'),
     Input('gen-params-store', 'children'),
     Input('gen-settings-input-1', 'values'),
     Input('gen-regression-input-1', 'value'),
     Input('gen-kmeans-cluster', 'value'),
     Input('gen-threshold-input-1', 'value'),
     Input('gen-graph-name','value'),
     Input('x-axis-label','value'),
     Input('y-axis-label','value'),
     Input('z-axis-label', 'value')],
    [State('g2', 'figure'),
     State('gen-vessel-input-1', 'value')]
    + filter_state_inputs)
def update_graph(filtered_df_json, value, settings, graph_mode, clusters, threshold, graphName,xLabel,yLabel,zLabel,figure, vessels, *filter_settings):
    if figure is not None:
        # Update Axis Titles based on Axis Parameters
        # Set X Axis
        # if value[1] is None:
        #     figure['layout']['xaxis']['title'] = default_figure['layout']['xaxis']['title']
        # else:
        #     figure['layout']['xaxis']['title'] = value[1]
        # # Set Y Axis
        # if value[2] is None:
        #     figure['layout']['yaxis']['title'] = default_figure['layout']['yaxis']['title']
        # else:
        #     figure['layout']['yaxis']['title'] = value[2]
        # Set Z Axis if 3D
        # if value[0] == '3D':
        #     if value[3] is None:
        #         figure['layout']['zaxis']['title'] = default_figure['layout']['zaxis']['title']
        #     else:
        #         figure['layout']['zaxis']['title'] = value[3]

        # Populate with 2D Data when X and Y set TODO: Remove hardcode + Account for 3D
        if value[1] is None or value[2] is None:
            figure['data'] = []
        else:
            # Create the dataset for the vessels selected
            # Get specifications
            specifications = []
            for i in range(1, len(filter_settings), 3):
                specifications.append(get_condition(filter_settings[i], filter_settings[i + 1], filter_settings[i + 2]))
            # Cleanup and prepare conditions
            conditions = []
            for specification in specifications:
                for condition in specification:
                    conditions.append(condition)

            # Obtain filtered df
            df = []
            for vessel in filter_settings[0]:
                df.append(dfs[vessel].get_filtered(conditions=conditions))

            dfsDF = pd.concat(df)

            # count = 0
            # for vessel in vessels:
            #     if count == 0:
            #         dfsDF = dfs.get(vessel).get_df()
            #     else:
            #         dfsDF.append(dfs.get(vessel).get_df())

            # dff = []
            # if value[0] == "2D":
            #     for vessel in vessels:
            #         dff.append(dfs[vessel].get_2D_data(value[1], value[2], clean=True))
            # else:
            #     for vessel in vessels:
            #         dff.append(dfs[vessel].get_3D_data(value[1], value[2], value[3]))
            # dff = pd.concat(dff)

            # K-means if 'clustering' toggled NOTE: Update from df to dfs/dfsDF
            # if 'clustering' in settings:
            #     df = k_means(dff[value[1]], dff[value[2]], clusters)
            # else:
            #     if value[0] == "2D":
            #         df = {'x': dff[value[1]], 'y': dff[value[2]]}
            #     else:
            #         df = {'x': dff[value[1]], 'y': dff[value[2]], 'z': dff[value[3]]}

            # Remove any NaN values
            print("THIS IS VALUE: {}".format(value))
            if value[0] == "2D":
                dfsDF = dfsDF.dropna(subset=[value[1], value[2]])
            else:
                dfsDF = dfsDF.dropna(subset=[value[1], value[2], value[3]])

            if threshold != "None":
                # Remove outliers NOTE: Adjust the threshold to modify how strictly filtered the data will be. So far tested 1, 1.5, 3. Strict ~ Lax
                # threshold = 1.5
                # mean = np.mean(dfsDF[value[1]])
                # stdio = np.std(dfsDF[value[1]])
                # print "Mean: " + str(mean) + " Std: " + str(stdio)
                # dfsDF = dfsDF[np.abs(dfsDF[value[1]] - mean) <= (threshold*stdio)]
                #
                # mean = np.mean(dfsDF[value[2]])
                # stdio = np.std(dfsDF[value[2]])
                # print "Mean: " + str(mean) + " Std: " + str(stdio)
                # dfsDF = dfsDF[np.abs(dfsDF[value[2]] - mean) <= (threshold*stdio)]
                #
                # if value[0] == "3D":
                #     mean = np.mean(dfsDF[value[3]])
                #     stdio = np.std(dfsDF[value[3]])
                #     print "Mean: " + str(mean) + " Std: " + str(stdio)
                #     dfsDF = dfsDF[np.abs(dfsDF[value[3]] - mean) <= (threshold*stdio)]
                mean = np.mean(dfsDF[value[1]])
                stdio = np.std(dfsDF[value[1]])
                print "Mean: " + str(mean) + " Std: " + str(stdio)
                dfsDF = dfsDF[np.abs(dfsDF[value[1]] - mean) <= (threshold * stdio)]

                mean = np.mean(dfsDF[value[2]])
                stdio = np.std(dfsDF[value[2]])
                print "Mean: " + str(mean) + " Std: " + str(stdio)
                dfsDF = dfsDF[np.abs(dfsDF[value[2]] - mean) <= (threshold * stdio)]

                if value[0] == "3D":
                    mean = np.mean(dfsDF[value[3]])
                    stdio = np.std(dfsDF[value[3]])
                    print "Mean: " + str(mean) + " Std: " + str(stdio)
                    dfsDF = dfsDF[np.abs(dfsDF[value[3]] - mean) <= (threshold * stdio)]

            hoverData = []
            if 'clustering' in settings:
                dfsDF = k_means(value, dfsDF, clusters)
                hoverData = np.c_[dfsDF[value[1]], dfsDF[value[2]]]
            else:
                # Generate the Hover Data
                # Iterate each row from db
                for key, value1 in dfsDF.iterrows():
                    placeholderText = ""
                    # Iterate each column in the row
                    for index, row in value1.items():
                        # Compare the value in important_attributes
                        for col in full_attributes:
                            if col == index:
                                if isinstance(row, float):
                                    placeholderText += "<b>" + index + "</b>: " + str(round(row, 3)) + "<br>"
                                else:
                                    placeholderText += "<b>" + index + "</b>: " + str(row) + "<br>"
                                break
                    hoverData.append(placeholderText)

            if value[0] == "2D":
                # Add scatter from data set if 'datapoints' toggled
                if len(figure['data']) < 1:
                    figure['data'].append({})
                if 'datapoints' in settings:
                    figure['data'][0] = go.Scatter(
                        x=dfsDF[value[1].encode('utf8')],
                        y=dfsDF[value[2].encode('utf8')],
                        name='Data Marker',
                        mode='markers',
                        text=hoverData,
                        # marker=go.Marker(color=color.red)
                    )
                else:
                    figure['data'][0] = None

                # Add Line/Curve if 'regression' toggled
                if len(figure['data']) < 2:
                    figure['data'].append({})
                if 'regression' in settings:
                    line_data, r_squared, sols, formula = regression(dfsDF[value[1].encode('utf8')],
                                                                     dfsDF[value[2].encode('utf8')], graph_mode)
                    print "R-Squared: " + str(r_squared)
                    print "Sum of Least Squares: " + str(sols)
                    print "A Formula: "
                    print formula
                    global gr_squared, gsols, gformula
                    gr_squared = r_squared
                    gsols = sols
                    gformula = formula

                    eqString, supScript = generateEquationString(formula)

                    figure['data'][1] = go.Scatter(
                        x=line_data['x'],
                        y=line_data['y'],
                        name='Line',
                        mode='lines',
                        # marker=go.Marker(color=color.red)
                    )
                    annotation = go.Annotation(
                        x=min(line_data['x']),
                        y=max(line_data['y']),
                        text="Formula: " + eqString.format(*supScript),
                        showarrow=False
                    )
                    if xLabel == "":
                        xName = value[1]
                    else:
                        xName = xLabel
                    if yLabel == "":
                        yName = value[2]
                    else:
                        yName = yLabel
                    if graphName == "":
                        gName = value[1] + " vs " + value[2]
                    else:
                        gName = graphName

                    layout2d = go.Layout(
                        title=gName,
                        plot_bgcolor='rgb(229, 229, 229)',
                        xaxis=go.XAxis(title=xName, zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                        yaxis=dict(title=yName, zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                        annotations=[annotation],
                        # yaxis2=dict(title='Percentage', gridcolor='blue', overlaying='y', side='right', range=[100,0]),
                    )
                    # layout2d = go.Layout(
                    #     title=value[1] + ' vs ' + value[2],
                    #     plot_bgcolor='rgb(229, 229, 229)',
                    #     xaxis=go.XAxis(title=value[1], zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                    #     yaxis=dict(title=value[2], zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                    #     annotations=[annotation],
                    #     # yaxis2=dict(title='Percentage', gridcolor='blue', overlaying='y', side='right', range=[100,0]),
                    # )
                    figure['layout'] = layout2d
                else:
                    figure['data'][1] = None
            else:
                # 3D
                # Add scatter from data set if 'datapoints' toggled
                if len(figure['data']) < 1:
                    figure['data'].append({})
                if 'datapoints' in settings:
                    figure['data'][0] = go.Scatter3d(
                        x=dfsDF[value[1].encode('utf8')],
                        y=dfsDF[value[2].encode('utf8')],
                        z=dfsDF[value[3].encode('utf8')],
                        name='Data Marker',
                        mode='markers',
                        text=hoverData,
                        # marker=go.Marker(color=color.red)
                    )
                else:
                    figure['data'][0] = None

                # Add Line/Curve if 'regression' toggled
                if len(figure['data']) < 2:
                    figure['data'].append({})
                if 'regression' in settings:
                    surfacePlot, surfaceLayout = plot_3d(dfsDF[value[1].encode('utf8')],
                                                         dfsDF[value[2].encode('utf8')],
                                                         dfsDF[value[3].encode('utf8')], value[1], value[2],
                                                         value[3])
                    figure['data'][1] = surfacePlot
                    figure['layout'] = surfaceLayout

                    # line_data, r_squared, sols, formula = regression(df['x'], df['y'], graph_mode)
                    # print "R-Squared: " + str(r_squared)
                    # print "Sum of Least Squares: " + str(sols)
                    # print "A Formula: "
                    # print formula
                    # global gr_squared, gsols, gformula
                    # gr_squared = r_squared
                    # gsols = sols
                    # gformula = formula
                    #
                    # figure['data'][1] = go.Surface(
                    #     x=line_data['x'],
                    #     y=line_data['y'],
                    #     name='Line',
                    #     mode='lines',
                    #     # marker=go.Marker(color=color.red)
                    # )
                else:
                    figure['data'][1] = None
                if xLabel == "":
                    xName = value[1]
                else:
                    xName = xLabel
                if yLabel == "":
                    yName = value[2]
                else:
                    yName = yLabel
                if zLabel == "":
                    zName = value[3]
                else:
                    zName = zLabel
                if graphName == "":
                    gName = value[1] + " vs " + value[2] + " vs " + value[3]
                else:
                    gName = graphName
                figure['layout']['scene']['xaxis']['title'] = xName
                figure['layout']['scene']['yaxis']['title'] = yName
                figure['layout']['scene']['zaxis']['title'] = zName
                figure['layout']['title'] = gName
        # Clean figure data
        figure['data'] = [i for i in figure['data'] if i is not None]
        return figure
    return default_figure


# save current state of
@app.callback(
    Output('save-setting', 'children'),
    [Input('save-all-btn','n_clicks')],
    [State('gen-params-store','children'),
    State('gen-settings-input-1', 'values'),
    State('gen-regression-input-1', 'value'),
    State('gen-kmeans-cluster', 'value'),
    State('gen-vessel-input-1', 'value'),
    State('gen-series-input-1','value'),
    State('gen-graph-name','value'),
    State('x-axis-label','value'),
    State('y-axis-label','value'),
    State('z-axis-label','value'),
    State('gen-database-input-1','value'),
    State('gen-threshold-input-1','value')])
def saveAll(saveClick,paramState,settingState,regState,clusterState,vesselState,seriesState,graphState,xState,yState,zState,databaseState,thresholdState):
    if saveClick > 0:
        temp_store['param'] = paramState
        temp_store['setting'] = settingState
        temp_store['regression'] = regState
        temp_store['cluster'] = clusterState
        temp_store['vessel'] = vesselState
        temp_store['series'] = seriesState
        temp_store['database']=databaseState
        temp_store['threshold'] = thresholdState
        temp_store['xLabel']=xState
        temp_store['yLabel'] = yState
        temp_store['zLabel'] = zState
        temp_store['dateTime'] = str(datetime.datetime.now().strftime("%d/%m/%y %H:%M"))
        temp_store['graphName'] = graphState
        if os.path.isfile(path + "archive/" + temp_store.get('graphName') + '.txt') == True:
            time = str(datetime.datetime.now().strftime('%H%M%S'))
            temp_store.update({'graphName': graphState + "(" + time + ")"})
        # if os.path.isfile(path+"archive/"+temp_store.get('graphName')+'.txt') == False:
        #     with open(os.path.join(path+'archive',temp_store.get('graphName')+'.txt'),'w') as file:
        #         file.write(json.dumps(temp_store))
        # #If yes, write to graph name that consist of today date
        # elif os.path.isfile(path+"archive/"+temp_store.get('graphName')+'.txt') == True:
        #     temp_store.update({'graphName':graphState+"("+str(datetime.datetime.now().date())+")"})
        #     with open(os.path.join(path + 'archive', temp_store.get('graphName')+ '.txt'), 'w') as file:
        #         file.write(json.dumps(temp_store))


@app.callback(
    Output('save-setting-filter', 'children'),
    [Input('save-all-btn', 'n_clicks')],
    filter_state_inputs)
def saveFilters(saveClick, *filtersInputs):
    if saveClick > 0:
        if filtersInputs not in temp_store.values():
            temp_store['filters'] = filtersInputs
            with open(os.path.join(path + 'archive', temp_store.get('graphName') + '.txt'), 'w') as file:
                file.write(json.dumps([temp_store]))
                file.close()
    return filtersInputs


@app.callback(
    Output('url', 'pathname'),
    [Input('save-all-btn', 'n_clicks')])
def goArchive(savedClick):
    if savedClick > 0:
        return '/Archive'


# callback to generate parameter fields depending on mode selected
@app.callback(
    Output('gen-right-panel-wrapper', 'children'),
    [Input('gen-button-1', 'n_clicks')],
    [State('gen-mode-input-1', 'value')])
def update_filer(value, mode):
    if value > 0:
        options = [{'label': i, 'value': i} for i in SQL().get_column_names()]
        return generate_graph(mode, options)

#
# callback to hide generate graph button and show update button after graph generated
@app.callback(
    Output('gen-button-1', 'style'),
    [Input('gen-button-1', 'n_clicks')])
def update_style(value):
    if value > 0:
        return {'display': 'none'}


# callback to show submit graph button and show update button after graph generated
@app.callback(
    Output('gen-filter-submit', 'style'),
    [Input('gen-button-1', 'n_clicks')])
def update_style(value):
    if value > 0:
        return {'display': 'block'}


# callback for retriving inputs
@app.callback(
    Output('gen-settings-mode-1', 'children'),
    [Input('gen-mode-input-1', 'value')])
def update_output(value):
    return "Mode: " + str(value)


@app.callback(
    Output('gen-settings-series-1', 'children'),
    [Input('gen-series-input-1', 'value')])
def update_output(value):
    return "Series: " + str(value)


@app.callback(
    Output('gen-settings-vessel-1', 'children'),
    [Input('gen-vessel-input-1', 'value')])
def update_output(value):
    vesselString = ""
    for vesselName in value:
        vesselString += str(vesselName).encode('ascii','ignore')
        if vesselName != value[-1]:
            vesselString += ", "
    return "Vessels: " + vesselString


@app.callback(
    Output('gen-settings-filter1-1', 'children'),
    [Input('gen-filter-input-1', 'value')])
def update_output(value):
    return "Filter 1: " + str(value)


@app.callback(
    Output('gen-settings-filter2-1', 'children'),
    [Input('gen-filter-input-2', 'value')])
def update_output(value):
    return "Filter 2: " + str(value)


@app.callback(
    Output('gen-settings-filter3-1', 'children'),
    [Input('gen-filter-input-3', 'value')])
def update_output(value):
    return "Filter 3: " + str(value)


@app.callback(
    Output('gen-paramX-output-1', 'children'),
    [Input('gen-paramX-input-1', 'value')])
def update_output(value):
    return "Parameter X: " + str(value)


@app.callback(
    Output('gen-output-value1-1', 'children'),
    [Input('value-1', 'value')])
def update_output(value):
    return "Value 1: " + str(value)


@app.callback(
    Output('gen-output-value2-1', 'children'),
    [Input('value-2', 'value')])
def update_output(value):
    return "Value 2: " + str(value)


@app.callback(
    Output('gen-output-value3-1', 'children'),
    [Input('value-3', 'value')])
def update_output(value):
    return "Value 3: " + str(value)


@app.callback(
    Output('gen-paramY-output-1', 'children'),
    [Input('gen-paramY-input-1', 'value')])
def update_output(value):
    return "Parameter Y: " + str(value)


@app.callback(
    Output('gen-paramZ-output-1', 'children'),
    [Input('gen-paramZ-input-1', 'value')])
def update_output(value):
    return "Parameter Z: " + str(value)


# @app.callback(
#     Output('gen-settings-output-1', 'children'),
#     [Input('gen-settings-input-1', 'values')])
# def update_output(value):
#     return "Settings: {}".format([item for item in value])
#

# Identifies whether an option is text, numeric or date
def get_option_type(option):
    if option is None:
        return None
    return SQL().get_column_datatypes(column=option, singular=True)


# Craft condition
def get_condition(option, value1, value2):
    result = []
    option_type = get_option_type(option)

    if option_type is None:
        pass
    elif option_type == 'varchar':
        if value1 != '':
            result.append((option, "==", "'{}'".format(value1)))
    elif option_type == 'int' or option_type == 'float':
        if value1 != '':
            result.append((option, ">=", value1))
        if value2 != '':
            result.append((option, "<=", value2))
    elif option_type == 'datetime':
        if value1 != '':
            result.append((option, ">=", value1))
        if value2 != '':
            result.append((option, "<=", value2))

    return result


@app.callback(
    Output('gen-filter', 'children'),
    [Input('gen-filter-add', 'n_clicks'),
     Input('gen-filter-dump', 'children')],
    [State('gen-filter', 'children')])
def add_filter(n_clicks, dump, container):
    if n_clicks is None:
        return add_hidden_filters(n_filters)
    elif n_clicks <= n_filters:
        container[0]['props']['children'][n_clicks - 1]['props']['style'] = {}
        # print container[0]['props']['children'][n_clicks - 1]['props']['style']
    return container


    #     print container[0]['props']['children'][n_clicks]
    #     container[0]['props']['children'][n_clicks] = generate_dropdown_filter(n_clicks)
    #     print "Hello"
    #     print container[0]['props']['children'][n_clicks]
    #     return container
    #     # return add_filters(n_clicks)


# @app.callback(
#     Output('gen-filter', 'children'),
#     [Input('gen-filter-add', 'n_clicks'),
#      Input('gen-filter-dump', 'children')],
#     [State('gen-filter', 'children')])
# def add_filter(n_clicks, dump, container):
#     if n_clicks is None:
#         print "Hello"
#         return add_hidden_filters(n_filters)
#     else:
#         # print container[0]['props']['children'][0]
#         print container[0]['props']['children'][n_clicks]
#         container[0]['props']['children'][n_clicks] = generate_dropdown_filter(n_clicks)
#         print "Hello"
#         print container[0]['props']['children'][n_clicks]
#         return container
#         # return add_filters(n_clicks)


# @app.callback(
#     Output('gen-filter-container','children'),
#     [Input('gen-filter-add', 'n_clicks')],
#     [State('gen-filter-container','children')])
# def loadFilter(n_clicks,gfContainer):
#     for i in n_filters:
#         if i < n_clicks:
#             return add_filters(n_clicks)
#         else:
#             #add_hidden_filter(n_clicks)

# TEST Catch data in graph
@app.callback(
    Output('g2-store', 'children'),
    [Input('gen-filter-line', 'n_clicks'),
     Input('gen-filter-submit', 'n_clicks')],
    [State('g2', 'figure')])
def catch_data(dump1, dump2, figure):
    pass
    # for item in figure:
    #     print item

# # Populate graph with data
# @app.callback(
#     Output('g2', 'figure'),
#     [Input('gen-filter-submit', 'n_clicks')],
#     [State('g2', 'figure')])
# def populate_graph(dump, fig):
#     if fig is not None:
#         for item in fig:
#             print(item)
#     return figure

# @app.callback(
#     Output('gen-test-store', 'children'),
#     [Input('gen-params-store', 'children')],
#     [State('g2', 'figure')])
# def update_graph(value, fig):
#     print(fig)
#
# @app.callback(
#     Output('gen-filtered-data','children'),
#     [Input('gen-filter-store','value')])
# def filtered_data(filterData):
#     print "Im Here"
#     print filterData
