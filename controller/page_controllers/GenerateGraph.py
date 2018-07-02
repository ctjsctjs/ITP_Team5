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

from view.pages.generateGraph import layout, generate_filter_input
from model.database import SQL
from app import app

sql = SQL()
n_filters = 3
dfs = {}


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
    filter_inputs.append(State('gen-filter-value1-{}'.format(n + 1), 'value'))
    filter_inputs.append(State('gen-filter-value2-{}'.format(n + 1), 'value'))


# Actual callback for retrieving inputs
@app.callback(
    Output('gen-filter-store', 'children'),
    [Input('gen-filter-add', 'n_clicks')],
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


# # callback to generate parameter fields depending on mode selected
# @app.callback(
#     Output('gen-params-wrapper', 'children'),
#     [Input('gen-mode-input-1', 'value')])
# def update_filer(value):
#     if (value == "3D"):
#         return html.Div([
#             dcc.Dropdown(
#                 id='gen-paramX-input-1',
#                 placeholder="Parameter X",
#                 options=[
#                     {'label': k, 'value': k} for k in [
#                         'A', 'B', 'C'
#                     ]
#                 ], className='item-element-margin'),
#             dcc.Dropdown(
#                 id='gen-paramY-input-1',
#                 placeholder="Parameter Y",
#                 options=[
#                     {'label': k, 'value': k} for k in [
#                         'A', 'B', 'C'
#                     ]
#                 ]),
#             dcc.Dropdown(
#                 id='gen-paramZ-input-1',
#                 placeholder="Parameter Z",
#                 className="item-element-margin-top",
#                 options=[
#                     {'label': k, 'value': k} for k in [
#                         'A', 'B', 'C'
#                     ]
#                 ])
#         ])
#     else:
#         return html.Div([
#             dcc.Dropdown(
#                 id='gen-paramX-input-1',
#                 placeholder="Parameter X",
#                 options=[
#                     {'label': k, 'value': k} for k in [
#                         'A', 'B', 'C'
#                     ]
#                 ], className='item-element-margin'),
#             dcc.Dropdown(
#                 id='gen-paramY-input-1',
#                 placeholder="Parameter Y",
#                 options=[
#                     {'label': k, 'value': k} for k in [
#                         'A', 'B', 'C'
#                     ]
#                 ]),
#         ])
#
#
# # callback to generate parameter fields depending on mode selected
# @app.callback(
#     Output('gen-right-panel-wrapper', 'children'),
#     [Input('gen-button-1', 'n_clicks')])
# def update_filer(value):
#     if value > 0:
#         return html.Div([
#             # Graph Panel
#             html.Div([
#                 html.H2('Graph Panel', className='item-element-margin'),
#                 dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}],
#                                            'layout': go.Layout(
#                                                xaxis={
#                                                    'title': "Engine Power",
#                                                    'type': 'linear'
#                                                },
#                                                yaxis={
#                                                    'title': "Engine Speed",
#                                                    'type': 'linear'
#                                                },
#                                                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
#                                                hovermode='closest'
#                                            )}
#                           )
#             ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),
#
#             # Information Panel
#             html.Div([
#                 html.Div([
#                     html.H2('Information Panel', className='item-element-margin'),
#                     html.Span([], className="settings-info", id='gen-settings-mode-1'),
#                     html.Span([], className="settings-info", id='gen-settings-series-1'),
#                     html.Span([], className="settings-info", id='gen-settings-vessel-1'),
#                     html.Span([], className="settings-info", id='gen-settings-filter1-1'),
#                     html.Span([], className="settings-info", id='gen-settings-filter2-1'),
#                     html.Span([], className="settings-info", id='gen-settings-filter3-1'),
#                     html.Span([], className="settings-info", id='gen-output-value1-1'),
#                     html.Span([], className="settings-info", id='gen-output-value2-1'),
#                     html.Span([], className="settings-info", id='gen-output-value3-1'),
#                     html.Span([], className="settings-info", id='gen-paramX-output-1'),
#                     html.Span([], className="settings-info", id='gen-paramY-output-1'),
#                     html.Span([], className="settings-info", id='gen-paramZ-output-1'),
#                     html.Span([], className="settings-info", id='gen-settings-output-1'),
#                 ], className='item-wrapper item-settings-panel left-panel', id="item-wrapper"),
#
#                 # Customise Panel
#                 html.Div([
#                     html.H2('Customize Panel', className='item-element-margin'),
#                     html.Div([
#                         html.H5('Parameter options', className='item-element-margin'),
#
#                         # DIV to populate paramater fields
#                         html.Div([], className='item-inline item-element-margin', id="gen-params-wrapper"),
#
#                         # Settings checklist form
#                         html.H5('Settings options', className='item-element-margin'),
#                         dcc.Checklist(
#                             id="gen-settings-input-1",
#                             options=[
#                                 {'label': 'Clustering', 'value': 'clustering'},
#                                 {'label': 'Regression', 'value': 'regression'},
#                                 {'label': 'Color', 'value': 'color'}
#                             ],
#                             labelStyle={'display': 'block', 'margin-bottom': '6px'},
#                             values=[]
#                         )
#                     ], className='item-row item-select-height item-inline'),
#                 ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),
#             ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),
#         ]
#         )

# # callback for retriving inputs
# @app.callback(
#     Output('gen-settings-mode-1', 'children'),
#     [Input('gen-mode-input-1', 'value')])
# def update_output(value):
#     return "Mode: " + str(value)
#
#
# @app.callback(
#     Output('gen-settings-series-1', 'children'),
#     [Input('gen-series-input-1', 'value')])
# def update_output(value):
#     return "Series: " + str(value)
#
#
# @app.callback(
#     Output('gen-settings-vessel-1', 'children'),
#     [Input('gen-vessel-input-1', 'value')])
# def update_output(value):
#     return "Vessel: " + str(value)
#
#
# @app.callback(
#     Output('gen-settings-filter1-1', 'children'),
#     [Input('gen-filter-input-1', 'value')])
# def update_output(value):
#     return "Filter 1: " + str(value)
#
#
# @app.callback(
#     Output('gen-settings-filter2-1', 'children'),
#     [Input('gen-filter-input-2', 'value')])
# def update_output(value):
#     return "Filter 2: " + str(value)
#
#
# @app.callback(
#     Output('gen-settings-filter3-1', 'children'),
#     [Input('gen-filter-input-3', 'value')])
# def update_output(value):
#     return "Filter 3: " + str(value)
#
#
# @app.callback(
#     Output('gen-paramX-output-1', 'children'),
#     [Input('gen-paramX-input-1', 'value')])
# def update_output(value):
#     return "Parameter X: " + str(value)
#
#
# @app.callback(
#     Output('gen-output-value1-1', 'children'),
#     [Input('value-1', 'value')])
# def update_output(value):
#     return "Value 1: " + str(value)
#
#
# @app.callback(
#     Output('gen-output-value2-1', 'children'),
#     [Input('value-2', 'value')])
# def update_output(value):
#     return "Value 2: " + str(value)
#
#
# @app.callback(
#     Output('gen-output-value3-1', 'children'),
#     [Input('value-3', 'value')])
# def update_output(value):
#     return "Value 3: " + str(value)
#
#
# @app.callback(
#     Output('gen-paramY-output-1', 'children'),
#     [Input('gen-paramY-input-1', 'value')])
# def update_output(value):
#     return "Parameter Y: " + str(value)
#
#
# @app.callback(
#     Output('gen-paramZ-output-1', 'children'),
#     [Input('gen-paramZ-input-1', 'value')])
# def update_output(value):
#     return "Parameter Z: " + str(value)
#
#
# @app.callback(
#     Output('gen-settings-output-1', 'children'),
#     [Input('gen-settings-input-1', 'values')])
# def update_output(value):
#     return "Settings: " + str(value)


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
