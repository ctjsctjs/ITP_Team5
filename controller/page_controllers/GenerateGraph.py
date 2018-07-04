from dash.dependencies import Input, Output, State, Event
import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

from view.pages.generateGraph import layout, generate_filter_input, add_filters, generate_axis_parameters, \
    generate_graph
from model.database import SQL
from app import app

# Init
sql = SQL()
options = [{'label': i, 'value': i} for i in SQL().get_column_names()]
n_filters = 1
dfs = {}

figure = {
    'data': [{'y': [1, 2, 3]}],
    'layout': go.Layout(
        xaxis={
            'title': "Engine Power",
            'type': 'linear'
        },
        yaxis={
            'title': "Engine Speed",
            'type': 'linear'
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest'
    )}


# TODO: Load vessel options based on series
# Populate Vessel field options
@app.callback(
    Output('gen-vessel-input-1', 'options'),
    [Input('gen-series-input-1', 'value')])
def load_vessel_field(series):
    print("THIS IS SERIES: {}".format(series))
    return [{'label': i, 'value': i} for i in SQL().get_vessels()]


# Load Vessel Data
@app.callback(
    Output('gen-vessel-store', 'children'),
    [Input('gen-vessel-input-1', 'value')])
def load_vessel_df(vessel):
    if vessel not in dfs:
        dfs[vessel] = SQL().get_vessel(vessel=vessel)


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

filter_inputs = [State('gen-vessel-input-1', 'value')]
for n in range(n_filters):
    filter_inputs.append(State('gen-filter-input-{}'.format(n + 1), 'value'))
    print('gen-filter-input-{}'.format(n + 1))
    filter_inputs.append(State('gen-filter-value1-{}'.format(n + 1), 'value'))
    filter_inputs.append(State('gen-filter-value2-{}'.format(n + 1), 'value'))


# Actual callback for retrieving inputs
@app.callback(
    Output('gen-filter-store', 'children'),
    [Input('gen-filter-submit', 'n_clicks')],
    filter_inputs)
def get_filtered_df(dump, *values):
    # Get specifications
    specifications = []
    for i in range(1, len(values), 3):
        specifications.append(get_condition(values[i], values[i + 1], values[i + 2]))

    # Cleanup and prepare conditions
    conditions = []
    for specification in specifications:
        for value in specification:
            conditions.append(value)

    # Obtain filtered df
    df = dfs[values[0]].get_filtered(conditions=conditions)
    print(df)
    return


# callback to generate parameter fields depending on mode selected
@app.callback(
    Output('gen-params-wrapper', 'children'),
    [Input('gen-mode-input-1', 'value')])
def update_filer(value):
    options = [{'label': i, 'value': i} for i in SQL().get_column_names()]
    return generate_axis_parameters(value, options)


# Obtain Axis Parameters Input
@app.callback(
    Output('gen-params-store', 'children'),
    [Input('gen-mode-input-1', 'value'),
     Input('gen-paramX-input-1', 'value'),
     Input('gen-paramY-input-1', 'value'),
     Input('gen-paramZ-input-1', 'value')])
def get_params_input(mode, input_x, input_y, input_z):
    print(mode)
    print(input_x)
    print(input_y)
    print(input_z)
    return [mode, input_x, input_y, input_z]


@app.callback(
    Output('g2', 'figure'),
    [Input('gen-params-store', 'children')],
    [State('g2', 'figure'),
     State('gen-vessel-input-1', 'value')])
def update_graph(value, fig, vessel):
    if fig is not None:
        # Update Axis Titles based on Axis Parameters
        fig['layout']['xaxis']['title'] = value[1]
        fig['layout']['yaxis']['title'] = value[2]
        if value[0] == '3D' and value[3] is not None:
            fig['layout']['yaxis']['title'] = value[3]

        # Populate with 2D Data TODO: Multiple lines/curves
        if value[1] is not None and value[2] is not None:
            print("THIS IS VESSEL: {}".format(vessel))
            df = dfs[vessel].get_2D_data(value[1], value[2], clean=True)
            fig['data'][0]['x'] = df[value[1]]
            fig['data'][0]['y'] = df[value[2]]

        print(fig['data'])

        return fig
    return figure


# callback to generate parameter fields depending on mode selected
@app.callback(
    Output('gen-right-panel-wrapper', 'children'),
    [Input('gen-button-1', 'n_clicks')],
    [State('gen-mode-input-1', 'value')])
def update_filer(value, mode):
    if value > 0:
        return generate_graph(mode, options)


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
    return "Settings: " + str(value)


# Identifies whether an option is text, numeric or date
def get_option_type(option):
    if option is None:
        return None
    return sql.get_column_datatypes(column=option, singular=True)


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
    [Input('gen-filter-add', 'n_clicks')])
def add_filter(n_clicks):
    return add_filters(n_clicks)


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
