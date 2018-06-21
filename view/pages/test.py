import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

layout = \
    html.Div([
        html.H1("HELLO"),
        html.Button('Click Here', id='test-big-button'),

        # Template Usage Test
        html.Div(id='test-table-container'),

        # # Input Test
        # dcc.Input(
        #     id='test-input',
        #     className='form-control col-sm-4',
        #     placeholder='Enter a value...',
        #     type='text',
        #     value=''
        # ),

        # Vessal Data Dropdown Test
        html.Div([
            # Graph
            html.Div(id='test-vessel-graph-container'),
            html.Div(id='test-vessel-graph-container2'),
            # Table View of Data
            html.Div(id='test-vessel-table-container'),

            # User Vessel Choice
            dcc.Dropdown(
                id='test-vessel-dropdown',
                placeholder='Select a vessel',
                className='',
                clearable='True'
            ),

            # User Filter Choice(s)
            html.Div(id='test-vessel-filter')
        ]),

        # # Dropdown Test
        # html.Div([
        #     dcc.Dropdown(
        #         id='test-dropdown',
        #         placeholder='HELLO',
        #         className='',
        #         clearable='True',
        #         options=[
        #             {'label': 'Option', 'value': 'option'},
        #             {'label': 'Value', 'value': 'value'},
        #             {'label': 'DateTime', 'value': 'datetime'}]
        #     ),
        #     html.Div(id='test-dropdown-output', className='')
        # ], className=''),

        # Hidden Elements
        html.Div(id='test-dump1', style={'display': 'none'}),
        html.Div(id='test-dump2', style={'display': 'none'}),
        html.Div(id='test-dump3', style={'display': 'none'}),
        html.Div(id='test-start', style={'display': 'none'}),
        html.Div(id='test-vessel-dropdown-store', style={'display': 'none'}),
        html.Div(id='test-store', style={'display': 'none'})
    ], className='')

# Input form to obtain text
text_input = \
    [
        dcc.Input(
            id='test-input1',
            className='form-control col-sm-4',
            placeholder='Enter Min',
            type='text',
            value=''
        ),
        dcc.Input(
            id='test-input2',
            className='form-control col-sm-4',
            placeholder='Enter Max',
            type='text',
            value=''
        ),
        html.Button('Submit', id='test-submit'),
    ]

# Input form to obtain dropdown option
option_input = \
    html.H1('Option')

# Input form to obtain int/float
value_input = \
    [
        dcc.Input(
            id='test-input1',
            className='form-control col-sm-4',
            placeholder='Enter Min',
            type='number',
            value=''
        ),
        dcc.Input(
            id='test-input2',
            className='form-control col-sm-4',
            placeholder='Enter Max',
            type='number',
            value=''
        ),
        html.Button('Submit', id='test-submit')
    ]

# Input form to obtain DataTime
date_input = \
    [
        dcc.Input(
            id='test-input1',
            className='form-control col-sm-4',
            placeholder='Enter Min',
            type='date',
            value=''
        ),
        dcc.Input(
            id='test-input2',
            className='form-control col-sm-4',
            placeholder='Enter Max',
            type='date',
            value=''
        ),
        html.Button('Submit', id='test-submit')
    ]

# Input form to obtain DataTime using Dash Datepicker (NOT WORKING)
# TODO: Decide if worth continuing. Remove if aborted
# datepicker_input = \
#     [
#         dcc.DatePickerRange(
#             id='test-date-picker-range',
#             initial_visible_month=dt.now(),
#             start_date_placeholder_text='Start',
#             end_date_placeholder_text='End'
#         ),
#         html.Button('Submit', id='test-submit-datetime')
#     ]


"""
Usable Stuff
"""


def generate_vessel_filter(options):
    return [
        # Filter Options
        dcc.Dropdown(
            id='test-vessel-filter-option',
            className='',
            clearable='True',
            options=options
        ),

        # Data Graph and Table. Loads after specification given
        html.Div(id='test-vessel-data-display', className=''),

        # Filter Option Specifications
        html.Div(id='test-vessel-filter-specification', className=''),

        # Filter Option Specifications
        html.Div(id='test-vessel-filter-specification', className=''),

        # Hidden Elements
        html.Div(id='test-vessel-filter-dump', style={'display': 'none'}),
        html.Div(id='test-vessel-filter-1-input-dump', style={'display': 'none'}),
        html.Div(id='test-vessel-filter-2-input-dump', style={'display': 'none'})
    ]


def generate_filter_input(option_type):
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

    # Single Input
    if input_type == 'text':
        filter_input = [
            # Input
            html.Label(
                label1,
                className=''
            ),
            dcc.Input(
                id='test-vessel-filter-specification-input',
                className='form-control col-sm-4',
                placeholder='',
                type=input_type,
                value=''
            ),

            # Submit button
            html.Button(
                'Submit',
                id='test-vessel-filter-specification-submit',
                className=''
            )
        ]

    # Double Input
    else:
        filter_input = [
            # First input
            html.Label(
                label1,
                className=''
            ),
            dcc.Input(
                id='test-vessel-filter-specification-input1',
                className='form-control col-sm-4',
                placeholder='',
                type=input_type,
                value=''
            ),

            # Second input if not text
            html.Label(
                label2,
                className=''
            ),
            dcc.Input(
                id='test-vessel-filter-specification-input2',
                className='form-control col-sm-4',
                placeholder='',
                type=input_type,
                value=''
            ),

            # Submit button
            html.Button(
                'Submit',
                id='test-vessel-filter-specification-submit2',
                className=''
            )
            # Testing for Graph output, idk if this is how its supposed to be done
            #generate_graph()
        ]

    return filter_input


def generate_graph():
    return [
        dcc.Graph(id='test-vessel-graph'),

        # Test button
        html.Button(
            'Press',
            id='test-vessel-graph-button',
            className=''
        )
    ]
