from dash.dependencies import Input, Output, State, Event
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt

from app import app

layout = html.Div([
#Header
html.Div([
   html.H1('Generate Graph', className='header-title'),

   #item-button, generate graph
   dcc.Link('Add Graph', href='#', className='button item-element-margin header-button'),

    # this is a hack: include a hidden dcc component so that
    # dash registers and serve's this component's JS and CSS
    # libraries
    dcc.Input(style={'display': 'none'})
   ], className='wrapper-white header-wrapper page-width'),

#body-wrapper
html.Div([

#body-Content
html.Div([
    #items added
    html.Div([

    #item-header

    html.Div([
        html.H2('Generate Panel', className='item-element-margin'),
        html.H5('Mode', className='item-element-margin'),
        dcc.RadioItems(
            id='gen-mode-input-1',
            options=[
                {'label': '2 Dimensions', 'value': '2D'},
                {'label': '3 Dimensions', 'value': '3D'}
            ],
        ),
    ], className='item-row item-select-height item-inline'),

    html.Div([
        dcc.Dropdown(
            id='gen-series-input-1',
            placeholder="Series",
            options=[
                {'label': k, 'value': k} for k in [
                    'A', 'B', 'C'
                ]
        ], className='item-element-margin'),
        dcc.Dropdown(
            id='gen-vessel-input-1',
            placeholder="Vessel",
            options=[
                {'label': k, 'value': k} for k in [
                    'A', 'B', 'C'
                ]
        ]),
    ], className='item-row item-select-height item-inline'),
    #item-row, settings
    html.Div([
        html.Div([
            html.H5('Filter options', className='item-element-margin'),
            dcc.Dropdown(
                id='gen-filter-input-1',
                placeholder="Filter",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Text', 'Range', 'Date'
                    ]
                ]),
                html.Div([
                    dcc.Dropdown(
                        id='value-1',
                        placeholder="Vessel",
                        options=[
                            {'label': k, 'value': k} for k in [
                                'A', 'B', 'C'
                            ]
                    ]),
                ], id="gen-filter-wrapper-1"),
            ], className='item-row item-select-height item-inline'),
        ], className='item-row  item-filter-section'),
        html.Div([
        html.Div([
            html.H5('Filter options', className='item-element-margin'),
            dcc.Dropdown(
                id='gen-filter-input-2',
                placeholder="Filter",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Text', 'Range', 'Date'
                    ]
                ]),
                html.Div([], id="gen-filter-wrapper-2"),
            ], className='item-row item-select-height item-inline'),
        ], className='item-row  item-filter-section'),
        html.Div([
        html.Div([
            html.H5('Filter options', className='item-element-margin'),
            dcc.Dropdown(
                id='gen-filter-input-3',
                placeholder="Filter",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Text', 'Range', 'Date'
                    ]
                ]),
                html.Div([], id="gen-filter-wrapper-3"),
            ], className='item-row item-select-height item-inline'),
        ], className='item-row item-filter-section'),
        html.Button('Generate Graph', className='button item-element-margin', id="add-button"),

        #html.Div(id='app-graph-display-value' ),
        ], className='item-wrapper item-wrapper-bordered item-settings-panel left-panel', id="item-wrapper"),
        html.Div([
                html.H2('Graph Panel', className='item-element-margin'),

        #JEROME: WHERE THE GRAPH IS GENERATED
        ], className='item-wrapper item-wrapper-bordered item-settings-panel right-panel', id="item-wrapper"),
        html.Div([
                html.H2('Information Panel', className='item-element-margin'),
                html.Span([], className="settings-info", id='gen-settings-mode-1'),
                html.Span([], className="settings-info", id='gen-settings-series-1'),
                html.Span([], className="settings-info", id='gen-settings-vessel-1'),
                html.Span([], className="settings-info", id='gen-settings-filter1-1'),
                html.Span([], className="settings-info", id='gen-settings-filter2-1'),
                html.Span([], className="settings-info", id='gen-settings-filter3-1'),
        ], className='item-wrapper item-wrapper-bordered item-settings-panel right-panel', id="item-wrapper"),
        html.Div([
                html.H2('Customize Panel', className='item-element-margin'),
                html.Div([
                    html.H5('Parameter options', className='item-element-margin'),
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
                        options=[
                            {'label': k, 'value': k} for k in [
                                'A', 'B', 'C'
                            ]
                    ]),

                    html.H5('Settings options', className='item-element-margin'),
                    dcc.Checklist(
                        options=[
                            {'label': 'Clustering', 'value': 'clustering'},
                            {'label': 'Regression', 'value': 'regression'},
                            {'label': 'Color', 'value': 'color'}
                        ],
                        values=['MTL', 'SF']
                    )
                    ], className='item-row item-select-height item-inline'),
        ], className='item-wrapper item-wrapper-bordered item-settings-panel right-panel', id="item-wrapper"),
        #item-button, add graph
        ], className='content-wrapper page-width')
    ], className='wrapper-grey')
])

@app.callback(
    Output('gen-filter-wrapper-1', 'children'),
    [Input('gen-filter-input-1', 'value')])
def update_filer(filter):
    if (filter=="Text"):
        return html.Div([
            dcc.Dropdown(
                id='value-1',
                placeholder="Series",
                options=[
                    {'label': k, 'value': k} for k in [
                        'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                    ]
                ])
            ], className='item-row item-inline' )
    elif (filter=="Range"):
        return html.Div([
        dcc.RangeSlider(
            id='value-1',
            marks={i: '{}'.format(i) for i in range(-5, 7)},
            min=-5,
            max=6,
            value=[-3, 4]
        )
    ], className='item-row item-inline')
    elif (filter=="Date"):
        return html.Div([
        dcc.DatePickerRange(
            id='value-1',
            start_date=dt(1997, 5, 3),
            end_date_placeholder_text='Select a date!'
        )
    ], className='item-row item-inline')

@app.callback(
    Output('gen-filter-wrapper-2', 'children'),
    [Input('gen-filter-input-2', 'value')])
def update_filer(filter):
    if (filter=="Text"):
        return html.Div([
            dcc.Dropdown(
                id='value-2',
                placeholder="Series",
                options=[
                    {'label': k, 'value': k} for k in [
                        'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                    ]
                ])
            ], className='item-row item-inline' )
    elif (filter=="Range"):
        return html.Div([
        dcc.RangeSlider(
            id='value-2',
            marks={i: '{}'.format(i) for i in range(-5, 7)},
            min=-5,
            max=6,
            value=[-3, 4]
        )
    ], className='item-row item-inline')
    elif (filter=="Date"):
        return html.Div([
        dcc.DatePickerRange(
            id='value-2',
            start_date=dt(1997, 5, 3),
            end_date_placeholder_text='Select a date!'
        )
    ], className='item-row item-inline')


@app.callback(
    Output('gen-filter-wrapper-3', 'children'),
    [Input('gen-filter-input-3', 'value')])
def update_filer(filter):
    if (filter=="Text"):
        return html.Div([
            dcc.Dropdown(
                id='value-3',
                placeholder="Series",
                options=[
                    {'label': k, 'value': k} for k in [
                        'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                    ]
                ])
            ], className='item-row item-inline' )
    elif (filter=="Range"):
        return html.Div([
        dcc.RangeSlider(
            id='value-3',
            marks={i: '{}'.format(i) for i in range(-5, 7)},
            min=-5,
            max=6,
            value=[-3, 4]
        )
    ], className='item-row item-inline')
    elif (filter=="Date"):
        return html.Div([
        dcc.DatePickerRange(
            id='value-3',
            start_date=dt(1997, 5, 3),
            end_date_placeholder_text='Select a date!'
        )
    ], className='item-row item-inline')

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