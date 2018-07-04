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


layout = html.Div([
    # Header
    html.Div([
        html.H1('Generate Graph', className='header-title'),

        # item-button, generate graph
        dcc.Link('Add Graph', href='#', className='button item-element-margin header-button'),

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
                html.Div([
                    html.H2('Generate Panel', className='item-element-margin'),
                    # Mode field
                    html.H5('Select graph mode to determine number of parameters', className='item-element-margin'),
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

                html.Div([
                    # Series field
                    html.H5('Select the series and vessel to be filtered', className='item-element-margin'),
                    dcc.Dropdown(
                        id='gen-series-input-1',
                        placeholder="Series",
                        options=[
                            {'label': k, 'value': k} for k in [
                                'A', 'B', 'C'
                            ]
                        ], className='item-element-margin'),
                    # Vessel field
                    dcc.Dropdown(
                        id='gen-vessel-input-1',
                        placeholder="Vessel"
                    ),
                    html.Div(id='gen-vessel-store')
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
                html.Div(id='gen-filter-store', style={'display': 'none'}),
                html.Div(id='gen-filter-dump', style={'display': 'none'}),

                html.Button(
                    'Add Filter',
                    className='button item-element-margin',
                    id='gen-filter-add'),

                html.Button(
                    'Generate Graph',
                    className='button item-element-margin',
                    id="gen-button-1"),

                html.Button(
                    id='gen-filter-submit',
                    className='button item-element-margin',
                    children='Submit'
                ),

                html.Button(
                    id='gen-filter-line',
                    className='button item-element-margin',
                    children='Line'
                ),

                # generate_filter_id(),

                # call filter layout
                html.Div(id='gen-filter'),

            ], className='item-wrapper item-settings-panel left-panel', id="item-wrapper"),
            html.Div([], id="gen-right-panel-wrapper"),

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
                className='item-element-margin-top',
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
                className='item-element-margin-top',
                placeholder='',
                type=input_type,
                value=''
            ),

            dcc.Input(
                id='gen-filter-value2-%d' % option_id,
                className='item-element-margin-top',
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
            options=options
        ),
    ]

    if mode == '3D':
        axis_parameters.append(
            dcc.Dropdown(
                id='gen-paramZ-input-1',
                placeholder=label_z,
                className="item-element-margin-top",
                options=options,
            )
        )
    else:
        axis_parameters.append(
            dcc.Input(id='gen-paramZ-input-1', style={'display': 'none'})
        )

    return axis_parameters


def generate_graph(mode, options):
    return html.Div([
        # Graph Panel
        html.Div([
            html.H2('Graph Panel', className='item-element-margin'),
            dcc.Graph(
                id='g2'
            )
        ], className='item-wrapper item-settings-panel right-panel', id="item-wrapper"),

        # Hidden Graph Store
        html.Div(id='g2-store', style={'display': 'none'}),
        html.Div(id='g2-param-store', style={'display': 'none'}),

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
                    html.Div(
                        id="gen-params-wrapper",
                        className='item-inline item-element-margin',
                        children=generate_axis_parameters(mode, options)
                    ),

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
