import dash_html_components as html
import dash_core_components as dcc

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

                # Filters section 1
                html.Div([
                    html.Div([
                        html.H5('Filter option 1', className='item-element-margin'),
                        dcc.Dropdown(
                            id='gen-filter-input-1',
                            placeholder="Filter",
                        ),
                        html.Div([], id="gen-filter-wrapper-1"),
                        html.Div(id="gen-filter-dump-1", style={'display': 'none'})
                    ], className='item-row item-select-height item-inline'),
                ], className='item-row  item-filter-section'),

                # Filter section 2
                html.Div([
                    html.Div([
                        html.H5('Filter option 2', className='item-element-margin'),
                        dcc.Dropdown(
                            id='gen-filter-input-2',
                            placeholder="Filter",
                        ),
                        html.Div([], id="gen-filter-wrapper-2"),
                        html.Div(id="gen-filter-dump-2", style={'display': 'none'})
                    ], className='item-row item-select-height item-inline'),
                ], className='item-row  item-filter-section'),

                # Filter section 3
                html.Div([
                    html.Div([
                        html.H5('Filter option 3', className='item-element-margin'),
                        dcc.Dropdown(
                            id='gen-filter-input-3',
                            placeholder="Filter",
                        ),
                        html.Div([], id="gen-filter-wrapper-3"),
                        html.Div(id="gen-filter-dump-3", style={'display': 'none'})
                    ], className='item-row item-select-height item-inline'),
                ], className='item-row item-filter-section'),

                # Hidden Element
                html.Div(id='gen-filter-store', style={'display': 'none'}),

                html.Button(
                    id='gen-filter-add',
                    className='button item-element-margin',
                    children='Add Filter',
                ),

                html.Button(
                    'Generate Graph',
                    className='button item-element-margin',
                    id="gen-button-1"),
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
