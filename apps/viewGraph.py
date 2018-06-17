from dash.dependencies import Input, Output
import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import controller.graph_components.fitting_master as fm
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
        placeholder="Series",
        options=[
            {'label': i, 'value': i} for i in [
                'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E', 'Parameter F'
            ]
    ]),
    dcc.Dropdown(
    id='app-graph-dropdown',
        className='panel-item-dropdown item-element-margin',
    placeholder="Name",
    options=[
        {'label': i, 'value': i} for i in [
            'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E', 'Parameter F'
        ]
    ]),
    dcc.Dropdown(
        id='app-graph-dropdown',
        className='panel-item-dropdown item-element-margin',
        placeholder="Mode",
        options=[
            {'label': i, 'value': i} for i in [
                'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E', 'Parameter F'
            ]
    ]),
    dcc.Dropdown(
        id='app-graph-dropdown',
        className='panel-item-dropdown item-element-margin',
        placeholder="Parameter X",
        options=[
            {'label': i, 'value': i} for i in [
                'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E', 'Parameter F'
            ]
    ]),
    dcc.Dropdown(
        id='app-graph-dropdown',
        className='panel-item-dropdown item-element-margin',
        placeholder="Parameter Y",
        options=[
            {'label': i, 'value': i} for i in [
                'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E', 'Parameter F'
            ]
        ])
], className='item-wrapper'),
], className='panel-left'),

    #panel-right
    html.Div([
        html.Div([
            html.Div(id='app-graph-display-value'),
                html.Div([
                html.Div([
                        html.H3('Column 3'),
                        dcc.Graph(id='g2', figure=fm.generateGraphTest(
                        xData = [12.0,20.3,20.4,20.1,20.2,20.2,20.2,19.9,21.7,20.0,19.4,12.9,20.0],
                        yData = [62.2,165.7,157.2,154.6,152.3,160.3,159.4,160.2,159.4,160.0,148.4,29.3,42.7],
                        xData2 = [19.0,12.6,19.0,20.0,19.9,19.4,12.5,18.8,18.7,20.2,19.8,17.1,18.0],
                        yData2=[132.4,43.2,129.1,139.4,139.8,144.6,115.8,160.8,119.9,139.7,139.2,134.5,135.2])
                        )
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
