from dash.dependencies import Input, Output, State

import static.colors as color
import plotly.graph_objs as go

from view.pages.generateGraph import layout, generate_filter_input, add_filters, generate_axis_parameters, \
    generate_graph, add_hidden_filters, generate_dropdown_filter
from controller.graph_components.regression import GraphMode, regression, k_means
from model.database import SQL
from app import app

# Init
sql = SQL()
options = [{'label': i, 'value': i} for i in SQL().get_column_names()]
n_filters = 3
dfs = {}

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
        print vessel
        dfs[vessel] = SQL().get_vessel(vessel=vessel)


# Populate 'gen-filter's
for n in range(n_filters):
    @app.callback(
        Output('gen-filter-input-{}'.format(n + 1), 'options'),
        [Input('gen-filter-dump-{}'.format(n + 1), 'children')])
    def load_filter(dump):
        return [{'label': i, 'value': i} for i in SQL().get_column_names()]
        # return [{'label': i, 'value': i} for i in [1, 2, 3]]


# Generates callbacks for filter options
def create_callback(filter_number):
    @app.callback(
        Output('gen-filter-wrapper-{}'.format(filter_number), 'children'),
        [Input('gen-filter-input-{}'.format(filter_number), 'value')])
    def update_filer(filter):
        return generate_filter_input(get_option_type(filter), filter_number)


# @app.callback(
#     Output('gen-filter-wrapper-{}'.format(filter_number),'children'),
#     [Input('gen-filter-input-{}'.format(filter_number),'value')],
#     [State('gen-filter-wrapper-{}'.format(filter_number),'children')])
# def loadWrapper(gfInput,gfWrapper):
#     gfWrapper = newWrapper
#     return gfWrapper

for n in range(n_filters):
    create_callback(n + 1)

filter_inputs = [State('gen-vessel-input-1', 'value')]
for n in range(n_filters):
    filter_inputs.append(State('gen-filter-input-{}'.format(n + 1), 'value'))
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
    #print(df)
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

#
# @app.callback(
#     Output('g2', 'figure'),
#     [Input('gen-params-store', 'children')],
#     [State('g2', 'figure'),
#      State('gen-vessel-input-1', 'value')])
# def update_graph(value, figure, vessel):
#     if figure is not None:
#         # Update Axis Titles based on Axis Parameters
#         figure['layout']['xaxis']['title'] = value[1]
#         figure['layout']['yaxis']['title'] = value[2]
#         if value[0] == '3D' and value[3] is not None:
#             figure['layout']['yaxis']['title'] = value[3]
#
#         # Populate with 2D Data when X and Y set TODO: Remove hardcode
#         if value[1] is not None and value[2] is not None:
#             if len(figure['data']) < 1:
#                 figure['data'].append({})
#             # Add scatter from first data set
#             df = dfs[vessel].get_2D_data(value[1], value[2], clean=True)
#             figure['data'][0] = go.Scatter(
#                 x=df[value[1]],
#                 y=df[value[2]],
#                 name='First DataSet',
#                 mode='markers',
#                 marker=go.Marker(color=color.red)
#             )
#
#             # Add first Line TODO: Include graphmode from user input
#             if len(figure['data']) < 2:
#                 figure['data'].append({})
#             line_data = regression(df[value[1]], df[value[2]])
#             figure['data'][1] = go.Scatter(
#                 x=line_data['x'],
#                 y=line_data['y'],
#                 name='First Regression',
#                 mode='lines',
#                 marker=go.Marker(color=color.red)
#             )
#
#             # TEST Add clean data set TODO: Use actual components
#             if len(figure['data']) < 3:
#                 figure['data'].append({})
#             figure['data'][2] = go.Scatter(
#                 x=[1, 2, 3, 4, 5],
#                 y=[7, 5, 8, 6, 9],
#                 name='Sample markers',
#                 mode='markers',
#                 marker=go.Marker(color=color.blue)
#             )
#
#             if len(figure['data']) < 4:
#                 figure['data'].append({})
#             k_means([1, 2, 3, 4, 5], [7, 5, 8, 6, 9])
#             figure['data'][3] = go.Scatter(
#                 x=[1, 2, 3, 4, 5],
#                 y=regression([1, 2, 3, 4, 5], [7, 5, 8, 6, 9]),
#                 name='Sample line',
#                 mode='lines',
#                 marker=go.Marker(color=color.blue)
#             )
#
#         return figure
#     return default_figure

@app.callback(
    Output('g2', 'figure'),
    [Input('gen-params-store', 'children'),
    Input('gen-filter-store','children')],
    [State('g2', 'figure'),
     State('gen-vessel-input-1', 'value')],
     )
def update_graph(value,filteredData,figure, vessel):
    print "Filter State: " + str(filteredData)
    if figure is not None and filteredData is None:
        # Update Axis Titles based on Axis Parameters
        figure['layout']['xaxis']['title'] = value[1]
        figure['layout']['yaxis']['title'] = value[2]
        if value[0] == '3D' and value[3] is not None:
            figure['layout']['yaxis']['title'] = value[3]

        # Populate with 2D Data when X and Y set TODO: Remove hardcode
        if value[1] is not None and value[2] is not None:
            if len(figure['data']) < 1:
                figure['data'].append({})
            # Add scatter from first data set
            df = dfs[vessel].get_2D_data(value[1], value[2], clean=True)
            figure['data'][0] = go.Scatter(
                x=df[value[1]],
                y=df[value[2]],
                name='First DataSet',
                mode='markers',
                marker=go.Marker(color=color.red)
            )

            # Add first Line TODO: Include graphmode from user input
            if len(figure['data']) < 2:
                figure['data'].append({})
            line_data = regression(df[value[1]], df[value[2]])
            figure['data'][1] = go.Scatter(
                x=line_data['x'],
                y=line_data['y'],
                name='First Regression',
                mode='lines',
                marker=go.Marker(color=color.red)
            )

            # TEST Add clean data set TODO: Use actual components
            if len(figure['data']) < 3:
                figure['data'].append({})
            figure['data'][2] = go.Scatter(
                x=[1, 2, 3, 4, 5],
                y=[7, 5, 8, 6, 9],
                name='Sample markers',
                mode='markers',
                marker=go.Marker(color=color.blue)
            )

            if len(figure['data']) < 4:
                figure['data'].append({})
            k_means([1, 2, 3, 4, 5], [7, 5, 8, 6, 9])
            figure['data'][3] = go.Scatter(
                x=[1, 2, 3, 4, 5],
                y=regression([1, 2, 3, 4, 5], [7, 5, 8, 6, 9]),
                name='Sample line',
                mode='lines',
                marker=go.Marker(color=color.blue)
            )
        return figure
    elif figure is not None and filterState is not None:
        # Update Axis Titles based on Axis Parameters
        figure['layout']['xaxis']['title'] = value[1]
        figure['layout']['yaxis']['title'] = value[2]
        if value[0] == '3D' and value[3] is not None:
            figure['layout']['yaxis']['title'] = value[3]

        # Populate with 2D Data when X and Y set TODO: Remove hardcode
        if value[1] is not None and value[2] is not None:
            if len(figure['data']) < 1:
                figure['data'].append({})
            # Add scatter from first data set
            df = filteredData.get_2D_data(value[1], value[2], clean=True)
            figure['data'][0] = go.Scatter(
                x=df[value[1]],
                y=df[value[2]],
                name='First DataSet',
                mode='markers',
                marker=go.Marker(color=color.red)
            )

            # Add first Line TODO: Include graphmode from user input
            if len(figure['data']) < 2:
                figure['data'].append({})
            line_data = regression(df[value[1]], df[value[2]])
            figure['data'][1] = go.Scatter(
                x=line_data['x'],
                y=line_data['y'],
                name='First Regression',
                mode='lines',
                marker=go.Marker(color=color.red)
            )

            # TEST Add clean data set TODO: Use actual components
            if len(figure['data']) < 3:
                figure['data'].append({})
            figure['data'][2] = go.Scatter(
                x=[1, 2, 3, 4, 5],
                y=[7, 5, 8, 6, 9],
                name='Sample markers',
                mode='markers',
                marker=go.Marker(color=color.blue)
            )

            if len(figure['data']) < 4:
                figure['data'].append({})
            k_means([1, 2, 3, 4, 5], [7, 5, 8, 6, 9])
            figure['data'][3] = go.Scatter(
                x=[1, 2, 3, 4, 5],
                y=regression([1, 2, 3, 4, 5], [7, 5, 8, 6, 9]),
                name='Sample line',
                mode='lines',
                marker=go.Marker(color=color.blue)
            )

        return figure
    return default_figure

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
    [Input('gen-filter-add', 'n_clicks'),
     Input('gen-filter-dump', 'children')],
    [State('gen-filter', 'children')])
def add_filter(n_clicks, dump, container):
    if n_clicks is None:
        print "Hello"
        return add_hidden_filters(n_filters)
    elif n_clicks <= n_filters:
        container[0]['props']['children'][n_clicks - 1]['props']['style'] = {}
        print container[0]['props']['children'][n_clicks - 1]['props']['style']
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
