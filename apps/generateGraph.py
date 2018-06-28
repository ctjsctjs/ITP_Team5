from dash.dependencies import Input, Output, State, Event
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt

from app import app

graphSettings = []
sliderList=[]

layout = html.Div([
#Header
html.Div([
   html.H1('Generate Graph', className='header-title'),

   #item-button, generate graph
   dcc.Link('Generate Graph', href='/apps/viewGraph', className='button item-element-margin header-button'),

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
    html.Div([], id="add-item-wrapper"),

    #item-button, add graph
    html.Button('Add Graph', className='button item-element-margin', id="add-button", n_clicks=0)

    ], className='content-wrapper page-width')
    ], className='wrapper-grey')
])

#callback for add button
@app.callback(
    Output('add-item-wrapper', 'children'),
    [Input('add-button', 'n_clicks')]
    )
def display_value(n_clicks):
    return html.Div([
        #item-wrapper
        html.Div([
        html.H2([], id='gen-output-{}'.format(i)),
        html.H2([], id='gen-output2-{}'.format(i)),

        #item-header
        html.Div([
            html.H5('Graph name', className='item-element-margin'),
            html.Div([
            dcc.Input(
                    placeholder='Graph Name',
                    type='text',
                    value='',
                    className="Select-control",
                    id='gen-name-input-{}'.format(i),
                )
            ]),
            dcc.Dropdown(
                    id='gen-mode-input-{}'.format(i),
                    placeholder="Mode",
                    value="2D",
                    options=[
                        {'label': k, 'value': k} for k in [
                            '2D', '3D'
                            ]
                        ])
        ], className='item-row item-select-height item-border-bottom item-inline'),

        #item-row, parameters
        html.Div([], className='item-border-bottom ', id='gen-param-wrapper-{}'.format(i)),

        #item-row, settings
        html.Div([

        html.Div([
        html.H5('Filter options', className='item-element-margin'),
        dcc.Dropdown(
            id='gen-filter-input-{}'.format(i),
            placeholder="Filter",
            options=[
                {'label': k, 'value': k} for k in [
                    'Series', 'Name', 'Date'
                ]
        ]),
        ], className='item-row item-select-height item-inline'),

        #item-row, settings
        html.Div([
        ], id='gen-filter-wrapper-{}'.format(i))
        ], className='item-row item-wrapper-bordered item-filter-section'),

        #html.Div(id='app-graph-display-value' ),
        ], className='item-wrapper item-wrapper-bordered', id="item-wrapper") for i in range(n_clicks)
    ])

limit = 10;

#Generate components for filter settings when filter option is selectd
for i in range(limit):
    @app.callback(
        Output('gen-filter-wrapper-{}'.format(i), 'children'),
        [Input('gen-filter-input-{}'.format(i), 'value')])
    def update_filer(filter):
        if (filter=="Series"):
            return html.Div([
                html.H5('Filter input', className='item-element-margin'),
                dcc.Dropdown(
                    id='gen-filter-input-value-{}'.format(i),
                    placeholder="Series",
                    options=[
                        {'label': k, 'value': k} for k in [
                            'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                        ]
                    ])
                ], className='item-row item-select-height  item-inline' )
        elif (filter=="Name"):
                return html.Div([
                html.H5('Filter input', className='item-element-margin'),
                dcc.Dropdown(
                    id='gen-filter-input-value-{}'.format(i),
                    placeholder="Name",
                    options=[
                        {'label': k, 'value': k} for k in [
                            'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                        ]
                    ])
                ], className='item-row item-select-height item-inline' )
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
            ], className='item-row item-select-height item-inline' )

#Callback to display 2 or 3 input for 2D or 3D graph
for i in range(limit):
    @app.callback(
        Output('gen-param-wrapper-{}'.format(i), 'children'),
        [Input('gen-mode-input-{}'.format(i), 'value')])
    def display_value(value):
        if (value=="2D"):
            return html.Div([
            html.H5('Parameters', className='item-element-margin'),
            dcc.Dropdown(
                id='gen-2D-input-value1-{}'.format(i),
                placeholder="Parameter X",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Speed', 'Power', 'Draft', 'RPM'
                        ]
            ]),
            dcc.Dropdown(
                id='gen-2D-input-value2-{}'.format(i),
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
                id='gen-2D-input-value1-{}'.format(i),
                placeholder="Parameter X",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Speed', 'Power', 'Draft', 'RPM'
                        ]
            ]),
            dcc.Dropdown(
                id='gen-2D-input-value2-{}'.format(i),
                placeholder="Parameter Y",
                options=[
                    {'label': k, 'value': k} for k in [
                        'Speed', 'Power', 'Draft', 'RPM'
                        ]
                ]),
            dcc.Dropdown(
                id='gen-2D-input-value3-{}'.format(i),
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
        Output('gen-output-{}'.format(i), 'children'),
        [Input('gen-name-input-{}'.format(i), 'value'),
        Input('gen-mode-input-{}'.format(i), 'value'),
        Input('gen-filter-input-{}'.format(i), 'value'),
        ])
    def update_output(name, mode, filter):
        return "Debug: " + str(name) + ", " + str(mode) + ", " + str(filter)

# Bind callback to each unique graph setting component
for i in range(limit):
    @app.callback(
        Output('gen-output2-{}'.format(i), 'children'),
        [Input('gen-filter-input-value-{}'.format(i), 'value')
        ])
    def update_outputz(value):
        return str(value)
