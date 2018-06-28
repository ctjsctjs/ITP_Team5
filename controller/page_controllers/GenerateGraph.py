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


# Populate 'gen-filter's
for n in range(1, 4):
    @app.callback(
        Output('gen-filter-input-%d' % n, 'options'),
        [Input('gen-filter-dump-%d' % n, 'children')])
    def populate_filter(dump):
        return [{'label': i, 'value': i} for i in SQL().get_column_names()]


# callback go generate filter for filter 1
for n in range(1, 4):
    # callback go generate filter for filter 1
    @app.callback(
        Output('gen-filter-wrapper-%d' % n, 'children'),
        [Input('gen-filter-input-%d' % n, 'value')])
    def update_filer(filter):
        if filter is not None:
            option_type = sql.get_column_datatypes(column=filter, singular=True)
            return generate_filter_input(option_type, n)


# callback to generate parameter fields depending on mode selected
@app.callback(
    Output('gen-params-wrapper', 'children'),
    [Input('gen-mode-input-1', 'value')])
def update_filer(value):
    if (value == "3D"):
        return html.Div([
            dcc.Dropdown(
                id='gen-paramX-input-1',
                placeholder="Parameter X",
                options=[
                    {'label': k, 'value': k} for k in [
                        'A', 'B', 'C'
                    ]
                ], className='item-element-margin'),
            dcc.Dropdown(
                id='gen-paramY-input-1',
                placeholder="Parameter Y",
                options=[
                    {'label': k, 'value': k} for k in [
                        'A', 'B', 'C'
                    ]
                ]),
            dcc.Dropdown(
                id='gen-paramZ-input-1',
                placeholder="Parameter Z",
                className="item-element-margin-top",
                options=[
                    {'label': k, 'value': k} for k in [
                        'A', 'B', 'C'
                    ]
                ])
        ])
    else:
        return html.Div([
            dcc.Dropdown(
                id='gen-paramX-input-1',
                placeholder="Parameter X",
                options=[
                    {'label': k, 'value': k} for k in [
                        'A', 'B', 'C'
                    ]
                ], className='item-element-margin'),
            dcc.Dropdown(
                id='gen-paramY-input-1',
                placeholder="Parameter Y",
                options=[
                    {'label': k, 'value': k} for k in [
                        'A', 'B', 'C'
                    ]
                ]),
        ])


# callback to generate parameter fields depending on mode selected
@app.callback(
    Output('gen-right-panel-wrapper', 'children'),
    [Input('gen-button-1', 'n_clicks')])
def update_filer(value):
    if value > 0:
        return html.Div([
            # Graph Panel
            html.Div([
                html.H2('Graph Panel', className='item-element-margin'),
                dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}],
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
                          )
            ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),

            # Information Panel
            html.Div([
                html.Div([
                    html.H2('Information Panel', className='item-element-margin'),
                    html.Span([], className="settings-info", id='gen-settings-mode-1'),
                    html.Span([], className="settings-info", id='gen-settings-series-1'),
                    html.Span([], className="settings-info", id='gen-settings-vessel-1'),
                    html.Span([], className="settings-info", id='gen-settings-filter1-1'),
                    html.Span([], className="settings-info", id='gen-settings-filter2-1'),
                    html.Span([], className="settings-info", id='gen-settings-filter3-1'),
                    html.Span([], className="settings-info", id='gen-output-value1-1'),
                    html.Span([], className="settings-info", id='gen-output-value2-1'),
                    html.Span([], className="settings-info", id='gen-output-value3-1'),
                    html.Span([], className="settings-info", id='gen-paramX-output-1'),
                    html.Span([], className="settings-info", id='gen-paramY-output-1'),
                    html.Span([], className="settings-info", id='gen-paramZ-output-1'),
                    html.Span([], className="settings-info", id='gen-settings-output-1'),
                ], className='item-wrapper item-settings-panel left-panel', id="item-wrapper"),

                # Customise Panel
                html.Div([
                    html.H2('Customize Panel', className='item-element-margin'),
                    html.Div([
                        html.H5('Parameter options', className='item-element-margin'),

                        # DIV to populate paramater fields
                        html.Div([], className='item-inline item-element-margin', id="gen-params-wrapper"),

                        # Settings checklist form
                        html.H5('Settings options', className='item-element-margin'),
                        dcc.Checklist(
                            id="gen-settings-input-1",
                            options=[
                                {'label': 'Clustering', 'value': 'clustering'},
                                {'label': 'Regression', 'value': 'regression'},
                                {'label': 'Color', 'value': 'color'}
                            ],
                            labelStyle={'display': 'block', 'margin-bottom': '6px'},
                            values=[]
                        )
                    ], className='item-row item-select-height item-inline'),
                ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),
            ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),
        ]
        )


# Actual callback for retrieving inputs
@app.callback(
    Output('test-vessel-filter-2-input-dump', 'children'),
    [Input('test-vessel-filter-specification-submit2', 'n_clicks')],
    [State('test-vessel-dropdown', 'value'),
     State('test-vessel-filter-option', 'value'),
     State('test-vessel-filter-specification-input1', 'value'),
     State('test-vessel-filter-specification-input2', 'value')])
def get_specification2(dump, vessel, option, input1, input2):
    print("HELLO")

    # Return DF after filter
    return

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
    return "Parameter Z: " + str(value)


@app.callback(
    Output('gen-settings-output-1', 'children'),
    [Input('gen-settings-input-1', 'values')])
def update_output(value):
    return "Settings: " + str(value)
