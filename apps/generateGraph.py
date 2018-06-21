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
   html.Button('Add a slider', id='button', n_clicks=0),
    html.Div(id='slider-container'),

    # this is a hack: include a hidden dcc component so that
    # dash registers and serve's this component's JS and CSS
    # libraries
    dcc.Input(style={'display': 'none'})
   ], className='wrapper-white header-wrapper page-width'),

#body-wrapper
html.Div([

#body-Content
html.Div([

    #item-wrapper
    html.Div([

    #item-header
    html.Div([
        html.H5('Graph name', className='item-element-margin'),
        dcc.Input(
            placeholder='Graph Name',
            type='text',
            value=''
        )
    ], className='item-row item-element-margin item-select-height item-border-bottom'),

    #item-row, settings
    html.Div([
    html.H5('Settings', className='item-element-margin'),
    dcc.Dropdown(
        id='app-graph-dropdown-filter',
        className='item-dropdown item-element-margin',
        placeholder="Filter",
        options=[
            {'label': i, 'value': i} for i in [
                'Series', 'Name', 'Date'
            ]
    ]),

    dcc.Dropdown(
            id='app-graph-dropdown-mode',
            className='item-dropdown item-element-margin',
            placeholder="Mode",
            value="2D",
            options=[
                {'label': i, 'value': i} for i in [
                    '2D', '3D'
                    ]
                ]),
    ], className='item-row item-element-margin item-select-height item-border-bottom'),

#item-row, settings
    html.Div([
        html.H5('Filter', className='item-element-margin')
    ], id="filter-field"),

    #item-row, parameters
    html.Div([
    ], className='item-row item-element-margin item-select-height', id="field-params"),

    #html.Div(id='app-graph-display-value' ),
    ], className='item-wrapper', id="item-wrapper"),

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
    [],
    [State('app-graph-dropdown-filter', 'value'),
    State('app-graph-dropdown-mode', 'value')],
    [Event('add-button', 'click')]
    )
def display_value(input1,input2):
    newGraph = {"label": "Graph " + str(len(graphSettings)), "value": str(input1) + "," + str(input2)}
    graphSettings.append(newGraph)
    print "New Graph settings: " + str(graphSettings) + "\n"

    return html.Div([
        html.H5('Graph List', className='item-element-margin'),
        dcc.Checklist(
        options=graphSettings,
        values= [i for i in [graphSettings]],
        labelStyle={'display': 'block'}
    )
], className='item-wrapper item-select-height', id="item-wrapper-2")


@app.callback(
    Output('field-params', 'children'),
    [Input('app-graph-dropdown-mode', 'value')])
def display_value(value):
    if (value=="2D"):
        return html.Div([
        html.H5('Parameters', className='item-element-margin'),
        dcc.Dropdown(
            id='app-graph-dropdown',
            className='item-dropdown item-element-margin',
            placeholder="Parameter X",
            options=[
                {'label': i, 'value': i} for i in [
                    'Speed', 'Power', 'Draft', 'RPM'
                    ]
        ]),
        dcc.Dropdown(
            id='app-graph-dropdown',
            className='item-dropdown item-element-margin',
            placeholder="Parameter Y",
            options=[
                {'label': i, 'value': i} for i in [
                    'Speed', 'Power', 'Draft', 'RPM'
                    ]
    ])
    ])
    else:
        return html.Div([
        html.H5('Parameters', className='item-element-margin'),
        dcc.Dropdown(
            id='app-graph-dropdown',
            className='item-dropdown item-element-margin',
            placeholder="Parameter X",
            options=[
                {'label': i, 'value': i} for i in [
                    'Speed', 'Power', 'Draft', 'RPM'
                    ]
        ]),
        dcc.Dropdown(
            id='app-graph-dropdown',
            className='item-dropdown item-element-margin',
            placeholder="Parameter Y",
            options=[
                {'label': i, 'value': i} for i in [
                    'Speed', 'Power', 'Draft', 'RPM'
                    ]
            ]),
        dcc.Dropdown(
            id='app-graph-dropdown',
            className='item-dropdown item-element-margin',
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
        html.H5('Filters', className='item-element-margin'),
        dcc.Dropdown(
                id='app-graph-dropdown',
                className='item-dropdown item-element-margin',
                placeholder="Name",
                options=[
                    {'label': i, 'value': i} for i in [
                        'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                    ]
                ])
            ], className='item-row item-element-margin item-select-height item-border-bottom' )
    elif (value=="Date"):
            return html.Div([
            html.H5('Filters', className='item-element-margin'),
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
        ], className='item-row item-element-margin item-select-height item-border-bottom' )


###SLIDER TEST TO GENERATE INFINITE COMPONENTS
@app.callback(
    Output('slider-container', 'children'),
    [Input('button', 'n_clicks')])
def add_sliders(n_clicks):
    #sliderList.append("1")
    #print "LENGTH" + str(sliderList)
    return \
        html.Div([
            html.Div([
                html.Div(dcc.Slider(id='slider-{}'.format(i))),
                dcc.Input(
                    id='input-{}'.format(i),
                    placeholder='Graph Name',
                    type='text',
                    value=''
                ),
                html.Div(id='output-{}'.format(i), style={'marginTop': 30})
            ]) for i in range(n_clicks)]
        )


# up to 10 sliders
for i in range(10):
    @app.callback(
        Output('slider-{}'.format(i), 'children'),
        [Input('slider-{}'.format(i), 'value'),
        Input('input-{}'.format(i), 'value')])
    def update_output(slider_i_value, input_i_value):
        return str(slider_i_value) + str(input_i_value)
