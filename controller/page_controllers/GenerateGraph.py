from dash.dependencies import Input, Output, State

import static.colors as color
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from view.pages.generateGraph import layout, generate_filter_input, add_filters, generate_axis_parameters, \
    generate_graph, add_hidden_filters, generate_dropdown_filter
from controller.graph_components.regression import GraphMode, regression, k_means, test_3d
from model.database import SQL
from app import app
from config.important_attributes import full_attributes
import collections

# import sympy as sp
# from sympy.abc import x

# Init
options = [{'label': i, 'value': i} for i in SQL().get_column_names()]
n_filters = 10
dfs = {}
# TEMPORARY Variables. TO replace if there is a better way
gr_squared = 0.0
gsols = 0.0
gformula = ""
global gr_squared
global gsols
global gformula

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


# Populate Database field options
@app.callback(
    Output('gen-database-input-1', 'options'),
    [Input('gen-database-input-dump', 'children')])
def load_series_field(dump):
    return [{'label': table, 'value': table} for table in SQL().get_table_names()]


# Populate Series field options
@app.callback(
    Output('gen-series-input-1', 'options'),
    [Input('gen-series-dump', 'children')])
def load_series_field(dump):
    return [{'label': series, 'value': series} for series in SQL().get_all_series()]


# Populate Vessel field options
@app.callback(
    Output('gen-vessel-input-1', 'options'),
    [Input('gen-series-input-1', 'value')])
def load_vessel_field(series):
    return [{'label': i, 'value': i} for i in SQL().get_series(series)]


# Load Vessel Data
@app.callback(
    Output('gen-vessel-store', 'children'),
    [Input('gen-vessel-input-1', 'value')])
def load_vessel_df(vessels):
    if vessels is not None:
        for vessel in vessels:
            if vessel not in dfs:
                dfs[vessel] = SQL().get_vessel(vessel=vessel)


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


# Actual callback for retrieving inputs
@app.callback(
    Output('gen-filter-store', 'children'),
    filter_inputs)
def get_filtered_df(*values):
    # Get specifications
    specifications = []
    for i in range(1, len(values), 3):
        if values[i] is not None:
            specifications.append(get_condition(values[i], values[i + 1], values[i + 2]))
    # Cleanup and prepare conditions
    conditions = []
    for specification in specifications:
        for value in specification:
            conditions.append(value)

    # Obtain filtered df
    runOnce = True
    for vessel in values[0]:
        if runOnce:
            df = dfs[vessel].get_filtered(conditions=conditions)
            print df
            runOnce = False
        else:
            df.append(dfs[vessel].get_filtered(conditions=conditions))
    return df.to_json()
    #return pd.concat(df)


# Generate parameter fields depending on mode selected
@app.callback(
    Output('gen-params-wrapper', 'children'),
    [Input('gen-mode-input-1', 'value')])
def update_filter(value):
    # TODO: Remove hardcoded db table
    options = [{'label': label2, 'value': value2} for label2, value2 in
               SQL().get_attributes("dsme 10700_2018_combined_a_after_dd").items()]
    return generate_axis_parameters(value, options)


# Populate Graph Mode Selection Dropdown
@app.callback(
    Output('gen-regression-input-1', 'options'),
    [Input('gen-regression-input-dump', 'children')])
def load_graphmode_selection(dump):
    return [{'label': item.name, 'value': item.value} for item in GraphMode]


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
    print "UPDATES R SQUARED"
    print gr_squared
    return "R-Squared: " + str(round(gr_squared, 4))


@app.callback(
    Output('gen-settings-sols-1', 'children'),
    [Input('g2', 'figure')])
def update_sols(temp):
    print "UPDATES SOLS"
    print gsols
    return "Sum of Least Squares: " + str(round(gsols, 4))


@app.callback(
    Output('gen-settings-formula-1', 'children'),
    [Input('g2', 'figure')])
def update_formula(temp):
    print "UPDATES FORMULA"
    print gformula
    return str(gformula)


@app.callback(
    Output('g2', 'figure'),
    [Input('gen-params-store', 'children'),
     Input('gen-settings-input-1', 'values'),
     Input('gen-regression-input-1', 'value'),
     Input('gen-kmeans-cluster', 'value'),
     Input('save-settings-btn', 'n_clicks'),
     Input('gen-filter-store', 'children')],
    [State('g2', 'figure'),
     State('gen-vessel-input-1', 'value'),
     State('gen-params-store', 'children'),
     State('gen-settings-input-1', 'values'),
     State('gen-regression-input-1', 'value'),
     State('gen-kmeans-cluster', 'value')])
def update_graph(value, settings, graph_mode, clusters, saveClick, filteredData,
 figure, vessels, valueState, settingsState, graph_modeState, clustersState):
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
        print "DEBUGGER MEEEEE: "
        print filteredData
        # Populate with 2D Data when X and Y set TODO: Remove hardcode + Account for 3D
        if value[1] is None or value[2] is None:
            figure['data'] = []
        else:
            if saveClick is None:
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

                # Create the dataset for the vessels selected
                firstIter = True
                for vessel in vessels:
                    if firstIter:
                        dfsDF = dfs.get(vessel).get_df()
                        firstIter = False
                    else:
                        dfsDF.append(dfs.get(vessel).get_df())

                # Remove any NaN values
                if value[0] == "2D":
                    dfsDF = dfsDF.dropna(subset=[value[1], value[2]])
                else:
                    dfsDF = dfsDF.dropna(subset=[value[1], value[2], value[3]])

                # Remove Outliers
                # def remove_outlier(df, graphInfo):
                #     low = .05
                #     high = .95
                #     quant_df = df.quantile([low, high])
                #     if graphInfo[0] == "2D":
                #         if is_numeric_dtype(df[graphInfo[1]]):
                #             df = df[(df[graphInfo[1]] > quant_df.loc[low, graphInfo[1]]) & (df[graphInfo[1]] < quant_df.loc[high, graphInfo[1]])]
                #         if is_numeric_dtype(df[graphInfo[2]]):
                #             df = df[(df[graphInfo[2]] > quant_df.loc[low, graphInfo[2]]) & (df[graphInfo[2]] < quant_df.loc[high, graphInfo[2]])]
                #     return df

                print "Before Cleaning: "
                # print dfsDF
                print "After Cleaning: "
                print value[1]
                mean = np.mean(dfsDF[value[1]])
                stdio = np.std(dfsDF[value[1]])
                print "Mean: " + str(mean) + " Std: " + str(stdio)
                dfsDF = dfsDF[np.abs(dfsDF[value[1]] - mean) <= (1*stdio)]
                # print dfsDF

                # df = pd.DataFrame(np.random.randn(100, 3))
                # print df
                # from scipy import stats
                # df=df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
                # print "Send Help: "
                # print df

                # df = pd.DataFrame({'Data':np.random.normal(size=200)})
                # # example dataset of normally distributed data.
                # print df
                # df = df[np.abs(df.Data-df.Data.mean()) <= (2*df.Data.std())]
                # # keep only the ones that are within +3 to -3 standard deviations in the column 'Data'.
                # print "Send Help: "
                # print df
                # Generate the Hover Data
                hoverData = []
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

                        figure['data'][1] = go.Scatter(
                            x=line_data['x'],
                            y=line_data['y'],
                            name='Line',
                            mode='lines',
                            # marker=go.Marker(color=color.red)
                        )
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
                        surfacePlot, surfaceLayout = test_3d(dfsDF[value[1].encode('utf8')],
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
        # Clean figure data
        figure['data'] = [i for i in figure['data'] if i is not None]
        return figure
    return default_figure


# settingsInput=[State('gen-mode-input-1', 'value'),
#   State('gen-paramX-input-1', 'value'),
#   State('gen-paramY-input-1', 'value'),
#   State('gen-paramZ-input-1', 'value'),
#   State('gen-settings-input-1', 'values'),
#   State('gen-regression-input-1', 'value'),
#   State('gen-kmeans-cluster', 'value'),
#   State('gen-vessel-input-1', 'value'),
#   State('gen-filter-store','children'),
#   State('g2', 'figure')]
#
# @app.callback(
#     Output('save-test','figure'),
#     [Input('save-settings-btn','n_clicks')],
#     settingsInput)
# def update_save_graph(saveClick,*settingData):
#     if saveClick > 0:
#         # print (settingData)
#         # print (settingData[0])
#         # print (settingData[1])
#         # print (settingData[2])
#         # print (settingData[3])
#         # print (settingData[4][1])
#         # print (settingData[5])
#         # print (settingData[6])
#         # print (settingData[7])
#         # print (settingData[8])
#         # Clean data
#         if settingData[8] is None:
#             dff = dfs[settingData[7]].get_2D_data(settingData[1], settingData[2], clean=True)
#         else:
#             dfToJson = pd.read_json(settingData[8])
#             dfClean = dfToJson[[settingData[1], settingData[2]]]
#             dff = dfClean.dropna()
#
#         # K-means if 'clustering' toggled
#         if 'clustering' in settingData[4]:
#             df = k_means(dff[settingData[1]], dff[settingData[2]], clusters)
#         else:
#             df = {'x': dff[settingData[1]], 'y': dff[settingData[2]]}
#
#         # Add scatter from data set if 'datapoints' toggled
#         if len(settingData[9]['data']) < 1:
#             settingData[9]['data'].append({})
#         if 'datapoints' in settingData[4]:
#             settingData[9]['data'][0] = go.Scatter(
#                 x=df['x'],
#                 y=df['y'],
#                 name='Saved DataSet',
#                 mode='markers',
#                 marker=go.Marker(color='rgb(44,180,177)')
#             )
#         else:
#             settingData[9]['data'][0] = None
#
#         # Add Line/Curve if 'regression' toggled
#         if len(settingData[9]['data']) < 2:
#             settingData[9]['data'].append({})
#         if 'regression' in settingData[4]:
#             line_data = regression(df['x'], df['y'], settingData[5])
#             settingData[9]['data'][1] = go.Scatter(
#                 x=line_data['x'],
#                 y=line_data['y'],
#                 name='Saved Regression',
#                 mode='lines',
#                 marker=go.Marker(color='rgb(232,12,194)')
#             )
#         else:
#             settingData[9]['data'][1] = None
#
#     # Clean figure data
#     settingData[9]['data'] = [i for i in settingData[9]['data'] if i is not None]
#
#     return settingData[9]


# callback to generate parameter fields depending on mode selected
@app.callback(
    Output('gen-right-panel-wrapper', 'children'),
    [Input('gen-button-1', 'n_clicks')],
    [State('gen-mode-input-1', 'value')])
def update_filer(value, mode):
    if value > 0:
        return generate_graph(mode, options)


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
    return "Vessel: " + str(value)


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


@app.callback(
    Output('gen-settings-output-1', 'children'),
    [Input('gen-settings-input-1', 'values')])
def update_output(value):
    return "Settings: {}".format([item for item in value])


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
