import dash_html_components as html
import dash_core_components as dcc


def generate_filter_id():
    filter_ids = []
    for i in range(1, 3):
        filter_ids.append(html.Div(id='gen-filter-input-{}'.format(i)))

    return html.Div(
        id='',
        children=filter_ids
    )


def generate_axis_parameters(mode, options):
    label_x = "Parameter X"
    label_y = "Parameter Y"
    label_z = "Parameter Z"

    axis_parameters = [
        # Axis Parameters Input store
        html.Div(id='gen-params-store', style={'display': 'none'}),
        html.Div(id='gen-test-store', style={'display': 'none'}),

        # Axis Parameters Dropdowns
        dcc.Dropdown(
            id='gen-paramX-input-1',
            placeholder=label_x,
            options=options,
            className='item-element-margin'
        ),
        dcc.Dropdown(
            id='gen-paramY-input-1',
            placeholder=label_y,
            options=options,
            className='item-element-margin'
        ),
    ]

    if mode == '3D':
        axis_parameters.append(
            dcc.Dropdown(
                id='gen-paramZ-input-1',
                placeholder=label_z,
                options=options,
                className='item-element-margin'
            )
        )
    else:
        axis_parameters.append(
            dcc.Input(id='gen-paramZ-input-1', style={'display': 'none'})
        )

    return axis_parameters


layout = html.Div([
    # Header
    html.Div([

        html.H1('Ship Performance Analysis', className='header-title'),

        # item-button, generate graph
        html.Button('Add Graph', className='button item-element-margin header-button'),
        html.Button('Save Settings', className='button item-element-margin header-button', id='save-all-btn'),

        html.P('Graph generation tool that provides an insight to ship performance',
               className='title-desc'),

        # this is a hack: include a hidden dcc component so that
        # dash registers and serve's this component's JS and CSS
        # libraries
        dcc.Input(style={'display': 'none'})
    ], className='wrapper-white header-wrapper page-width'),

    # body-wrapper
    html.Div([

        # body-Content
        html.Div([
            # Generate Panel
            html.Div([

                # Tutorial Tooltip
                html.Div([
                    html.I(className="fas fa-caret-down icon"),
                    "Enter settings to begin"],
                    className='tutorial-tooltip',
                ),
                html.H2('Generate Panel', className='item-element-margin'),
                html.Div([
                    # html.Button([
                    #     html.I(className="fas fa-caret-left icon"),
                    #     ],id='toggle-minimize-panel',
                    #     className='button-round toggle-panel-button',
                    # ),

                    html.H3([
                        'Database'
                    ], className='input-label item-element-margin'),
                    html.H5([
                        html.I(className="fas fa-exclamation-circle icon"),
                        '1. Select database of dataset'
                    ], className='helper-text item-element-margin'),
                    # Database field
                    dcc.Dropdown(
                        id='gen-database-input-1',
                        placeholder="Database",
                        className='item-element-margin'),
                    # Hidden Database field dump
                    html.Div(id='gen-database-input-dump', style={'display': 'none'}),
                ], className='item-row item-select-height item-inline'),
                # Mode field
                html.Div([
                    html.H3([
                        'Mode'
                    ], className='input-label item-element-margin'),
                    html.H5([
                        html.I(className="fas fa-exclamation-circle icon"),
                        '2. Select graph mode to determine number of parameters'
                    ], className='helper-text item-element-margin'),
                    dcc.RadioItems(
                        id='gen-mode-input-1',
                        labelStyle={'display': 'block', 'margin-bottom': '6px'},
                        options=[
                            {'label': '2 Dimensions', 'value': '2D'},
                            {'label': '3 Dimensions', 'value': '3D'}
                        ],
                        value="2D"
                    ),
                ], className='item-row item-select-height item-inline'),

                # Param field
                html.Div([
                    html.H3([
                        'Parameters'
                    ], className='input-label item-element-margin'),
                    html.H5([
                        html.I(className="fas fa-exclamation-circle icon"),
                        '3. Select the parameters of the graph'
                    ], className='helper-text item-element-margin'),
                    # Axis Parameters
                    html.Div(
                        id="gen-params-wrapper",
                        # className='custom-panel',
                        # className='item-inline item-element-margin',
                    ),
                    # Hidden Axis Parameters dump
                    html.Div(id='gen-params-dump', style={'display': 'none'}),
                ], className='item-row item-select-height item-inline'),

                # Vessel field
                html.Div([
                    html.H3([
                        'Vessel'
                    ], className='input-label item-element-margin'),
                    html.H5([
                        html.I(className="fas fa-exclamation-circle icon"),
                        '4. Select the vessel series and name to be filtered'
                    ], className='helper-text item-element-margin'),
                    # Series field
                    dcc.Dropdown(
                        id='gen-series-input-1',
                        placeholder="Series",
                        className='item-element-margin'),
                    # Vessel field
                    dcc.Dropdown(
                        id='gen-vessel-input-1',
                        placeholder="Vessel",
                        multi=True
                    ),
                    html.Div(id='gen-vessel-store'),

                    # Hidden Series/Vessels Elements
                    html.Div(id='gen-series-dump', style={'display': 'none'}),
                ], className='item-row item-select-height item-inline'),

                # # Filter section 3
                # html.Div([
                #     html.Div([
                #         html.H5('Filter option 3', className='item-element-margin'),
                #         dcc.Dropdown(
                #             id='gen-filter-input-3',
                #             placeholder="Filter",
                #         ),
                #         html.Div([], id="gen-filter-wrapper-3"),
                #         html.Div(id="gen-filter-dump-3", style={'display': 'none'})
                #     ], className='item-row item-select-height item-inline'),
                # # ], className='item-row item-filter-section'),
                # html.Div([
                #     html.Div([
                #         html.Div(dcc.Slider(id='slider-{}'.format(i))),
                #         html.Div(id='output-{}'.format(i), style={'marginTop': 30})
                #     ]) for i in range(n_clicks)]
                # )
                # Hidden Element
                # html.Div(id='gen-filter-store', style={'display': 'none'}),

                # Filter field
                html.Div([
                    html.H3([
                        'Filters'
                    ], className='input-label item-element-margin'),
                    html.H5([
                        html.I(className="fas fa-exclamation-circle icon"),
                        '5. Add filters to scope down the data'
                    ], className='helper-text item-element-margin'),

                    html.Div(id='gen-filter-dump', style={'display': 'none'}),

                    html.Button([
                        html.I(className="fas fa-plus-circle icon"),
                        'Add Filter',
                    ], className='button item-element-margin add-filter-btn',
                        id='gen-filter-add'),
                    # call filter layout
                    html.Div(id='gen-filter'),
                ], className='item-row item-select-height item-inline'),
                #
                # # Load File field
                # html.Div([
                #     html.H3([
                #         'Load Line'
                #     ], className='input-label item-element-margin'),
                #     html.H5([
                #         html.I(className="fas fa-exclamation-circle icon"),
                #         '6. Select the file to load'
                #     ], className='helper-text item-element-margin'),
                #     # File field
                #     dcc.Dropdown(
                #         id='gen-loadline-input-1',
                #         placeholder="File",
                #         className='item-element-margin'
                #     ),
                #
                #     # # Hidden Line Elements
                #     html.Div(id='gen-loadline-dump', style={'display': 'none'}),
                # ], className='item-row item-select-height item-inline'),

                html.Button([
                    html.I(className="fas fa-caret-right icon"),
                    'Generate Graph',
                ], className='button item-element-margin margin-right-12',
                    id="gen-button-1",
                    style={'display': 'block'}
                ),

                html.Button(
                    id='gen-filter-submit',
                    className='button item-element-margin hidden',
                    children='Update Graph',
                ),
                #
                # html.Button(
                #     id='gen-filter-line',
                #     className='button item-element-margin',
                #     children='Line'
                # ),

                # generate_filter_id(),


                # hidden store
                html.Div(id='save-setting', style={'display': 'none'}),
                html.Div(id='save-setting-filter', style={'display': 'none'}),

            ], className='item-wrapper item-settings-panel left-panel', id="item-wrapper"),

            html.Div([
            ], id="gen-right-panel-wrapper"),

        ], className='content-wrapper page-width')
    ], className='wrapper-grey')
])


def generate_filter_input(option_type, option_id):
    # Setup Input Type Label Text TODO: Reconsider hardcoded option types
    if option_type == 'varchar':
        input_type = 'text'
        label1 = 'Text'
    elif option_type == 'int' or option_type == 'float':
        input_type = 'number'
        label1 = 'Min'
        label2 = 'Max'
    elif option_type == 'datetime':
        input_type = 'date'
        label1 = 'Start'
        label2 = 'End'
    else:
        input_type = None
        label1 = None
        label2 = None

    # No Input [Used to generate id]
    if input_type is None:
        filter_input = [
            dcc.Input(
                id='gen-filter-value1-%d' % option_id,
                style={'display': 'none'}
            ),
            dcc.Input(
                id='gen-filter-value2-%d' % option_id,
                style={'display': 'none'}
            )
        ]

    # Single Input
    elif input_type == 'text':
        filter_input = [
            dcc.Input(
                id='gen-filter-value1-%d' % option_id,
                className='item-element-margin form-control form-control-sm ',
                placeholder='',
                type=input_type,
                value=''
            ),
            dcc.Input(
                id='gen-filter-value2-%d' % option_id,
                style={'display': 'none'}
            )
        ]

    # Double Input
    else:
        filter_input = [
            dcc.Input(
                id='gen-filter-value1-%d' % option_id,
                className='item-element-margin form-control form-control-sm ',
                placeholder='',
                type=input_type,
                value=''
            ),

            dcc.Input(
                id='gen-filter-value2-%d' % option_id,
                className='item-element-margin form-control form-control-sm ',
                placeholder='',
                type=input_type,
                value=''
            ),
        ]

    return filter_input


def add_filters(n_clicks):
    return \
        html.Div([
            html.Div([
                html.Div([
                    html.H5('Filter option {}'.format(k + 1), className='item-element-margin'),
                    dcc.Dropdown(
                        id='gen-filter-input-{}'.format(k + 1),
                        className='item-element-margin',
                        placeholder="Filter",
                        style={'display': 'none'}
                    ),
                    html.Div([], id="gen-filter-wrapper-{}".format(k + 1)),
                    html.Div(id="gen-filter-dump-{}".format(k + 1), style={'display': 'none'})
                ], className='item-row item-select-height item-inline')
                for k in range(n_clicks)
            ], className='item-row item-filter-section'),
        ], id='gen-filter'),


def add_hidden_filters(n_clicks):
    return \
        html.Div([
            html.Div([
                html.H5('Filter option {}'.format(k), className='item-element-margin'),
                dcc.Dropdown(
                    id='gen-filter-input-{}'.format(k),
                    className='item-element-margin',
                    placeholder="Filter",
                ),
                html.Div([
                    dcc.Input(
                        id='gen-filter-value1-{}'.format(k),
                        style={'display': 'none'}
                    ),
                    dcc.Input(
                        id='gen-filter-value2-{}'.format(k),
                        style={'display': 'none'}
                    )
                ], id="gen-filter-wrapper-{}".format(k)),
                html.Div(id="gen-filter-dump-{}".format(k))
            ], className='item-row item-select-height item-inline', style={'display': 'none'})
            for k in range(1, n_clicks + 1)
        ], className='item-row item-filter-section'),


def generate_dropdown_filter(n):
    return \
        html.Div([
            html.H5('Filter option {}'.format(n), className='item-element-margin'),
            dcc.Dropdown(
                id='gen-filter-input-{}'.format(n),
                placeholder="Filter",
            ),
            html.Div([
                dcc.Input(
                    id='gen-filter-value1-{}'.format(n),
                    style={'display': 'none'}
                ),
                dcc.Input(
                    id='gen-filter-value2-{}'.format(n),
                    style={'display': 'none'}
                )
            ], id="gen-filter-wrapper-{}".format(n), style={'display': 'none'}),
            html.Div(id="gen-filter-dump-{}".format(n), style={'display': 'none'})
        ], className='item-row item-select-height item-inline'),


def generate_graph(mode, options):
    return html.Div([
        # Graph Panel
        html.Div([
            html.H2('Graph Panel', className='item-element-margin'),
            dcc.Graph(
                id='g2'
            ),

        ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),

        # Hidden Graph Store
        html.Div(id='g2-store', style={'display': 'none'}),
        html.Div(id='g2-param-store', style={'display': 'none'}),
        html.Div(id='gen-filter-store', style={'display': 'none'}),

        # Information Panel
        html.Div([

            # Customise Panel
            html.Div([
                html.H2('Information Panel', className='item-element-margin'),
                html.Div([
                    html.H5('Settings Information', className='item-element-margin'),
                    html.Span([], className="settings-info", id='gen-settings-mode-1'),
                    html.Span([], className="settings-info", id='gen-settings-series-1'),
                    html.Span([], className="settings-info", id='gen-settings-vessel-1'),
                    html.Span([], className="settings-info", id='gen-paramX-output-1'),
                    html.Span([], className="settings-info", id='gen-paramY-output-1'),
                    html.Span([], className="settings-info", id='gen-paramZ-output-1'),
                    html.Span([], className="settings-info", id='gen-settings-output-1'),
                ], className='custom-panel', id="item-wrapper"),

                # DIV to populate paramater fields TODO: shift to left panel
                # html.Div([
                #     html.H5('Settings options', className='item-element-margin'),
                #     # Graph name input
                #     dcc.Input(
                #         placeholder='Graph Name',
                #         type='text',
                #         value=''
                #     ),
                #     # X axis label input
                #     dcc.Input(
                #         placeholder='X axis label',
                #         type='text',
                #         value=''
                #     ),
                #     # Y axis label input
                #     dcc.Input(
                #         placeholder='Y axis label',
                #         type='text',
                #         value=''
                #     ),
                # ], className='custom-panel'),

                html.Div([
                    html.H5('Filter Information', className='item-element-margin'),
                    html.Span([], className="settings-info", id='gen-settings-filter1-1'),
                    html.Span([], className="settings-info", id='gen-settings-filter2-1'),
                    html.Span([], className="settings-info", id='gen-settings-filter3-1'),
                    html.Span([], className="settings-info", id='gen-output-value1-1'),
                    html.Span([], className="settings-info", id='gen-output-value2-1'),
                    html.Span([], className="settings-info", id='gen-output-value3-1'),
                ], className='custom-panel'),

                html.Div([
                    html.H5('Graph Information', className='item-element-margin'),
                    html.Span([], className="settings-info", id='gen-settings-rsquared-1'),
                    html.Span([], className="settings-info", id='gen-settings-sols-1'),
                    html.Span([], className="settings-info", id='gen-settings-formula-1'),
                    # TODO: output regression, equation, etc
                ], className='custom-panel'),

            ], className='item-row item-select-height'),

            # Customise Panel
            html.Div([
                html.H2('Customize Panel', className='item-element-margin'),

                html.Div([
                    html.H5('Settings options', className='item-element-margin'),
                    # Graph name input
                    dcc.Input(
                        id='gen-graph-name',
                        className='item-element-margin form-control form-control-sm',
                        placeholder='Graph Name',
                        type='text',
                        value=''
                    ),
                    # X axis label input
                    dcc.Input(
                        className='item-element-margin form-control form-control-sm',
                        placeholder='X axis label',
                        type='text',
                        value=''
                    ),
                    # Y axis label input
                    dcc.Input(
                        className='item-element-margin form-control form-control-sm',
                        placeholder='Y axis label',
                        type='text',
                        value=''
                    ),
                ], className='custom-panel'),

                html.Div([
                    # Settings checklist form
                    html.H5('Settings options', className='item-element-margin'),
                    dcc.Checklist(
                        id="gen-settings-input-1",
                        options=[
                            {'label': 'Toggle Regression', 'value': 'regression'},
                            {'label': 'Toggle Clustering', 'value': 'clustering'},
                            {'label': 'Toggle Datapoints', 'value': 'datapoints'}
                        ],
                        labelStyle={'display': 'block', 'margin-bottom': '6px'},
                        values=[]
                    ),
                ], className='custom-panel'),
                html.Div([

                    # Regression type input
                    html.H5('Select the regression degree of the graph', className='item-element-margin'),
                    dcc.Dropdown(
                        id='gen-regression-input-1',
                        placeholder="Graph Mode",
                        className='item-element-margin'),
                    html.Div(id='gen-regression-input-dump', style={'display': 'none'}),

                    # Outliers  input
                    html.H5('Select the outliers threshold level of the graph', className='item-element-margin'),
                    dcc.Dropdown(
                        id='gen-threshold-input-1',
                        placeholder="Threshold",
                        className='item-element-margin',
                        value='None'),
                    html.Div(id='gen-threshold-input-dump', style={'display': 'none'}),

                    # Clusters input
                    html.H5('Select the number of clusters of the graph', className='item-element-margin'),
                    dcc.Input(
                        id='gen-kmeans-cluster',
                        type='number',
                        className='item-element-margin form-control form-control-sm',
                    ),

                ], className='custom-panel'),

            ], className='item-row item-select-height'),

        ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),
    ])

# def generate_graph():
#     return html.Div([
#         # Graph Panel
#         html.Div([
#             html.H2('Graph Panel', className='item-element-margin'),
#             dcc.Graph(
#                 id='g2'
#             )
#         ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),
#
#         # Information Panel
#         html.Div([
#             html.Div([
#                 html.H2('Information Panel', className='item-element-margin'),
#                 html.Span([], className="settings-info", id='gen-settings-mode-1'),
#                 html.Span([], className="settings-info", id='gen-settings-series-1'),
#                 html.Span([], className="settings-info", id='gen-settings-vessel-1'),
#                 html.Span([], className="settings-info", id='gen-settings-filter1-1'),
#                 html.Span([], className="settings-info", id='gen-settings-filter2-1'),
#                 html.Span([], className="settings-info", id='gen-settings-filter3-1'),
#                 html.Span([], className="settings-info", id='gen-output-value1-1'),
#                 html.Span([], className="settings-info", id='gen-output-value2-1'),
#                 html.Span([], className="settings-info", id='gen-output-value3-1'),
#                 html.Span([], className="settings-info", id='gen-paramX-output-1'),
#                 html.Span([], className="settings-info", id='gen-paramY-output-1'),
#                 html.Span([], className="settings-info", id='gen-paramZ-output-1'),
#                 html.Span([], className="settings-info", id='gen-settings-output-1'),
#             ], className='item-wrapper item-settings-panel left-panel', id="item-wrapper"),
#
#             # Customise Panel
#             html.Div([
#                 html.H2('Customize Panel', className='item-element-margin'),
#                 html.Div([
#                     html.H5('Parameter options', className='item-element-margin'),
#
#                     # DIV to populate paramater fields
#                     html.Div([], className='item-inline item-element-margin', id="gen-params-wrapper"),
#
#                     # Settings checklist form
#                     html.H5('Settings options', className='item-element-margin'),
#                     dcc.Checklist(
#                         id="gen-settings-input-1",
#                         options=[
#                             {'label': 'Clustering', 'value': 'clustering'},
#                             {'label': 'Regression', 'value': 'regression'},
#                             {'label': 'Color', 'value': 'color'}
#                         ],
#                         labelStyle={'display': 'block', 'margin-bottom': '6px'},
#                         values=[]
#                     )
#                 ], className='item-row item-select-height item-inline'),
#             ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),
#         ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),
#     ])
