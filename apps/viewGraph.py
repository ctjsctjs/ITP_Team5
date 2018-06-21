from dash.dependencies import Input, Output
import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from app import app

# Read data from a csv and setup 3D graph data
z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
data = [
go.Surface(
z=z_data.as_matrix()
)
]
layout = go.Layout(
title='Graph 1',
autosize=False,
width=500,
height=500,
margin=dict(
l=65,
r=50,
b=65,
t=90
)
)

stock = 'TSLA'
start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2018, 2, 8)
df = web.DataReader(stock, 'morningstar', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
df = df.drop("Symbol", axis=1)

layout = html.Div([

#Header
html.Div([
    html.H1('View Graph', className='header-title'),

    #item-button, generate graph
    dcc.Link('Save', href='/apps/viewGraph', className='button item-element-margin header-button'),
    dcc.Link('Export', href='/apps/viewGraph', className='button item-element-margin header-button')

    ], className='wrapper-white header-wrapper page-width'),


    #body-wrapper
    html.Div([

    #body-Content
    html.Div([

#item-row
html.Div([

#panel-left
html.Div([
html.Div([
    html.H2('Graph 1', className='item-element-margin'),

    dcc.Dropdown(
        id='app-graph-dropdown',
        className='panel-item-dropdown item-element-margin',
        placeholder="Mode",
        options=[
            {'label': i, 'value': i} for i in [
                '2D', '3D'
            ]
    ]),
    dcc.Dropdown(
        id='app-graph-dropdown',
        className='panel-item-dropdown item-element-margin',
        placeholder="Parameter X",
        options=[
            {'label': i, 'value': i} for i in [
                'Speed', 'Power', 'Draft', 'RPM'
            ]
    ]),
    dcc.Dropdown(
        id='app-graph-dropdown',
        className='panel-item-dropdown item-element-margin',
        placeholder="Parameter Y",
        options=[
            {'label': i, 'value': i} for i in [
                'Speed', 'Power', 'Draft', 'RPM'
            ]
        ]),
    dcc.Dropdown(
            id='app-graph-dropdown',
            className='panel-item-dropdown item-element-margin',
            placeholder="Filter",
            options=[
                {'label': i, 'value': i} for i in [
                    'Series', 'Name', 'Date'
                ]
        ]),
    dcc.Dropdown(
            id='app-graph-dropdown',
            className='panel-item-dropdown item-element-margin',
            placeholder="Name",
            options=[
                {'label': i, 'value': i} for i in [
                    'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                ]
            ]),
    html.Button('Add Filter', className='button item-element-margin', id="add-button", n_clicks=0)

], className='item-wrapper'),
], className='panel-left'),

    #panel-right
    html.Div([
        html.Div([
            html.Div(id='app-graph-display-value'),
                html.Div([
                html.Div([
                        html.H3('Column 3'),
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
                                                )})
                    ], className="eight columns")
            ], className="row"),
        ], className='item-wrapper'),
        ], className='panel-right'),
        ], className='item-row item-element-margin overflow-auto'),
        ], className='content-wrapper page-width')],
    className='wrapper-grey')
])


@app.callback(
Output('app-2-display-value', 'children'),
[Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)