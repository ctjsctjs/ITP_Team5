from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt

from app import app

layout = html.Div([
#Header
html.Div([
   html.H1('Generate Graph', className='header-title'),

   #item-button, generate graph
   dcc.Link('Generate Graph', href='/apps/viewGraph', className='button item-element-margin header-button')

   ], className='wrapper-white header-wrapper page-width'),

#body-wrapper
html.Div([

#body-Content
html.Div([

    #item-wrapper
    html.Div([

    #item-header
    html.H2('Graph 1', className='item-element-margin'),

    #item-row, settings
    html.Div([
    dcc.Dropdown(
        id='app-graph-dropdown-filter',
        className='item-element-margin',
        placeholder="Filter",
        options=[
            {'label': i, 'value': i} for i in [
                'Series', 'Name', 'Date'
            ]
    ]),
    html.Div([], id="filter-field"),
    dcc.Dropdown(
            id='app-graph-dropdown-mode',
            className='item-element-margin',
            placeholder="Mode",
            value="2D",
            options=[
                {'label': i, 'value': i} for i in [
                    '2D', '3D'
                    ]
            ]),
    ], className='item-row item-element-margin item-select-height'),

    #item-row, parameters
    html.Div([

    ], className='item-row item-element-margin item-select-height', id="field-params"),

    #html.Div(id='app-graph-display-value' ),
    ], className='item-wrapper', id="item-wrapper"),

    html.Div([], id="add-item-wrapper"),

    #item-button, add graph
    html.Button('Add Graph', className='button item-element-margin', id="add-button", n_clicks=0)

    ], className='content-wrapper page-width')
    ], className='wrapper-grey')
])


@app.callback(
    Output('add-item-wrapper', 'children'),
    [Input('add-button', 'n_clicks')])
def display_value(value):
    if (value>0):
        return html.Div([

        #item-header
        html.H2('Graph 2', className='item-element-margin'),

        #item-row, settings
        html.Div([
        dcc.Dropdown(
            id='app-graph-dropdown-filter-2',
            className='item-element-margin',
            placeholder="Filter",
            options=[
                {'label': i, 'value': i} for i in [
                    'Series', 'Name', 'Date'
                ]
        ], class="item-dropdown"),
        html.Div([], id="filter-field-2"),
        dcc.Dropdown(
                id='app-graph-dropdown-mode',
                className=' item-element-margin',
                placeholder="Mode",
                value="2D",
                options=[
                    {'label': i, 'value': i} for i in [
                        '2D', '3D'
                        ]
                    ], class="item-dropdown"),
        ], className='item-row item-element-margin item-select-height'),

        #item-row, parameters
        html.Div([

        ], className='item-row item-element-margin item-select-height', id="field-params-2"),

        #html.Div(id='app-graph-display-value' ),
        ], className='item-wrapper', id="item-wrapper-2")


@app.callback(
    Output('field-params', 'children'),
    [Input('app-graph-dropdown-mode', 'value')])
def display_value(value):
    if (value=="2D"):
        return html.Div([
        dcc.Dropdown(
            id='app-graph-dropdown',
            className='item-element-margin',
            placeholder="Parameter X",
            options=[
                {'label': i, 'value': i} for i in [
                    'Speed', 'Power', 'Draft', 'RPM'
                    ]
        ], class="item-dropdown"),
        dcc.Dropdown(
            id='app-graph-dropdown',
            className='item-element-margin',
            placeholder="Parameter Y",
            options=[
                {'label': i, 'value': i} for i in [
                    'Speed', 'Power', 'Draft', 'RPM'
                    ]
        ], class="item-dropdown"),
    ])
    else:
        return html.Div([
        dcc.Dropdown(
            id='app-graph-dropdown',
            className='item-element-margin',
            placeholder="Parameter X",
            options=[
                {'label': i, 'value': i} for i in [
                    'Speed', 'Power', 'Draft', 'RPM'
                    ]
        ]),
        dcc.Dropdown(
            id='app-graph-dropdown',
            className='item-element-margin',
            placeholder="Parameter Y",
            options=[
                {'label': i, 'value': i} for i in [
                    'Speed', 'Power', 'Draft', 'RPM'
                    ]
            ]),
        dcc.Dropdown(
            id='app-graph-dropdown',
            className=' item-element-margin',
            placeholder="Parameter Z",
            options=[
                {'label': i, 'value': i} for i in [
                    'Speed', 'Power', 'Draft', 'RPM'
                    ]
            ])
])


@app.callback(
    Output('filter-field', 'children'),
    [Input('app-graph-dropdown-filter', 'value')])
def display_value(value):
    if (value=="Series" or value=="Name"):
        return html.Div([
        dcc.Dropdown(
                id='app-graph-dropdown',
                className='item-element-margin',
                placeholder="Name",
                options=[
                    {'label': i, 'value': i} for i in [
                        'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                    ]
                ])
            ])
    elif (value=="Date"):
            return html.Div([
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
        ])
