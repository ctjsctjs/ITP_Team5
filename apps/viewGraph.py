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
    #items added
    html.Div([], id="view-item-wrapper"),

    #item-button, add graph
    html.Button('invis', className='button item-element-margin hidden', id="init-button", n_clicks=1)

    ], className='content-wrapper page-width')
    ], className='wrapper-grey')
])

#callback for add button
@app.callback(
    Output('view-item-wrapper', 'children'),
    [Input('init-button', 'n_clicks')]
    )
def display_value(n_clicks):
    return html.Div([
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
        ], className="eight columns"),
        html.Details([

        #item-wrapper
        html.Div([
        html.H2([], id='view-output-{}'.format(i)),
        html.H2([], id='view-output2-{}'.format(i)),

        #item-header
        html.Div([
            html.H5('Graph name', className='item-element-margin'),
            html.Div([
            dcc.Input(
                    placeholder='Graph Name',
                    type='text',
                    value='',
                    className="Select-control",
                    id='view-name-input-{}'.format(i),
                )
            ]),

            dcc.Dropdown(
                    id='view-mode-input-{}'.format(i),
                    placeholder="Mode",
                    value="2D",
                    className="hidden",
                    options=[
                        {'label': k, 'value': k} for k in [
                            '2D', '3D'
                            ]
                        ]),
        ], className='item-row item-element-margin item-select-height item-border-bottom item-inline'),



        #item-row, parameters
        html.Div([], className='item-border-bottom ',id='view-param-wrapper-{}'.format(i)),

        html.Div([

        #item-row, settings
        html.Div([
        html.H5('Filter options', className='item-element-margin'),
        dcc.Dropdown(
            id='view-filter-input-{}'.format(i),
            placeholder="Filter",
            value='Series',
            options=[
                {'label': k, 'value': k} for k in [
                    'Series', 'Name', 'Date'
                ]
        ]),
        ], className='item-row item-select-height item-inline'),

        #item-row, settings
        html.Div([], id='view-filter-wrapper-{}'.format(i))

        ], className='item-row item-wrapper-bordered item-filter-section'),

        html.Div([], id='view-add-filter-wrapper-{}'.format(i)),

            #item-button, add graph
        html.Button('Add Filter', className='button margin-top-12', id='add-filter-button-{}'.format(i), n_clicks=0)

        #html.Div(id='app-graph-display-value' ),
        ], className='item-wrapper item-wrapper-bordered', id="item-wrapper")
        ])
        ]) for i in range(n_clicks)
    ])


limit = 10;

for i in range(limit):
    @app.callback(
        Output('view-add-filter-wrapper-{}'.format(i), 'children'),
        [Input('add-filter-button-{}'.format(i), 'n_clicks')])
    def add_filter(n_clicks):
        return html.Div([
            html.Div([

            #item-row, settings
            html.Div([
            html.H5('Filter options', className='item-element-margin'),
            dcc.Dropdown(
                id='view-added-filter-input-{}'.format(i),
                placeholder="Filter",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Series', 'Name', 'Date'
                    ]
            ]),
            ], className='item-row item-select-height item-inline'),

            #item-row, settings
            html.Div([], id='view-added-filter-wrapper-{}'.format(i))

            ], className='item-row item-wrapper-bordered item-filter-section')  for i in range(n_clicks)
        ])

#Generate components for filter settings when filter option is selectd
for i in range(limit):
    @app.callback(
        Output('view-filter-wrapper-{}'.format(i), 'children'),
        [Input('view-filter-input-{}'.format(i), 'value')])
    def update_filer(filter):
        if (filter=="Series"):
            return html.Div([
                html.H5('Filter input', className='item-element-margin'),
                dcc.Dropdown(
                    id='view-filter-input-value-{}'.format(i),
                    placeholder="Series",
                    options=[
                        {'label': k, 'value': k} for k in [
                            'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                        ]
                    ])
                ], className='item-row item-select-height item-border-bottom  item-inline' )
        elif (filter=="Name"):
                return html.Div([
                html.H5('Filter input', className='item-element-margin'),
                dcc.Dropdown(
                    id='view-filter-input-value-{}'.format(i),
                    placeholder="Name",
                    options=[
                        {'label': k, 'value': k} for k in [
                            'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                        ]
                    ])
                ], className='item-row item-select-height item-border-bottom  item-inline' )
        elif (filter=="Date"):
                return html.Div([
                html.H5('Filter input', className='item-element-margin'),
                dcc.DatePickerSingle(
                    clearable=True,
                    with_portal=True,
                    date=dt.now()
                    ),
                dcc.DatePickerSingle(
                    clearable=True,
                    with_portal=True,
                    date=dt.now()
                    )
            ], className='item-row item-select-height item-border-bottom item-inline' )

#Callback to display 2 or 3 input for 2D or 3D graph
for i in range(limit):
    @app.callback(
        Output('view-param-wrapper-{}'.format(i), 'children'),
        [Input('view-mode-input-{}'.format(i), 'value')])
    def display_value(value):
        if (value=="2D"):
            return html.Div([
            html.H5('Parameters', className='item-element-margin'),
            dcc.Dropdown(
                id='view-2D-input-value1-{}'.format(i),
                placeholder="Parameter X",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Speed', 'Power', 'Draft', 'RPM'
                        ]
            ]),
            dcc.Dropdown(
                id='view-2D-input-value2-{}'.format(i),
                placeholder="Parameter Y",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Speed', 'Power', 'Draft', 'RPM'
                        ]
                    ])
        ], className='item-row item-select-height item-inline'),

        else:
            return html.Div([
            html.H5('Parameters', className='item-element-margin'),
            dcc.Dropdown(
                id='view-2D-input-value1-{}'.format(i),
                placeholder="Parameter X",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Speed', 'Power', 'Draft', 'RPM'
                        ]
            ]),
            dcc.Dropdown(
                id='view-2D-input-value2-{}'.format(i),
                placeholder="Parameter Y",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Speed', 'Power', 'Draft', 'RPM'
                        ]
                ]),
            dcc.Dropdown(
                id='view-2D-input-value3-{}'.format(i),
                placeholder="Parameter Z",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Speed', 'Power', 'Draft', 'RPM'
                        ]
                ])
        ], className='item-row item-select-height item-inline')


# Bind callback to each unique graph setting component
for i in range(limit):
    @app.callback(
        Output('view-output-{}'.format(i), 'children'),
        [Input('view-name-input-{}'.format(i), 'value'),
        Input('view-mode-input-{}'.format(i), 'value'),
        Input('view-filter-input-{}'.format(i), 'value'),
        ])
    def update_output(name, mode, filter):
        return "Debug: " + str(name) + ", " + str(mode) + ", " + str(filter)

# Bind callback to each unique graph setting component
for i in range(limit):
    @app.callback(
        Output('view-output2-{}'.format(i), 'children'),
        [Input('view-filter-input-value-{}'.format(i), 'value')
        ])
    def update_outputz(value):
        return str(value)
